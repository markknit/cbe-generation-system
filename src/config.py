"""
Configuration Management for CBE Lesson Plan Generation System
Handles all API credentials, Spark settings, and pipeline parameters
"""
import os
from typing import Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()


@dataclass
class APIConfig:
    """API credentials and model settings"""
    
    # Anthropic Claude
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    claude_model: str = "claude-sonnet-4-6"
    claude_max_tokens: int = 8000
    claude_temperature: float = 0.7
    
    # OpenAI GPT
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    gpt_model: str = "gpt-5"
    gpt_max_tokens: int = 8000
    gpt_temperature: float = 0.7
    
    # Google Gemini
    gemini_api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = "gemini-3-flash-preview"
    gemini_max_tokens: int = 8000
    gemini_temperature: float = 0.7
    
    # Rate Limits (requests per minute)
    claude_rpm: int = 50
    openai_rpm: int = 60
    gemini_rpm: int = 60
    
    # Batch processing
    enable_batch_api: bool = True
    batch_size: int = 50
    
    # Pricing (per million tokens) - Updated Jan 2026
    pricing: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
        "claude-opus-4-5": {"input": 5.00, "output": 25.00},
        "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
        "gpt-5": {"input": 1.25, "output": 10.00},
        "gpt-5.2": {"input": 1.75, "output": 14.00},
        "gpt-5-mini": {"input": 0.25, "output": 2.00},
        "gemini-3-flash": {"input": 0.50, "output": 3.00},
        "gemini-3-pro": {"input": 2.00, "output": 12.00},
    })
    
    def validate(self) -> bool:
        """Validate all API keys are present"""
        missing = []
        if not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        
        if missing:
            raise ValueError(f"Missing API keys: {', '.join(missing)}")
        return True


@dataclass
class SparkConfig:
    """Apache Spark cluster configuration"""
    
    app_name: str = "CBE-Lesson-Generator"
    master: str = "local[*]"  # Use local[*] for local mode, spark://host:port for cluster
    
    # Memory settings
    driver_memory: str = "64g"
    executor_memory: str = "32g"
    executor_cores: int = 16
    
    # Parallelism
    default_parallelism: int = 128
    sql_shuffle_partitions: int = 200
    
    # GPU settings (Blackwell)
    gpu_enabled: bool = True
    gpu_per_executor: int = 1
    rapids_enabled: bool = False  # RAPIDS acceleration (optional)
    
    # Storage
    checkpoint_dir: str = "./data/spark-checkpoints"
    temp_dir: str = "./data/spark-temp"
    
    # Performance
    serializer: str = "org.apache.spark.serializer.KryoSerializer"
    memory_fraction: float = 0.8
    
    def get_spark_conf(self) -> Dict[str, str]:
        """Generate Spark configuration dictionary"""
        conf = {
            "spark.app.name": self.app_name,
            "spark.master": self.master,
            "spark.driver.memory": self.driver_memory,
            "spark.executor.memory": self.executor_memory,
            "spark.executor.cores": str(self.executor_cores),
            "spark.default.parallelism": str(self.default_parallelism),
            "spark.sql.shuffle.partitions": str(self.sql_shuffle_partitions),
            "spark.serializer": self.serializer,
            "spark.memory.fraction": str(self.memory_fraction),
        }
        
        if self.gpu_enabled:
            conf.update({
                "spark.executor.resource.gpu.amount": str(self.gpu_per_executor),
                "spark.task.resource.gpu.amount": "1",
                "spark.rapids.sql.enabled": str(self.rapids_enabled).lower(),
            })
        
        return conf


@dataclass
class EmbeddingConfig:
    """Embedding generation configuration"""
    
    # Model settings
    model_name: str = "all-MiniLM-L6-v2"
    model_dimension: int = 384
    
    # Processing settings
    batch_size: int = 256
    max_seq_length: int = 512
    device: str = "cuda"  # "cuda" or "cpu"
    normalize_embeddings: bool = True
    
    # GPU optimization
    use_mixed_precision: bool = True
    num_workers: int = 4
    pin_memory: bool = True


