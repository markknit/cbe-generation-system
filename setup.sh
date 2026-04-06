#!/bin/bash
# CBE Lesson Plan Generation System - Setup and Deployment Script
# Run this script to set up the complete environment

set -e  # Exit on error

echo "========================================================================"
echo "CBE LESSON PLAN GENERATION SYSTEM - SETUP"
echo "========================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "Do not run this script as root"
   exit 1
fi

print_info "Starting setup..."

# 1. Check Python version
print_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    print_success "Python $PYTHON_VERSION detected"
else
    print_error "Python 3.10+ required. Found: $PYTHON_VERSION"
    exit 1
fi

# 2. Check CUDA availability
print_info "Checking CUDA installation..."
if command -v nvidia-smi &> /dev/null; then
    print_success "NVIDIA GPU detected"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    print_error "NVIDIA GPU not detected. GPU acceleration will not be available."
    print_info "Install NVIDIA drivers: sudo apt install nvidia-driver-535"
fi

# 3. Check Java (required for Spark)
print_info "Checking Java installation..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -1 | cut -d'"' -f2)
    print_success "Java $JAVA_VERSION detected"
else
    print_error "Java not found. Installing OpenJDK 17..."
    sudo apt update
    sudo apt install -y openjdk-17-jdk
fi

# 4. Check Spark installation
print_info "Checking Spark installation..."
if [ -d "/opt/spark" ]; then
    print_success "Spark found at /opt/spark"
else
    print_info "Spark not found. Installing..."
    
    cd /tmp
    wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
    tar -xzf spark-3.5.0-bin-hadoop3.tgz
    sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
    
    # Add to PATH
    if ! grep -q "SPARK_HOME" ~/.bashrc; then
        echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc
        echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
    fi
    
    source ~/.bashrc
    print_success "Spark installed successfully"
fi

# 5. Create virtual environment
print_info "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# 6. Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# 7. Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip upgraded"

# 8. Install Python dependencies
print_info "Installing Python dependencies (this may take several minutes)..."
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

# 9. Install PyTorch with CUDA support
print_info "Installing PyTorch with CUDA support..."
if command -v nvidia-smi &> /dev/null; then
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 > /dev/null 2>&1
    print_success "PyTorch with CUDA installed"
else
    pip install torch torchvision torchaudio > /dev/null 2>&1
    print_success "PyTorch (CPU-only) installed"
fi

# 10. Verify CUDA availability in PyTorch
print_info "Verifying GPU availability in PyTorch..."
if python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
    GPU_COUNT=$(python -c "import torch; print(torch.cuda.device_count())")
    GPU_NAME=$(python -c "import torch; print(torch.cuda.get_device_name(0))")
    print_success "GPU available: $GPU_NAME (Count: $GPU_COUNT)"
else
    print_error "GPU not available in PyTorch. Will use CPU (slower)."
fi

# 11. Create directory structure
print_info "Creating directory structure..."
mkdir -p data/{raw/curriculum_pdfs,processed,embeddings,outputs/{html,reports},cache}
mkdir -p logs
mkdir -p config
mkdir -p data/spark-checkpoints
mkdir -p data/spark-temp
mkdir -p data/vectordb
print_success "Directories created"

# 12. Check for .env file
print_info "Checking for API credentials..."
if [ ! -f ".env" ]; then
    print_error ".env file not found"
    print_info "Creating .env template..."
    
    cat > .env << EOF
# API Keys - Replace with your actual keys
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
OPENAI_API_KEY=sk-your-key-here
GEMINI_API_KEY=your-key-here
EOF
    
    print_success ".env template created"
    print_error "⚠️  IMPORTANT: Edit .env file and add your API keys!"
    print_info "   1. Get Anthropic key: https://console.anthropic.com/"
    print_info "   2. Get OpenAI key: https://platform.openai.com/api-keys"
    print_info "   3. Get Gemini key: https://makersuite.google.com/app/apikey"
else
    print_success ".env file found"
fi

# 13. Create configuration file
print_info "Creating default configuration..."
python -c "
import sys
sys.path.append('src')
from config import Config

config = Config()
config.to_yaml('config/config.yaml')
print('Configuration saved to config/config.yaml')
" 2>/dev/null

if [ $? -eq 0 ]; then
    print_success "Configuration created"
else
    print_error "Failed to create configuration"
fi

# 14. Verify installation
print_info "Verifying installation..."

python << EOF
import sys
errors = []

# Check imports
try:
    import pyspark
    print("✓ PySpark imported successfully")
except ImportError as e:
    errors.append(f"PySpark import failed: {e}")

try:
    import anthropic
    print("✓ Anthropic SDK imported successfully")
except ImportError as e:
    errors.append(f"Anthropic SDK import failed: {e}")

try:
    import openai
    print("✓ OpenAI SDK imported successfully")
except ImportError as e:
    errors.append(f"OpenAI SDK import failed: {e}")

try:
    import google.generativeai
    print("✓ Google Generative AI SDK imported successfully")
except ImportError as e:
    errors.append(f"Google SDK import failed: {e}")

try:
    import torch
    print(f"✓ PyTorch imported successfully (CUDA: {torch.cuda.is_available()})")
except ImportError as e:
    errors.append(f"PyTorch import failed: {e}")

try:
    import chromadb
    print("✓ ChromaDB imported successfully")
except ImportError as e:
    errors.append(f"ChromaDB import failed: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("✓ Sentence Transformers imported successfully")
except ImportError as e:
    errors.append(f"Sentence Transformers import failed: {e}")

if errors:
    print("\n⚠️ Errors found:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)
else:
    print("\n✅ All dependencies verified successfully")
    sys.exit(0)
EOF

if [ $? -eq 0 ]; then
    print_success "Installation verification passed"
else
    print_error "Installation verification failed"
    exit 1
fi

# 15. Print summary
echo ""
echo "========================================================================"
echo "SETUP COMPLETE!"
echo "========================================================================"
echo ""
print_success "System is ready to use"
echo ""
echo "Next Steps:"
echo "  1. Edit .env file and add your API keys"
echo "  2. Place curriculum PDFs in: data/raw/curriculum_pdfs/"
echo "  3. Run test: python src/main_pipeline.py"
echo "  4. Check output: data/outputs/html/"
echo ""
echo "Quick Test:"
echo "  source venv/bin/activate"
echo "  python src/main_pipeline.py"
echo ""
echo "Documentation:"
echo "  README.md - Complete system documentation"
echo "  config/config.yaml - Configuration settings"
echo ""
echo "Monitoring:"
echo "  Logs: ./logs/"
echo "  Metrics: http://localhost:8000/metrics (when running)"
echo ""
echo "========================================================================"
echo ""

print_info "To activate environment in future sessions:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo ""

# Deactivate virtual environment
deactivate 2>/dev/null || true

print_success "Setup script completed successfully!"
