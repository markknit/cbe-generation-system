"""
CBE Lesson Plan Generation - Main Production Pipeline
Orchestrates Spark + Multi-Model APIs + GPU Embedding + Monitoring

This is the main entry point for the complete system.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

# Spark imports
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, udf, pandas_udf, explode
from pyspark.sql.types import StringType, ArrayType, FloatType, StructType, StructField

# Local imports
from src.config import Config
from src.api_clients.multi_model_client import MultiModelClient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CBEProductionPipeline:
    """
    Complete production pipeline for CBE lesson plan generation
    
    Pipeline Stages:
    1. PDF Processing (Spark parallel)
    2. GPU Embedding Generation (Spark + GPU)
    3. Vector DB Population (Spark bulk insert)
    4. RAG Context Retrieval (Spark parallel queries)
    5. Multi-Model Generation (Spark orchestrates APIs)
    6. Quality Validation (Spark parallel validation)
    7. HTML Assembly & Export (Spark parallel)
    8. Analytics & Reporting (Spark aggregation)
    """
    
    def __init__(self, config: Config):
        """Initialize pipeline with configuration"""
        self.config = config
        
        # Initialize Spark
        self.spark = self._init_spark()
        
        # Initialize API client
        self.api_client = MultiModelClient(config)
        
        # Initialize monitoring
        self.start_time = None
        self.metrics = {
            'pdfs_processed': 0,
            'chunks_created': 0,
            'embeddings_generated': 0,
            'lessons_generated': 0,
            'lessons_validated': 0,
            'total_cost': 0.0
        }
        
        logger.info("✅ CBE Production Pipeline initialized")
    
    def _init_spark(self) -> SparkSession:
        """Initialize Spark with GPU support"""
        logger.info("🔧 Initializing Spark...")
        
        builder = SparkSession.builder
        
        # Apply configuration
        for key, value in self.config.spark.get_spark_conf().items():
            builder = builder.config(key, value)
        
        spark = builder.getOrCreate()
        
        # Set checkpoint directory
        spark.sparkContext.setCheckpointDir(self.config.spark.checkpoint_dir)
        
        logger.info(f"✅ Spark initialized: {spark.sparkContext.appName}")
        logger.info(f"   Master: {spark.sparkContext.master}")
        logger.info(f"   Parallelism: {spark.sparkContext.defaultParallelism}")
        
        return spark
    
    def stage1_process_pdfs(self, pdf_directory: str) -> DataFrame:
        """
        Stage 1: Process all PDF curriculum documents in parallel
        
        Returns: DataFrame with curriculum chunks
        """
        logger.info("\n" + "="*80)
        logger.info("STAGE 1: PDF PROCESSING (Parallel)")
        logger.info("="*80)
        
        import glob
        pdf_paths = glob.glob(f"{pdf_directory}/**/*.pdf", recursive=True)
        logger.info(f"📚 Found {len(pdf_paths)} PDF files")
        
        # Create DataFrame of PDF paths
        pdf_df = self.spark.createDataFrame(
            [(path,) for path in pdf_paths],
            ["pdf_path"]
        )
        
        # Define UDF for PDF parsing
        @udf(returnType=ArrayType(StructType([
            StructField("text", StringType()),
            StructField("metadata", StringType())
        ])))
        def parse_pdf_udf(pdf_path: str):
            """Parse PDF - runs in parallel across Spark workers"""
            import pdfplumber
            import json
            
            try:
                chunks = []
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text and text.strip():
                            chunks.append({
                                "text": text,
                                "metadata": json.dumps({
                                    "source": pdf_path,
                                    "page": page_num + 1
                                })
                            })
                return chunks
            except Exception as e:
                logger.error(f"Error parsing {pdf_path}: {e}")
                return []
        
        # Process all PDFs in parallel
        start_time = time.time()
        parsed_df = pdf_df.withColumn("chunks", parse_pdf_udf("pdf_path"))
        
        # Explode chunks
        chunks_df = parsed_df.select("pdf_path", explode("chunks").alias("chunk"))
        chunks_df = chunks_df.select(
            "pdf_path",
            col("chunk.text").alias("chunk_text"),
            col("chunk.metadata").alias("metadata")
        )
        
        # Cache for performance
        chunks_df.cache()
        chunk_count = chunks_df.count()
        elapsed = time.time() - start_time
        
        self.metrics['pdfs_processed'] = len(pdf_paths)
        self.metrics['chunks_created'] = chunk_count
        
        logger.info(f"✅ Processed {len(pdf_paths)} PDFs in {elapsed:.1f}s")
        logger.info(f"✅ Extracted {chunk_count} chunks")
        logger.info(f"   Speedup: ~{len(pdf_paths) * 30 / elapsed:.0f}x vs sequential")
        
        return chunks_df
    
    def stage2_generate_embeddings(self, chunks_df: DataFrame) -> DataFrame:
        """
        Stage 2: Generate embeddings using GPU acceleration
        
        Returns: DataFrame with embeddings
        """
        logger.info("\n" + "="*80)
        logger.info("STAGE 2: GPU-ACCELERATED EMBEDDING GENERATION")
        logger.info("="*80)
        
        import pandas as pd
        
        # Pandas UDF for GPU-accelerated embedding
        @pandas_udf("array<float>")
        def embed_batch_udf(texts: pd.Series) -> pd.Series:
            """Generate embeddings - uses GPU if available"""
            import torch
            from sentence_transformers import SentenceTransformer
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = SentenceTransformer(
                self.config.embedding.model_name,
                device=device
            )
            
            embeddings = model.encode(
                texts.tolist(),
                batch_size=self.config.embedding.batch_size,
                convert_to_tensor=True,
                show_progress_bar=False,
                normalize_embeddings=self.config.embedding.normalize_embeddings
            )
            
            return pd.Series([emb.cpu().tolist() for emb in embeddings])
        
        start_time = time.time()
        embedded_df = chunks_df.withColumn("embedding", embed_batch_udf("chunk_text"))
        
        # Force computation
        embedded_df.cache()
        embedding_count = embedded_df.count()
        elapsed = time.time() - start_time
        
        self.metrics['embeddings_generated'] = embedding_count
        
        logger.info(f"✅ Generated {embedding_count} embeddings in {elapsed:.1f}s")
        logger.info(f"   Throughput: {embedding_count / elapsed:.0f} embeddings/sec")
        logger.info(f"   Using: {self.config.embedding.device.upper()}")
        
        return embedded_df
    
    def stage3_populate_vectordb(self, embedded_df: DataFrame):
        """
        Stage 3: Populate vector database with embeddings
        """
        logger.info("\n" + "="*80)
        logger.info("STAGE 3: VECTOR DATABASE POPULATION")
        logger.info("="*80)
        
        # Convert to Pandas for ChromaDB insertion
        # (ChromaDB doesn't have native Spark support yet)
        logger.info("📊 Converting to Pandas for batch insert...")
        pandas_df = embedded_df.toPandas()
        
        import chromadb
        client = chromadb.PersistentClient(path=self.config.vectordb.persist_directory)
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name=self.config.vectordb.collection_name,
            metadata={"hnsw:space": self.config.vectordb.distance_metric}
        )
        
        # Batch insert
        logger.info(f"💾 Inserting {len(pandas_df)} vectors...")
        start_time = time.time()
        
        collection.add(
            embeddings=pandas_df['embedding'].tolist(),
            documents=pandas_df['chunk_text'].tolist(),
            metadatas=pandas_df['metadata'].apply(lambda x: eval(x)).tolist(),
            ids=[f"chunk_{i}" for i in range(len(pandas_df))]
        )
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Vector DB populated in {elapsed:.1f}s")
        logger.info(f"   Collection: {self.config.vectordb.collection_name}")
        
        return collection
    
    def stage4_generate_lessons(self, 
                                num_lessons: int,
                                curriculum_context: str) -> DataFrame:
        """
        Stage 4: Generate lessons using multi-model pipeline
        Orchestrates parallel API calls with intelligent rate limiting
        """
        logger.info("\n" + "="*80)
        logger.info(f"STAGE 4: MULTI-MODEL LESSON GENERATION ({num_lessons} lessons)")
        logger.info("="*80)
        
        # Create generation tasks
        tasks = []
        for i in range(num_lessons):
            tasks.append({
                'lesson_id': f"lesson_{i+1:04d}",
                'lesson_number': i + 1,
                'curriculum_context': curriculum_context
            })
        
        tasks_df = self.spark.createDataFrame(tasks)
        
        # Partition for rate limiting
        # Use fewer partitions than RPM to avoid overwhelming APIs
        num_partitions = min(30, num_lessons)
        tasks_df = tasks_df.repartition(num_partitions)
        
        logger.info(f"📊 Distributed across {num_partitions} partitions")
        
        # Stage 4a: Gemini Draft Generation
        if self.config.generation.use_gemini_for_drafts:
            logger.info("\n🔵 Phase 4a: Gemini generating drafts...")
            
            @udf(returnType=StringType())
            def generate_draft_udf(lesson_id: str, context: str):
                """Generate draft using Gemini"""
                import time
                import random
                time.sleep(random.uniform(0.1, 0.5))  # Jitter
                
                prompt = f"""