@dataclass
class VectorDBConfig:
    """ChromaDB vector database configuration"""
    
    persist_directory: str = "./data/vectordb"
    collection_name: str = "cbe_curriculum"
    
    # Embedding settings
    embedding_dimension: int = 384
    distance_metric: str = "cosine"  # "cosine", "l2", or "ip"
    
    # Retrieval settings
    n_results: int = 10
    min_similarity: float = 0.5
    
    # Performance
    batch_size: int = 5000
    use_hnsw: bool = True
    hnsw_space: str = "cosine"
    hnsw_ef: int = 200
    hnsw_m: int = 16


@dataclass
class GenerationConfig:
    """Lesson generation pipeline configuration"""
    
    # Multi-model pipeline stages
    use_gemini_for_drafts: bool = True
    use_gpt5_for_structure: bool = True
    use_claude_for_polish: bool = True
    
    # Processing parameters
    polish_percentage: float = 0.5  # Polish top 50% based on quality scores
    num_lessons_per_substrand: int = 8
    
    # Quality control
    min_quality_score: float = 0.7
    require_validation: bool = True
    auto_fix_errors: bool = True
    max_validation_errors: int = 3
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2  # seconds
    exponential_backoff: bool = True
    
    # Output settings
    output_format: str = "html"
    output_directory: str = "./data/outputs/lesson_plans"
    save_intermediate: bool = True
    create_backups: bool = True


@dataclass
class MonitoringConfig:
    """Monitoring, logging, and observability configuration"""
    
    # Prometheus metrics
    enable_prometheus: bool = True
    prometheus_port: int = 8000
    
    # Logging
    enable_logging: bool = True
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_directory: str = "./logs"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cost tracking
    enable_cost_tracking: bool = True
    cost_alert_threshold: float = 100.0  # USD
    track_cost_per_lesson: bool = True
    
    # Quality monitoring
    enable_quality_monitoring: bool = True
    quality_alert_threshold: float = 0.6
    
    # Performance monitoring
    enable_performance_monitoring: bool = True
    track_latency: bool = True
    track_throughput: bool = True


@dataclass
class PathConfig:
    """File system paths configuration"""
    
    # Base paths
    project_root: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system"))
    data_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data"))
    
    # Input paths
    curriculum_pdfs: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/raw/curriculum_pdfs"))
    skills_dir: Path = field(default_factory=lambda: Path("/mnt/skills"))
    templates_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/templates"))
    
    # Output paths
    outputs_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/outputs"))
    html_output: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/outputs/html"))
    reports_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/outputs/reports"))
    
    # Intermediate paths
    processed_data: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/processed"))
    embeddings_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/embeddings"))
    cache_dir: Path = field(default_factory=lambda: Path("/home/claude/cbe-generation-system/data/cache"))
    
    def create_directories(self):
        """Create all necessary directories"""
        for attr_name, path in self.__dict__.items():
            if isinstance(path, Path):
                path.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created: {path}")


