# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
# One-command setup (installs deps, verifies GPU, creates dirs)
./setup.sh

# Or manually:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# API keys (required before any generation run)
cp .env.example .env   # then fill in the three keys
# ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY
```

PyTorch with CUDA must be installed separately:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

## Running the Pipeline

```bash
# Test run (10 lessons)
source venv/bin/activate
python src/main_pipeline.py

# Production run — edit num_lessons in main_pipeline.py first
# Change: num_lessons = 2000
python src/main_pipeline.py

# Monitor logs
tail -f logs/cbe_generation.log

# Check Prometheus metrics (if enabled)
curl http://localhost:8000/metrics
```

## Architecture

The system has two distinct execution paths:

### 1. Full Spark Pipeline (`src/main_pipeline.py`)
The production path. `CBEProductionPipeline` runs a 6-stage orchestration:
- **Stage 1**: Spark parallel PDF parsing → text chunks
- **Stage 2**: GPU sentence-transformer embeddings (batch=256, CUDA)
- **Stage 3**: ChromaDB bulk insert with HNSW indexing
- **Stage 4**: Multi-model generation — Gemini drafts → GPT-5 structure → Claude polish (top 50%)
- **Stage 5**: Spark parallel quality validation
- **Stage 6**: HTML export

### 2. Standalone Generators (`src/production_generator_complete.py`, `src/generate_with_ai.py`, etc.)
Simpler scripts that call Claude directly without Spark. These use `ResourceManager` (reads `config/generation_config.yaml`) and `TemplateLoader` (reads `templates/cbe_lesson_template.md`). The top-level scripts (`generate_lesson.py`, `generate_four_new_lessons.py`, etc.) are wrappers around these.

### Key Modules
- `src/config.py` — Master `Config` dataclass with nested `APIConfig`, `SparkConfig`, `EmbeddingConfig`, `VectorDBConfig`, `GenerationConfig`, `MonitoringConfig`, `PathConfig`. Load from YAML via `Config.from_yaml()`.
- `src/api_clients/multi_model_client.py` — Thread-safe unified client for all three APIs; token-bucket rate limiting; automatic cost tracking per model.
- `src/resource_manager.py` — Resolves curriculum PDFs and template examples from `config/generation_config.yaml`.
- `src/template_loader.py` — Loads `templates/cbe_lesson_template.md` and builds system prompts for AI generation.

### Configuration
`config/generation_config.yaml` is the active config for standalone generators. The Spark pipeline uses `src/config.py` defaults or `config/config.yaml`. Key tunables:
- `generation.polish_percentage` — fraction of lessons Claude polishes (default 0.5)
- `embedding.batch_size` — reduce to 128 if CUDA OOM
- `api.claude_rpm` / `openai_rpm` / `gemini_rpm` — reduce if hitting rate limits
- `spark.default_parallelism` — increase for larger cluster runs

### Data Layout
```
data/raw/curriculum_pdfs/   ← place Kenya CBE PDFs here (Physics/Bio/Chem/Math, Gr10-13)
data/outputs/html/          ← generated lesson plan HTML files
data/vectordb/              ← ChromaDB persistent store
logs/                       ← pipeline logs
```

### Lesson Output Format
Each HTML file is a complete Kenya CBE lesson plan: Specific Learning Outcomes → 5-column implementation framework → Teacher Reflection → Formative Assessments → Differentiation Strategies. Sections are delimited `===SECTION A:...===` through `===SECTION E:===` in the raw AI output before HTML assembly.