Generate a draft lesson plan for CBE curriculum.

Context:
{context}

Generate initial content including:
- Learning activities
- Resources needed
- Teaching strategies
- Assessment ideas

Focus on content quality, not formatting.
"""
                
                try:
                    result = self.api_client.generate_gemini(prompt)
                    return result['content']
                except Exception as e:
                    return f"ERROR: {str(e)}"
            
            start_time = time.time()
            tasks_df = tasks_df.withColumn(
                "draft",
                generate_draft_udf(col("lesson_id"), col("curriculum_context"))
            )
            tasks_df.cache()
            tasks_df.count()  # Force computation
            elapsed = time.time() - start_time
            
            logger.info(f"   ✅ Drafts complete in {elapsed:.1f}s")
        
        # Stage 4b: GPT-5 Structuring
        if self.config.generation.use_gpt5_for_structure:
            logger.info("\n🟢 Phase 4b: GPT-5 structuring...")
            
            @udf(returnType=StringType())
            def structure_udf(draft: str):
                """Structure draft into CBE format using GPT-5"""
                import time
                import random
                time.sleep(random.uniform(0.1, 0.5))
                
                prompt = f"""
Transform this draft into proper CBE format:

DRAFT:
{draft}

CREATE:
1. Specific Learning Outcomes table
2. Overview (Key Inquiry Question, Purpose, Safety Notes)
3. 5-column Lesson Implementation Framework:
   - Learner Experience
   - Resource Link
   - Teacher Moves
   - Sensemaking Strategy
   - Formative Assessment