@dataclass
class Config:
    """Master configuration object for entire system"""
    
    api: APIConfig = field(default_factory=APIConfig)
    spark: SparkConfig = field(default_factory=SparkConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    vectordb: VectorDBConfig = field(default_factory=VectorDBConfig)
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Config':
        """Load configuration from YAML file"""
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        return cls(
            api=APIConfig(**config_dict.get('api', {})),
            spark=SparkConfig(**config_dict.get('spark', {})),
            embedding=EmbeddingConfig(**config_dict.get('embedding', {})),
            vectordb=VectorDBConfig(**config_dict.get('vectordb', {})),
            generation=GenerationConfig(**config_dict.get('generation', {})),
            monitoring=MonitoringConfig(**config_dict.get('monitoring', {})),
            paths=PathConfig()
        )
    
    def to_yaml(self, yaml_path: str):
        """Save configuration to YAML file"""
        config_dict = {
            'api': {k: v for k, v in self.api.__dict__.items() if k != 'pricing'},
            'spark': self.spark.__dict__,
            'embedding': self.embedding.__dict__,
            'vectordb': self.vectordb.__dict__,
            'generation': self.generation.__dict__,
            'monitoring': self.monitoring.__dict__,
            'paths': {k: str(v) for k, v in self.paths.__dict__.items()}
        }
        
        with open(yaml_path, 'w') as f:
            yaml.dump(config_dict, f, default_flow_style=False, indent=2)
    
    def validate(self) -> bool:
        """Validate all configurations"""
        print("🔍 Validating configuration...")
        self.api.validate()
        self.paths.create_directories()
        print("✅ Configuration validated successfully")
        return True
    
    def print_summary(self):
        """Print comprehensive configuration summary"""
        print("\n" + "="*80)
        print("CBE LESSON PLAN GENERATION SYSTEM - CONFIGURATION")
        print("="*80)
        
        print(f"\n📊 API Configuration:")
        print(f"   Claude: {self.api.claude_model} (Rate: {self.api.claude_rpm} req/min)")
        print(f"   OpenAI: {self.api.gpt_model} (Rate: {self.api.openai_rpm} req/min)")
        print(f"   Gemini: {self.api.gemini_model} (Rate: {self.api.gemini_rpm} req/min)")
        
        print(f"\n⚡ Spark Configuration:")
        print(f"   App: {self.spark.app_name}")
        print(f"   Driver Memory: {self.spark.driver_memory}")
        print(f"   Executor Memory: {self.spark.executor_memory}")
        print(f"   Executor Cores: {self.spark.executor_cores}")
        print(f"   Parallelism: {self.spark.default_parallelism}")
        print(f"   GPU Enabled: {self.spark.gpu_enabled}")
        
        print(f"\n🧠 Embedding Configuration:")
        print(f"   Model: {self.embedding.model_name}")
        print(f"   Dimension: {self.embedding.model_dimension}")
        print(f"   Batch Size: {self.embedding.batch_size}")
        print(f"   Device: {self.embedding.device}")
        
        print(f"\n💾 Vector DB Configuration:")
        print(f"   Collection: {self.vectordb.collection_name}")
        print(f"   Persist Dir: {self.vectordb.persist_directory}")
        print(f"   Distance: {self.vectordb.distance_metric}")
        
        print(f"\n🎯 Generation Pipeline:")
        print(f"   Draft Model: {'Gemini' if self.generation.use_gemini_for_drafts else 'Disabled'}")
        print(f"   Structure Model: {'GPT-5' if self.generation.use_gpt5_for_structure else 'Disabled'}")
        print(f"   Polish Model: {'Claude' if self.generation.use_claude_for_polish else 'Disabled'}")
        print(f"   Polish %: {self.generation.polish_percentage*100:.0f}%")
        print(f"   Quality Threshold: {self.generation.min_quality_score}")
        
        print(f"\n📈 Monitoring:")
        print(f"   Prometheus: {'Enabled' if self.monitoring.enable_prometheus else 'Disabled'} (:{self.monitoring.prometheus_port})")
        print(f"   Logging: {self.monitoring.log_level}")
        print(f"   Cost Tracking: {'Enabled' if self.monitoring.enable_cost_tracking else 'Disabled'}")
        
        print(f"\n📁 Key Paths:")
        print(f"   Project Root: {self.paths.project_root}")
        print(f"   Curriculum PDFs: {self.paths.curriculum_pdfs}")
        print(f"   HTML Output: {self.paths.html_output}")
        print(f"   Reports: {self.paths.reports_dir}")
        
        print("="*80 + "\n")


# Create default configuration instance
default_config = Config()


if __name__ == "__main__":
    # Test configuration
    config = Config()
    
    try:
        config.validate()
        config.print_summary()
        
        # Save to YAML
        yaml_path = "/home/claude/cbe-generation-system/config/config.yaml"
        config.to_yaml(yaml_path)
        print(f"✅ Configuration saved to {yaml_path}")
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
