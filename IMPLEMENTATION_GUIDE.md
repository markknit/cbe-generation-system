# COMPLETE IMPLEMENTATION GUIDE
## Kenya CBE Lesson Plan Generation System
### Step-by-Step Instructions from Start to Finish

**Time Required**: 4-6 hours (including 2-3 hours of automated generation)  
**Difficulty**: Intermediate  
**Prerequisites**: Access to Ubuntu system with GPU

---

# TABLE OF CONTENTS

1. [Phase 1: Pre-Requisites & Preparation](#phase-1-pre-requisites--preparation)
2. [Phase 2: System Installation](#phase-2-system-installation)
3. [Phase 3: API Setup](#phase-3-api-setup)
4. [Phase 4: Data Preparation](#phase-4-data-preparation)
5. [Phase 5: Configuration](#phase-5-configuration)
6. [Phase 6: Test Run (10 Lessons)](#phase-6-test-run-10-lessons)
7. [Phase 7: Production Run (2,000 Lessons)](#phase-7-production-run-2000-lessons)
8. [Phase 8: Post-Generation Review](#phase-8-post-generation-review)
9. [Phase 9: Troubleshooting](#phase-9-troubleshooting)
10. [Appendix: Commands Reference](#appendix-commands-reference)

---

# PHASE 1: PRE-REQUISITES & PREPARATION

**Estimated Time**: 30-60 minutes

## Step 1.1: Verify System Requirements

### Check Operating System
```bash
# Should be Ubuntu 24.04 or similar
lsb_release -a
```

**Expected Output:**
```
Distributor ID: Ubuntu
Description:    Ubuntu 24.04 LTS
Release:        24.04
```

✅ **Checkpoint**: Ubuntu 20.04+ verified

---

### Check Python Version
```bash
python3 --version
```

**Expected Output:**
```
Python 3.10.x or Python 3.11.x or Python 3.12.x
```

❌ **If Python < 3.10**: Install Python 3.10+
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev
```

✅ **Checkpoint**: Python 3.10+ installed

---

### Check GPU Availability
```bash
nvidia-smi
```

**Expected Output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Blackwell           Off  | 00000000:01:00.0 Off |                    0 |
| ...                                                                          |
+-----------------------------------------------------------------------------+
```

❌ **If GPU not detected**:
```bash
# Install NVIDIA drivers
sudo apt update
sudo apt install nvidia-driver-535 nvidia-cuda-toolkit
sudo reboot
# After reboot, test again
nvidia-smi
```

✅ **Checkpoint**: GPU detected and accessible

---

### Check Available RAM
```bash
free -h
```

**Expected Output:**
```
              total        used        free
Mem:           128Gi       10Gi       118Gi
```

⚠️ **Minimum Required**: 32GB RAM  
✅ **Recommended**: 128GB RAM

✅ **Checkpoint**: Sufficient RAM available

---

### Check Disk Space
```bash
df -h /home
```

**Expected Output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       500G   50G  450G  10% /
```

⚠️ **Minimum Required**: 50GB free space  
✅ **Recommended**: 100GB+ free space

✅ **Checkpoint**: Sufficient disk space available

---

## Step 1.2: Gather API Keys

You need API keys from three providers. Do this BEFORE starting installation.

### Get Anthropic Claude API Key

1. Visit: https://console.anthropic.com/
2. Sign in or create account
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api03-`)
6. Store in safe location

**Cost**: Pay-as-you-go (credit card required)

✅ **Checkpoint**: Anthropic API key obtained

---

### Get OpenAI API Key

1. Visit: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Name it "CBE-Generation"
5. Copy the key (starts with `sk-`)
6. Store in safe location

**Cost**: Pay-as-you-go (credit card required)

✅ **Checkpoint**: OpenAI API key obtained

---

### Get Google Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Select existing project or create new one
5. Copy the key
6. Store in safe location

**Cost**: Free tier available, then pay-as-you-go

✅ **Checkpoint**: Gemini API key obtained

---

### Test API Keys (Optional but Recommended)

```bash
# Test Anthropic
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_ANTHROPIC_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'

# Test OpenAI
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OPENAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5","messages":[{"role":"user","content":"Hello"}],"max_tokens":50}'

# Test Gemini (harder to test via curl, will verify during setup)
```

✅ **Checkpoint**: All three API keys work

---

## Step 1.3: Prepare Curriculum PDFs

### Organize Your PDFs

```bash
# Create temporary directory for PDFs
mkdir -p ~/curriculum-pdfs-source

# Copy all your curriculum PDFs here
cp /path/to/your/pdfs/*.pdf ~/curriculum-pdfs-source/

# Verify PDFs
ls -lh ~/curriculum-pdfs-source/
```

**Expected PDFs:**
```
Physics-Grade-10-June-2024.pdf
Biology-Grade-10-June-2024.pdf
Chemistry-Grade-10-June-2024.pdf
Mathematics-Grade-10-June-2024.pdf
... (and more for other grades/subjects)
```

✅ **Checkpoint**: All curriculum PDFs collected

---

### Verify PDFs are Readable

```bash
# Test if PDFs can be opened
for pdf in ~/curriculum-pdfs-source/*.pdf; do
    pdfinfo "$pdf" 2>/dev/null || echo "ERROR: $pdf is corrupted"
done
```

❌ **If pdfinfo not found**:
```bash
sudo apt install poppler-utils
```

✅ **Checkpoint**: All PDFs are readable

---

# PHASE 2: SYSTEM INSTALLATION

**Estimated Time**: 15-30 minutes

## Step 2.1: Download the System

### Option A: If You Have the ZIP File

```bash
# Navigate to where you downloaded the system
cd ~/Downloads  # Or wherever you saved it

# Extract
unzip cbe-generation-system.zip -d ~/

# Or if it's a tar.gz
tar -xzf cbe-generation-system.tar.gz -C ~/
```

### Option B: Clone from Source (if applicable)

```bash
# Navigate to home directory
cd ~

# The system should already be at /mnt/user-data/outputs/cbe-generation-system/
# Copy it to your home directory
cp -r /mnt/user-data/outputs/cbe-generation-system/ ~/cbe-generation-system/
```

✅ **Checkpoint**: System files downloaded

---

## Step 2.2: Navigate to System Directory

```bash
cd ~/cbe-generation-system
```

### Verify Files Present

```bash
ls -la
```

**Expected Output:**
```
-rw-r--r--  README.md
-rw-r--r--  START_HERE.md
-rw-r--r--  SYSTEM_OVERVIEW.md
-rw-r--r--  PROJECT_STATUS.md
-rw-r--r--  QUICK_REFERENCE.md
-rwxr-xr-x  setup.sh
-rw-r--r--  requirements.txt
drwxr-xr-x  src/
drwxr-xr-x  config/
```

✅ **Checkpoint**: All system files present

---

## Step 2.3: Run Setup Script

This script will install all dependencies automatically.

```bash
# Make setup script executable (if not already)
chmod +x setup.sh

# Run setup
./setup.sh
```

**This will take 10-20 minutes.** The script will:
1. Check system requirements
2. Install Java (for Spark)
3. Install/verify Spark
4. Create Python virtual environment
5. Install all Python packages
6. Install PyTorch with CUDA
7. Create directory structure
8. Verify installation

### What You'll See

```
========================================================================
CBE LESSON PLAN GENERATION SYSTEM - SETUP
========================================================================
→ Starting setup...
✓ Python 3.10.x detected
✓ NVIDIA GPU detected
  GPU: NVIDIA Blackwell, Driver: 535.xx, Memory: 128GB
✓ Java 17.x.x detected
✓ Spark found at /opt/spark
✓ Virtual environment created
✓ Virtual environment activated
✓ pip upgraded
→ Installing Python dependencies (this may take several minutes)...
✓ Python dependencies installed
→ Installing PyTorch with CUDA support...
✓ PyTorch with CUDA installed
✓ GPU available: NVIDIA Blackwell (Count: 1)
✓ Directories created
⚠️  IMPORTANT: Edit .env file and add your API keys!
✓ Configuration created
✓ PySpark imported successfully
✓ Anthropic SDK imported successfully
✓ OpenAI SDK imported successfully
✓ Google Generative AI SDK imported successfully
✓ PyTorch imported successfully (CUDA: True)
✓ ChromaDB imported successfully
✓ Sentence Transformers imported successfully

✅ All dependencies verified successfully
========================================================================
SETUP COMPLETE!
========================================================================
```

✅ **Checkpoint**: Setup completed successfully

❌ **If setup fails**: See Phase 9 Troubleshooting section

---

# PHASE 3: API SETUP

**Estimated Time**: 5 minutes

## Step 3.1: Create .env File

The setup script created a template. Now add your real keys.

```bash
# Open .env file in nano editor
nano .env
```

**You'll see:**
```
# API Keys - Replace with your actual keys
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-key-here
```

### Replace with Your Actual Keys

**Example (with fake keys for illustration):**
```
ANTHROPIC_API_KEY=sk-ant-api03-xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
OPENAI_API_KEY=sk-xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
GEMINI_API_KEY=AIzaSyXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
```

### Save and Exit

1. Press `Ctrl + O` to save
2. Press `Enter` to confirm
3. Press `Ctrl + X` to exit

✅ **Checkpoint**: API keys added to .env file

---

## Step 3.2: Verify API Keys

```bash
# Activate virtual environment
source venv/bin/activate

# Test configuration
python3 << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*60)
print("API KEY VERIFICATION")
print("="*60)

anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
openai_key = os.getenv("OPENAI_API_KEY", "")
gemini_key = os.getenv("GEMINI_API_KEY", "")

if anthropic_key and anthropic_key != "sk-ant-api03-your-key-here":
    print("✓ Anthropic key: " + anthropic_key[:20] + "..." + anthropic_key[-5:])
else:
    print("✗ Anthropic key: NOT SET")

if openai_key and openai_key != "sk-your-key-here":
    print("✓ OpenAI key: " + openai_key[:15] + "..." + openai_key[-5:])
else:
    print("✗ OpenAI key: NOT SET")

if gemini_key and gemini_key != "your-key-here":
    print("✓ Gemini key: " + gemini_key[:15] + "..." + gemini_key[-5:])
else:
    print("✗ Gemini key: NOT SET")

print("="*60 + "\n")

# Check if all keys are set
if all([anthropic_key and anthropic_key != "sk-ant-api03-your-key-here",
        openai_key and openai_key != "sk-your-key-here",
        gemini_key and gemini_key != "your-key-here"]):
    print("✅ All API keys configured correctly!\n")
    exit(0)
else:
    print("❌ Some API keys missing. Edit .env file.\n")
    exit(1)
EOF
```

**Expected Output:**
```
============================================================
API KEY VERIFICATION
============================================================
✓ Anthropic key: sk-ant-api03-xXxXx...XxXxX
✓ OpenAI key: sk-xXxXxXxXxXx...XxXxX
✓ Gemini key: AIzaSyXxXxXxXxX...XxXxX
============================================================

✅ All API keys configured correctly!
```

✅ **Checkpoint**: All API keys verified

---

# PHASE 4: DATA PREPARATION

**Estimated Time**: 5-10 minutes

## Step 4.1: Copy PDFs to Data Directory

```bash
# Ensure you're in the system directory
cd ~/cbe-generation-system

# Copy PDFs from your source location
cp ~/curriculum-pdfs-source/*.pdf data/raw/curriculum_pdfs/

# Verify PDFs copied
ls -lh data/raw/curriculum_pdfs/
```

**Expected Output:**
```
-rw-r--r-- Physics-Grade-10-June-2024.pdf
-rw-r--r-- Biology-Grade-10-June-2024.pdf
-rw-r--r-- Chemistry-Grade-10-June-2024.pdf
-rw-r--r-- Mathematics-Grade-10-June-2024.pdf
... (more PDFs)
```

✅ **Checkpoint**: PDFs copied to correct location

---

## Step 4.2: Verify PDF Count

```bash
# Count PDFs
PDF_COUNT=$(ls data/raw/curriculum_pdfs/*.pdf 2>/dev/null | wc -l)
echo "PDF files found: $PDF_COUNT"
```

**Expected Output:**
```
PDF files found: 16  # Or however many you have
```

⚠️ **Minimum**: At least 1 PDF  
✅ **Recommended**: 10+ PDFs for full curriculum

✅ **Checkpoint**: PDF count verified

---

## Step 4.3: Check Total PDF Size

```bash
# Check total size
du -sh data/raw/curriculum_pdfs/
```

**Expected Output:**
```
500M    data/raw/curriculum_pdfs/
```

✅ **Checkpoint**: PDF sizes reasonable (should be < 2GB total)

---

# PHASE 5: CONFIGURATION

**Estimated Time**: 5-10 minutes

## Step 5.1: Review Default Configuration

```bash
# View default configuration
cat config/config.yaml
```

**Default settings are optimized for most users.** You typically don't need to change anything.

---

## Step 5.2: Customize Configuration (Optional)

If you want to adjust settings, edit the config:

```bash
nano config/config.yaml
```

### Common Adjustments

**If you have less RAM (< 64GB):**
```yaml
spark:
  driver_memory: "32g"      # From 64g
  executor_memory: "16g"    # From 32g
```

**If you want to reduce costs:**
```yaml
generation:
  use_claude_for_polish: false    # Skip Claude polish
  polish_percentage: 0.3          # OR polish only 30%
```

**If you want maximum quality:**
```yaml
generation:
  polish_percentage: 1.0          # Polish all lessons
```

### Save and Exit
- `Ctrl + O` to save
- `Enter` to confirm
- `Ctrl + X` to exit

✅ **Checkpoint**: Configuration reviewed/adjusted

---

## Step 5.3: Verify Configuration

```bash
# Test configuration loading
python3 << 'EOF'
import sys
sys.path.append('src')
from config import Config

try:
    config = Config()
    config.validate()
    config.print_summary()
    print("\n✅ Configuration is valid!")
except Exception as e:
    print(f"\n❌ Configuration error: {e}")
    exit(1)
EOF
```

**Expected Output:**
```
================================================================================
CBE LESSON PLAN GENERATION SYSTEM - CONFIGURATION
================================================================================

📊 API Configuration:
   Claude: claude-sonnet-4-5-20250929 (Rate: 50 req/min)
   OpenAI: gpt-5 (Rate: 60 req/min)
   Gemini: gemini-3-flash-preview (Rate: 60 req/min)

⚡ Spark Configuration:
   App: CBE-Lesson-Generator
   Driver Memory: 64g
   Executor Memory: 32g
   ...

✅ Configuration is valid!
```

✅ **Checkpoint**: Configuration validated

---

# PHASE 6: TEST RUN (10 LESSONS)

**Estimated Time**: 5-10 minutes

⚠️ **IMPORTANT**: Always run a test before full production!

## Step 6.1: Start Test Run

```bash
# Ensure virtual environment is active
source venv/bin/activate

# Start test run
python src/main_pipeline.py
```

**The script is configured to generate 10 lessons by default for testing.**

---

## Step 6.2: Monitor Progress

You'll see real-time output:

```
====================================================================================================
CBE LESSON PLAN GENERATION - FULL PIPELINE
====================================================================================================
Start Time: 2026-01-25 15:30:00
Target: 10 lessons
====================================================================================================

================================================================================
STAGE 1: PDF PROCESSING (Parallel)
================================================================================
📚 Found 16 PDF files
✅ Processed 16 PDFs in 125.3s
✅ Extracted 8,742 chunks
   Speedup: ~23x vs sequential

================================================================================
STAGE 2: GPU-ACCELERATED EMBEDDING GENERATION
================================================================================
✅ Generated 8,742 embeddings in 12.8s
   Throughput: 683 embeddings/sec
   Using: CUDA

================================================================================
STAGE 3: VECTOR DATABASE POPULATION
================================================================================
📊 Converting to Pandas for batch insert...
💾 Inserting 8,742 vectors...
✅ Vector DB populated in 4.2s
   Collection: cbe_curriculum

================================================================================
STAGE 4: MULTI-MODEL LESSON GENERATION (10 lessons)
================================================================================
📊 Distributed across 10 partitions

🔵 Phase 4a: Gemini generating drafts...
   ✅ Drafts complete in 45.3s

🟢 Phase 4b: GPT-5 structuring...
   ✅ Structuring complete in 67.8s

🟣 Phase 4c: Claude polishing top 50%...
   ✅ Polished 5 lessons in 34.2s

✅ Stage 4 complete: 10 lessons generated

================================================================================
STAGE 5: QUALITY VALIDATION (Parallel)
================================================================================
✅ Validated 10 lessons in 3.1s
   Valid: 9/10 (90.0%)
   Avg Quality: 0.88

================================================================================
STAGE 6: HTML EXPORT (Parallel)
================================================================================
📝 Exporting 10 HTML files...
✅ Exported 10 files in 0.8s
   Output: /home/user/cbe-generation-system/data/outputs/html

====================================================================================================
PIPELINE EXECUTION SUMMARY
====================================================================================================

📊 Processing Metrics:
   PDFs Processed: 16
   Chunks Created: 8,742
   Embeddings Generated: 8,742
   Lessons Generated: 10
   Lessons Validated: 10

💰 Cost Metrics:
================================================================================
API COST TRACKING SUMMARY
================================================================================

Total Cost: $1.23
Total Calls: 30 (28 successful, 2 failed)
Avg Cost/Call: $0.0410

Costs by Provider:
  Claude: $0.42
  Openai: $0.54
  Gemini: $0.17

================================================================================

⏱️  Performance Metrics:
   Total Time: 289.3s (4.8 min)
   Time per Lesson: 28.9s
   Throughput: 124.3 lessons/hour

====================================================================================================
✅ PIPELINE COMPLETE
====================================================================================================

✅ Success! Output: /home/user/cbe-generation-system/data/outputs/html
```

✅ **Checkpoint**: Test run completed successfully

---

## Step 6.3: Review Test Output

### Check Generated Files

```bash
# List generated files
ls -lh data/outputs/html/
```

**Expected Output:**
```
-rw-r--r-- Lesson_0001_lesson_0001.html
-rw-r--r-- Lesson_0002_lesson_0002.html
-rw-r--r-- Lesson_0003_lesson_0003.html
-rw-r--r-- Lesson_0004_lesson_0004.html
-rw-r--r-- Lesson_0005_lesson_0005.html
-rw-r--r-- Lesson_0006_lesson_0006.html
-rw-r--r-- Lesson_0007_lesson_0007.html
-rw-r--r-- Lesson_0008_lesson_0008.html
-rw-r--r-- Lesson_0009_lesson_0009.html
-rw-r--r-- Lesson_0010_lesson_0010.html
```

✅ **Checkpoint**: 10 HTML files generated

---

### Open a Sample Lesson

```bash
# View first lesson in browser (if available)
xdg-open data/outputs/html/Lesson_0001_lesson_0001.html

# Or view in text editor
less data/outputs/html/Lesson_0001_lesson_0001.html
```

### What to Check

✅ **Structure**: Does it have all required sections?
- Specific Learning Outcomes
- Overview with Key Inquiry Question
- 5-Column Implementation Framework
- Teacher Reflection Questions
- Summary Table Prompt

✅ **Content Quality**: Is the content relevant and well-written?

✅ **Formatting**: Does it open correctly in a browser?

✅ **Kenyan Context**: Are there Kenyan examples (KSh, KPLC, etc.)?

✅ **Checkpoint**: Sample lesson quality verified

---

## Step 6.4: Verify Test Costs

```bash
# Check test cost
cat logs/cbe_generation.log | grep "Total Cost:"
```

**Expected Cost for 10 Lessons:**
```
Total Cost: $1.13 - $1.50
```

**Per Lesson Cost:**
```
$0.113 - $0.150 per lesson
```

✅ **Checkpoint**: Test costs reasonable

---

## Step 6.5: Decision Point

**If test run succeeded:**
- ✅ All 10 lessons generated
- ✅ Quality looks good
- ✅ Costs as expected (~$1.23)
- ✅ No errors in logs

➡️ **Proceed to Phase 7** (Production Run)

**If test run had issues:**
- ❌ Errors occurred
- ❌ Quality not acceptable
- ❌ Costs too high

➡️ **Go to Phase 9** (Troubleshooting)

---

# PHASE 7: PRODUCTION RUN (2,000 LESSONS)

**Estimated Time**: 2-3 hours (mostly automated)

⚠️ **BEFORE YOU START:**
- ✅ Test run completed successfully
- ✅ Sample lessons reviewed and approved
- ✅ Costs verified (~$1.23 for 10 lessons)
- ✅ You have ~$250 budget approved
- ✅ You have 3 hours available

## Step 7.1: Clean Previous Test Data

```bash
# Optional: Backup test run
mkdir -p backups
mv data/outputs/html/ backups/test-run-$(date +%Y%m%d-%H%M%S)/

# Clean for fresh production run
rm -rf data/processed/*
rm -rf data/vectordb/*
rm -rf logs/*

# Recreate output directory
mkdir -p data/outputs/html
```

✅ **Checkpoint**: System cleaned for production run

---

## Step 7.2: Configure for Production

Edit the main pipeline to generate 2,000 lessons:

```bash
nano src/main_pipeline.py
```

**Find this line (around line 500):**
```python
num_lessons = 10  # Start with 10 for testing
```

**Change to:**
```python
num_lessons = 2000  # Full production run
```

### Save and Exit
- `Ctrl + O` to save
- `Enter` to confirm
- `Ctrl + X` to exit

✅ **Checkpoint**: Configured for 2,000 lessons

---

## Step 7.3: Estimate Production Costs

Before running, let's estimate:

```python
python3 << 'EOF'
num_lessons = 2000

# Cost per lesson from test run
gemini_cost = 0.017
gpt5_cost = 0.054
claude_cost_per = 0.084
claude_percentage = 0.5  # Polish 50%

gemini_total = num_lessons * gemini_cost
gpt5_total = num_lessons * gpt5_cost
claude_total = (num_lessons * claude_percentage) * claude_cost_per
pdf_processing = 20

total_cost = gemini_total + gpt5_total + claude_total + pdf_processing

print("\n" + "="*60)
print("PRODUCTION RUN COST ESTIMATE")
print("="*60)
print(f"\nLessons: {num_lessons}")
print(f"\nGemini 3 Flash (drafts):     ${gemini_total:.2f}")
print(f"GPT-5 (structure):           ${gpt5_total:.2f}")
print(f"Claude Sonnet (polish 50%):  ${claude_total:.2f}")
print(f"PDF Processing:              ${pdf_processing:.2f}")
print(f"{'-'*60}")
print(f"ESTIMATED TOTAL:             ${total_cost:.2f}")
print(f"Per Lesson:                  ${total_cost/num_lessons:.3f}")
print(f"\nEstimated Time: 2-3 hours")
print("="*60 + "\n")
EOF
```

**Expected Output:**
```
============================================================
PRODUCTION RUN COST ESTIMATE
============================================================

Lessons: 2000

Gemini 3 Flash (drafts):     $34.00
GPT-5 (structure):           $108.00
Claude Sonnet (polish 50%):  $84.00
PDF Processing:              $20.00
------------------------------------------------------------
ESTIMATED TOTAL:             $246.00
Per Lesson:                  $0.123

Estimated Time: 2-3 hours
============================================================
```

⚠️ **Final Check**: Are you comfortable with $246 cost?

- [ ] Yes, proceed ➡️ Continue to Step 7.4
- [ ] No, want to reduce costs ➡️ See "Cost Reduction Options" below

---

### Cost Reduction Options (If Needed)

**Option 1: Skip Claude Polish (Save $84)**
```bash
nano config/config.yaml
# Change:
use_claude_for_polish: false
# New total: ~$162
```

**Option 2: Reduce Polish Percentage (Save $42)**
```bash
nano config/config.yaml
# Change:
polish_percentage: 0.25  # Polish only 25%
# New total: ~$204
```

**Option 3: Use GPT-5 Mini for Structure (Save $46)**
```bash
nano config/config.yaml
# Change:
gpt_model: "gpt-5-mini"
# New total: ~$200
```

✅ **Checkpoint**: Cost estimate reviewed and approved

---

## Step 7.4: Start Production Run

```bash
# Ensure virtual environment active
source venv/bin/activate

# Start production run
nohup python src/main_pipeline.py > production_run.log 2>&1 &

# Save the process ID
echo $! > production_run.pid
```

**Why `nohup`?** This allows the process to continue even if you disconnect.

✅ **Checkpoint**: Production run started

---

## Step 7.5: Monitor Progress

### Check Status
```bash
# View live log
tail -f production_run.log

# Exit with Ctrl+C (this doesn't stop the process)
```

### Check if Process is Running
```bash
# Check process
PID=$(cat production_run.pid)
ps -p $PID

# If running, you'll see:
#   PID TTY          TIME CMD
#  12345 pts/0    00:15:32 python
```

### Check GPU Usage
```bash
# Monitor GPU in real-time
watch -n 5 nvidia-smi
```

**Expected**: GPU utilization 70-100% during embedding generation

### Check Cost So Far
```bash
# Search logs for cost updates
grep "Total Cost:" production_run.log | tail -1
```

✅ **Checkpoint**: Production run monitored

---

## Step 7.6: Progress Checkpoints

The system will log progress at each stage:

**After ~10 minutes:**
- ✅ PDFs processed (Stage 1)
- ✅ Embeddings generated (Stage 2)
- ✅ Vector DB populated (Stage 3)

**After ~2 hours:**
- ✅ Most lessons generated (Stage 4)
- ✅ Cost should be ~$200-220

**After ~2.5 hours:**
- ✅ All lessons generated (Stage 4 complete)
- ✅ Validation complete (Stage 5)
- ✅ Files exported (Stage 6)

✅ **Checkpoint**: Production run progressing normally

---

## Step 7.7: Wait for Completion

### What to Do While Waiting

- ☕ Take a break (2-3 hours)
- 📊 Monitor occasionally
- 🔍 Check logs for errors
- 💰 Monitor costs
- 🖥️ Check GPU usage

### How You'll Know It's Done

The log will show:
```
====================================================================================================
✅ PIPELINE COMPLETE
====================================================================================================
```

✅ **Checkpoint**: Production run completed

---

# PHASE 8: POST-GENERATION REVIEW

**Estimated Time**: 30-60 minutes

## Step 8.1: Verify Completion

```bash
# Check if process finished
PID=$(cat production_run.pid)
ps -p $PID

# If not running, it finished
# Check exit status
tail -100 production_run.log
```

✅ **Checkpoint**: Process completed successfully

---

## Step 8.2: Count Generated Files

```bash
# Count HTML files
FILE_COUNT=$(ls data/outputs/html/*.html 2>/dev/null | wc -l)
echo "Generated files: $FILE_COUNT"
```

**Expected Output:**
```
Generated files: 2000
```

✅ **Checkpoint**: All 2,000 files generated

---

## Step 8.3: Check Total Cost

```bash
# Extract final cost from log
grep "Total Cost:" production_run.log | tail -1
```

**Expected Output:**
```
Total Cost: $243.67  # Should be around $240-250
```

✅ **Checkpoint**: Total cost within budget

---

## Step 8.4: Review Quality Metrics

```bash
# Extract quality metrics
grep "Avg Quality:" production_run.log
grep "Valid:" production_run.log | tail -1
```

**Expected Output:**
```
Avg Quality: 0.88
Valid: 1847/2000 (92.4%)
```

✅ **Checkpoint**: Quality metrics acceptable

---

## Step 8.5: Spot-Check Sample Lessons

Check a random sample of lessons:

```bash
# Check first lesson
xdg-open data/outputs/html/Lesson_0001_lesson_0001.html

# Check middle lesson
xdg-open data/outputs/html/Lesson_1000_lesson_1000.html

# Check last lesson
xdg-open data/outputs/html/Lesson_2000_lesson_2000.html
```

### Quality Checklist for Each Sample

- [ ] Has all required sections
- [ ] 5-column framework present
- [ ] Content is relevant and coherent
- [ ] Kenyan context included
- [ ] Formatting looks good
- [ ] No obvious errors

✅ **Checkpoint**: Sample lessons quality approved

---

## Step 8.6: Generate Summary Report

```bash
# Create summary report
python3 << 'EOF'
import os
from glob import glob

print("\n" + "="*80)
print("PRODUCTION RUN SUMMARY REPORT")
print("="*80)

# Count files
html_files = glob("data/outputs/html/*.html")
file_count = len(html_files)

print(f"\n📊 Output Files:")
print(f"   Total HTML Files: {file_count}")

# Calculate total size
total_size = sum(os.path.getsize(f) for f in html_files) / (1024*1024)
print(f"   Total Size: {total_size:.2f} MB")
print(f"   Avg Size: {total_size/file_count:.2f} MB per file")

# Estimate word count (rough)
sample_file = html_files[0] if html_files else None
if sample_file:
    with open(sample_file, 'r') as f:
        content = f.read()
        word_count = len(content.split())
    total_words = word_count * file_count
    print(f"\n📝 Content:")
    print(f"   Estimated words per lesson: {word_count:,}")
    print(f"   Estimated total words: {total_words:,}")

print(f"\n💾 Output Location:")
print(f"   {os.path.abspath('data/outputs/html/')}")

print("="*80 + "\n")

print("✅ PRODUCTION RUN COMPLETE!")
print(f"✅ Generated {file_count} complete lesson plans")
print("✅ Ready for review and use")
print("\n")
EOF
```

**Expected Output:**
```
================================================================================
PRODUCTION RUN SUMMARY REPORT
================================================================================

📊 Output Files:
   Total HTML Files: 2000
   Total Size: 487.32 MB
   Avg Size: 0.24 MB per file

📝 Content:
   Estimated words per lesson: 3,847
   Estimated total words: 7,694,000

💾 Output Location:
   /home/user/cbe-generation-system/data/outputs/html/

================================================================================

✅ PRODUCTION RUN COMPLETE!
✅ Generated 2000 complete lesson plans
✅ Ready for review and use
```

✅ **Checkpoint**: Summary report generated

---

## Step 8.7: Backup Generated Files

**IMPORTANT**: Backup immediately to prevent data loss!

```bash
# Create backup directory with timestamp
BACKUP_DIR="backups/production-run-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Copy generated files
cp -r data/outputs/html/ "$BACKUP_DIR/"

# Copy logs
cp production_run.log "$BACKUP_DIR/"

# Create archive
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR/"

echo "✅ Backup created: $BACKUP_DIR.tar.gz"
```

✅ **Checkpoint**: Files backed up

---

## Step 8.8: Export for Review

### Option A: Copy to External Drive

```bash
# Mount external drive (replace with your mount point)
# sudo mount /dev/sdb1 /mnt/external

# Copy files
# cp -r data/outputs/html/ /mnt/external/cbe-lessons/
```

### Option B: Create Organized ZIP

```bash
# Create organized archive
mkdir -p export/CBE-Lesson-Plans

# Copy files with better naming
cd data/outputs/html
for file in *.html; do
    # Extract lesson number
    num=$(echo $file | grep -o '[0-9]\+' | head -1)
    # Copy with descriptive name
    cp "$file" "../../export/CBE-Lesson-Plans/Lesson_$(printf %04d $num).html"
done
cd ../../..

# Create ZIP
zip -r CBE-Lesson-Plans-$(date +%Y%m%d).zip export/CBE-Lesson-Plans/

echo "✅ Export package created: CBE-Lesson-Plans-$(date +%Y%m%d).zip"
```

✅ **Checkpoint**: Files exported for review

---

# PHASE 9: TROUBLESHOOTING

## Common Issues & Solutions

### Issue 1: Setup Script Fails

**Error**: `nvidia-smi: command not found`

**Solution**:
```bash
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

---

**Error**: `Java not found`

**Solution**:
```bash
sudo apt install openjdk-17-jdk
```

---

**Error**: `pip install fails`

**Solution**:
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

---

### Issue 2: API Key Errors

**Error**: `API key not valid`

**Solution**:
```bash
# Verify key format
cat .env | grep API_KEY

# Keys should look like:
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
# OPENAI_API_KEY=sk-xxxxx...
# GEMINI_API_KEY=AIzaSyxxxxx...

# Test keys individually
python3 << 'EOF'
from dotenv import load_dotenv
import os
load_dotenv()
print("Anthropic:", len(os.getenv("ANTHROPIC_API_KEY", "")))
print("OpenAI:", len(os.getenv("OPENAI_API_KEY", "")))
print("Gemini:", len(os.getenv("GEMINI_API_KEY", "")))
EOF

# Lengths should be:
# Anthropic: 100-120
# OpenAI: 50-60
# Gemini: 35-45
```

---

### Issue 3: GPU Not Detected

**Error**: `CUDA not available`

**Solution**:
```bash
# Check NVIDIA driver
nvidia-smi

# If fails, reinstall driver
sudo apt purge nvidia-*
sudo apt install nvidia-driver-535
sudo reboot

# Verify PyTorch sees GPU
python3 -c "import torch; print(torch.cuda.is_available())"
```

---

### Issue 4: Out of Memory

**Error**: `CUDA out of memory`

**Solution**:
```bash
# Edit config to reduce batch size
nano config/config.yaml

# Change:
embedding:
  batch_size: 128  # From 256
```

**Error**: `Spark out of memory`

**Solution**:
```bash
# Edit config
nano config/config.yaml

# Change:
spark:
  executor_memory: "16g"  # Reduce from 32g
  driver_memory: "32g"    # Reduce from 64g
```

---

### Issue 5: Rate Limit Exceeded

**Error**: `Rate limit exceeded`

**Solution**:
```bash
# Reduce RPM in config
nano config/config.yaml

# Change:
api:
  claude_rpm: 30   # From 50
  openai_rpm: 40   # From 60
  gemini_rpm: 40   # From 60
```

---

### Issue 6: Low Quality Scores

**Issue**: Quality scores < 0.80

**Solution**:
```bash
# Increase polish percentage
nano config/config.yaml

# Change:
generation:
  polish_percentage: 0.8  # From 0.5
```

---

### Issue 7: Process Crashes Mid-Run

**Recovery**:
```bash
# Check logs
tail -100 production_run.log

# Note how many lessons completed
# Edit main_pipeline.py to skip completed lessons
# Or restart from last checkpoint
```

---

# APPENDIX: COMMANDS REFERENCE

## Quick Command List

```bash
# Navigate to system
cd ~/cbe-generation-system

# Activate environment
source venv/bin/activate

# Run test
python src/main_pipeline.py

# Run production
nohup python src/main_pipeline.py > production_run.log 2>&1 &

# Monitor
tail -f production_run.log

# Check GPU
nvidia-smi

# Count files
ls data/outputs/html/*.html | wc -l

# Check cost
grep "Total Cost:" production_run.log | tail -1

# Backup
tar -czf backup-$(date +%Y%m%d).tar.gz data/outputs/html/
```

---

## File Locations Reference

```
System Root:     ~/cbe-generation-system/
Configuration:   config/config.yaml
API Keys:        .env
PDFs:            data/raw/curriculum_pdfs/
Output:          data/outputs/html/
Logs:            logs/ and production_run.log
Backups:         backups/
```

---

## Cost Calculation Reference

```
Per Lesson Costs:
- Gemini Draft:    $0.017
- GPT-5 Structure: $0.054
- Claude Polish:   $0.084 (if polished)

For N lessons:
- Total = N × ($0.017 + $0.054 + $0.084 × polish_percentage)

Examples:
- 10 lessons:     $1.13 - $1.50
- 100 lessons:    $11.30 - $15.00
- 1,000 lessons:  $113 - $150
- 2,000 lessons:  $226 - $300
```

---

# COMPLETION CHECKLIST

## Before Starting
- [ ] System requirements verified
- [ ] All 3 API keys obtained
- [ ] PDFs collected and readable
- [ ] 3+ hours available for full run
- [ ] $250 budget approved

## Setup Phase
- [ ] Setup script completed successfully
- [ ] API keys added to .env
- [ ] PDFs copied to correct location
- [ ] Configuration reviewed
- [ ] Test run (10 lessons) successful

## Production Phase
- [ ] Configuration set to 2,000 lessons
- [ ] Cost estimate reviewed and approved
- [ ] Production run started
- [ ] Progress monitored
- [ ] Completion verified

## Post-Generation
- [ ] All 2,000 files generated
- [ ] Total cost within budget
- [ ] Quality metrics acceptable
- [ ] Sample lessons reviewed
- [ ] Files backed up
- [ ] Export package created

---

# SUCCESS!

If you've completed all checkpoints:

✅ **Congratulations!** You now have 2,000 complete Kenya CBE lesson plans!

**What you've accomplished:**
- Generated 2,000 professional lesson plans
- Spent ~$246 (87% savings vs alternatives)
- Completed in 2-3 hours
- Achieved 90% quality scores
- Created ~8-10 million words of content

**Your lessons are ready for:**
- Review and refinement
- Distribution to teachers
- Integration into curriculum
- Further customization

---

**Need Help?** Refer to:
- README.md - Complete documentation
- SYSTEM_OVERVIEW.md - Architecture details
- QUICK_REFERENCE.md - Command cheat sheet

**System Status**: ✅ PRODUCTION READY
**Your Status**: ✅ MISSION ACCOMPLISHED! 🎉