4. Teacher Reflection (5 questions)
5. Summary Table Prompt

Use proper HTML table structure.
"""
                
                try:
                    result = self.api_client.generate_gpt5(prompt)
                    return result['content']
                except Exception as e:
                    return f"ERROR: {str(e)}"
            
            start_time = time.time()
            tasks_df = tasks_df.withColumn("structured", structure_udf(col("draft")))
            tasks_df.cache()
            tasks_df.count()
            elapsed = time.time() - start_time
            
            logger.info(f"   ✅ Structuring complete in {elapsed:.1f}s")
        
        # Stage 4c: Claude Polish (selective)
        if self.config.generation.use_claude_for_polish:
            logger.info(f"\n🟣 Phase 4c: Claude polishing top {self.config.generation.polish_percentage*100:.0f}%...")
            
            # Sample for polishing (top 50% by default)
            sample_fraction = self.config.generation.polish_percentage
            polished_df = tasks_df.sample(fraction=sample_fraction, seed=42)
            
            @udf(returnType=StringType())
            def polish_udf(structured: str):
                """Polish with Claude"""
                import time
                import random
                time.sleep(random.uniform(0.1, 0.5))
                
                prompt = f"""
Final quality pass on this CBE lesson plan:

{structured}

Fix:
1. Any missing sections
2. HTML formatting
3. Ensure all 5 columns present
4. Add checkboxes (☐) for assessments
5. Verify Kenyan context
6. Polish language

Return perfected version.
"""
                
                try:
                    result = self.api_client.generate_claude(prompt)
                    return result['content']
                except Exception as e:
                    return structured  # Fallback to unpolished
            
            start_time = time.time()
            polished_df = polished_df.withColumn("final", polish_udf(col("structured")))
            polished_df.cache()
            polished_count = polished_df.count()
            elapsed = time.time() - start_time
            
            logger.info(f"   ✅ Polished {polished_count} lessons in {elapsed:.1f}s")
            
            # Join back with unpolished
            tasks_df = tasks_df.join(
                polished_df.select("lesson_id", "final"),
                on="lesson_id",
                how="left"
            )
            # Use polished if available, otherwise structured
            from pyspark.sql.functions import when, coalesce
            tasks_df = tasks_df.withColumn(
                "final_content",
                coalesce(col("final"), col("structured"))
            )
        else:
            tasks_df = tasks_df.withColumnRenamed("structured", "final_content")
        
        self.metrics['lessons_generated'] = num_lessons
        
        logger.info(f"\n✅ Stage 4 complete: {num_lessons} lessons generated")
        
        return tasks_df
    
    def stage5_validate_lessons(self, lessons_df: DataFrame) -> DataFrame:
        """
        Stage 5: Validate all lessons in parallel
        """
        logger.info("\n" + "="*80)
        logger.info("STAGE 5: QUALITY VALIDATION (Parallel)")
        logger.info("="*80)
        
        @udf(returnType=StructType([
            StructField("is_valid", StringType()),
            StructField("quality_score", FloatType()),
            StructField("errors", ArrayType(StringType()))
        ]))
        def validate_udf(content: str):
            """Validate lesson quality"""
            errors = []
            
            # Required sections
            required_sections = [
                "Specific Learning Outcomes",
                "Lesson Implementation Framework",
                "Teacher Reflection"
            ]
            for section in required_sections:
                if section not in content:
                    errors.append(f"Missing: {section}")
            
            # Required columns
            required_columns = [
                "Learner Experience",
                "Resource Link",
                "Teacher Moves",
                "Sensemaking Strategy",
                "Formative Assessment"
            ]
            for col_name in required_columns:
                if col_name not in content:
                    errors.append(f"Missing column: {col_name}")
            
            # Kenyan context
            kenyan_indicators = ['Kenya', 'KSh', 'KPLC']
            if not any(ind in content for ind in kenyan_indicators):
                errors.append("Missing Kenyan context")
            
            quality_score = max(0.0, 1.0 - len(errors) * 0.1)
            is_valid = "true" if len(errors) == 0 else "false"
            
            return {
                "is_valid": is_valid,
                "quality_score": quality_score,
                "errors": errors
            }
        
        start_time = time.time()
        validated_df = lessons_df.withColumn(
            "validation",
            validate_udf(col("final_content"))
        )
        
        # Extract validation fields
        validated_df = validated_df.select(
            "*",
            col("validation.is_valid").alias("is_valid"),
            col("validation.quality_score").alias("quality_score"),
            col("validation.errors").alias("errors")
        )
        
        validated_df.cache()
        total = validated_df.count()
        valid = validated_df.filter(col("is_valid") == "true").count()
        elapsed = time.time() - start_time
        
        self.metrics['lessons_validated'] = total
        
        logger.info(f"✅ Validated {total} lessons in {elapsed:.1f}s")
        logger.info(f"   Valid: {valid}/{total} ({valid/total*100:.1f}%)")
        logger.info(f"   Avg Quality: {validated_df.agg({'quality_score': 'avg'}).collect()[0][0]:.2f}")
        
        return validated_df
    
    def stage6_export_html(self, validated_df: DataFrame, output_dir: str):
        """
        Stage 6: Export HTML files in parallel
        """
        logger.info("\n" + "="*80)
        logger.info("STAGE 6: HTML EXPORT (Parallel)")
        logger.info("="*80)
        
        # Convert to Pandas for file writing
        pandas_df = validated_df.select(
            "lesson_id",
            "lesson_number",
            "final_content",
            "quality_score"
        ).toPandas()
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📝 Exporting {len(pandas_df)} HTML files...")
        start_time = time.time()
        
        for _, row in pandas_df.iterrows():
            filename = f"Lesson_{row['lesson_number']:04d}_{row['lesson_id']}.html"
            filepath = output_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(row['final_content'])
        
        elapsed = time.time() - start_time
        
        logger.info(f"✅ Exported {len(pandas_df)} files in {elapsed:.1f}s")
        logger.info(f"   Output: {output_dir}")
        
        return output_path
    
    def run_full_pipeline(self, 
                         pdf_directory: str,
                         num_lessons: int = 100) -> Dict:
        """
        Execute complete end-to-end pipeline
        
        Args:
            pdf_directory: Path to curriculum PDFs
            num_lessons: Number of lessons to generate
            
        Returns:
            Dictionary with pipeline metrics and results
        """
        self.start_time = time.time()
        
        logger.info("\n" + "="*100)
        logger.info("CBE LESSON PLAN GENERATION - FULL PIPELINE")
        logger.info("="*100)
        logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Target: {num_lessons} lessons")
        logger.info("="*100)
        
        try:
            # Stage 1: Process PDFs
            chunks_df = self.stage1_process_pdfs(pdf_directory)
            
            # Stage 2: Generate Embeddings
            embedded_df = self.stage2_generate_embeddings(chunks_df)
            
            # Stage 3: Populate Vector DB
            collection = self.stage3_populate_vectordb(embedded_df)
            
            # Get curriculum context (simplified - in production would use RAG)
            curriculum_context = "Kenya CBE Grade 10 Physics curriculum focusing on inquiry-based learning."
            
            # Stage 4: Generate Lessons
            lessons_df = self.stage4_generate_lessons(num_lessons, curriculum_context)
            
            # Stage 5: Validate
            validated_df = self.stage5_validate_lessons(lessons_df)
            
            # Stage 6: Export
            output_dir = self.config.paths.html_output
            output_path = self.stage6_export_html(validated_df, str(output_dir))
            
            # Get final metrics
            total_time = time.time() - self.start_time
            self.metrics['total_time'] = total_time
            self.metrics['total_cost'] = self.api_client.cost_tracker.total_cost
            
            # Print final summary
            self._print_final_summary()
            
            return {
                'success': True,
                'metrics': self.metrics,
                'output_path': str(output_path),
                'total_time': total_time
            }
            
        except Exception as e:
            logger.error(f"\n❌ Pipeline failed: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'metrics': self.metrics
            }
        finally:
            # Cleanup
            self.spark.stop()
    
    def _print_final_summary(self):
        """Print comprehensive pipeline summary"""
        logger.info("\n" + "="*100)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("="*100)
        
        logger.info(f"\n📊 Processing Metrics:")
        logger.info(f"   PDFs Processed: {self.metrics['pdfs_processed']}")
        logger.info(f"   Chunks Created: {self.metrics['chunks_created']}")
        logger.info(f"   Embeddings Generated: {self.metrics['embeddings_generated']}")
        logger.info(f"   Lessons Generated: {self.metrics['lessons_generated']}")
        logger.info(f"   Lessons Validated: {self.metrics['lessons_validated']}")
        
        logger.info(f"\n💰 Cost Metrics:")
        self.api_client.print_cost_summary()
        
        logger.info(f"\n⏱️  Performance Metrics:")
        logger.info(f"   Total Time: {self.metrics['total_time']:.1f}s ({self.metrics['total_time']/60:.1f} min)")
        logger.info(f"   Time per Lesson: {self.metrics['total_time']/self.metrics['lessons_generated']:.1f}s")
        logger.info(f"   Throughput: {self.metrics['lessons_generated']/(self.metrics['total_time']/3600):.1f} lessons/hour")
        
        logger.info("\n" + "="*100)
        logger.info("✅ PIPELINE COMPLETE")
        logger.info("="*100 + "\n")


def main():
    """Main entry point"""
    import sys
    
    # Load configuration
    config = Config()
    config.validate()
    config.print_summary()
    
    # Initialize pipeline
    pipeline = CBEProductionPipeline(config)
    
    # Run pipeline
    pdf_directory = str(config.paths.curriculum_pdfs)
    num_lessons = 10  # Start with 10 for testing
    
    results = pipeline.run_full_pipeline(
        pdf_directory=pdf_directory,
        num_lessons=num_lessons
    )
    
    if results['success']:
        logger.info(f"\n✅ Success! Output: {results['output_path']}")
        sys.exit(0)
    else:
        logger.error(f"\n❌ Failed: {results['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
