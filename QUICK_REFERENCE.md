# CBE GENERATION SYSTEM - QUICK REFERENCE

## ONE-PAGE CHEAT SHEET

### 🚀 SETUP (One Time Only)

```bash
cd /home/claude/cbe-generation-system
./setup.sh
nano .env  # Add API keys
```

### 📝 RUN PIPELINE

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run
python src/main_pipeline.py

# 3. Check output
ls data/outputs/html/
```

### 💰 COST CALCULATOR

**For N lessons:**
- Gemini Draft: N × $0.017
- GPT-5 Structure: N × $0.054
- Claude Polish: (N × 0.5) × $0.084
- **Total: N × $0.123**

**Examples:**
- 10 lessons: $1.23
- 100 lessons: $12.30
- 1,000 lessons: $123
- 2,000 lessons: $246

### ⚡ PERFORMANCE ESTIMATES

**For N lessons:**
- Time: N ÷ 700 hours
- GPU time: ~1 minute (fixed)
- API time: dominant factor

**Examples:**
- 10 lessons: ~1 minute
- 100 lessons: ~9 minutes
- 1,000 lessons: ~1.4 hours
- 2,000 lessons: ~2.8 hours

---

## 🔧 CONFIGURATION QUICK TWEAKS

### Speed Up Generation

```python
# In src/config.py
generation:
  use_claude_for_polish: false  # Skip polishing
  polish_percentage: 0.3         # OR reduce polishing
```

### Reduce Costs

```python
generation:
  use_gpt5_for_structure: false  # Use Gemini for everything
  use_claude_for_polish: false
```

### Improve Quality

```python
generation:
  polish_percentage: 1.0  # Polish all lessons
  use_claude_for_structure: true  # Use Claude for structure too
```

### Adjust Rate Limits

```python
api:
  claude_rpm: 30   # Reduce if hitting limits
  openai_rpm: 40
  gemini_rpm: 40
```

---

## 📊 MONITORING COMMANDS

### Check Cost While Running

```python
# In Python REPL during execution
from src.api_clients.multi_model_client import MultiModelClient
client = MultiModelClient(config)
client.print_cost_summary()
```

### View Logs

```bash
# Real-time log viewing
tail -f logs/cbe_generation.log

# Search for errors
grep ERROR logs/cbe_generation.log

# Search for cost info
grep "Cost:" logs/cbe_generation.log
```

### Check GPU Usage

```bash
# Real-time GPU monitoring
watch -n 1 nvidia-smi

# GPU memory usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

---

## 🐛 COMMON ERRORS & FIXES

### Error: "CUDA out of memory"

**Fix:**
```python
# Reduce batch size
embedding:
  batch_size: 128  # From 256
```

### Error: "Rate limit exceeded"

**Fix:**
```python
# Reduce RPM
api:
  claude_rpm: 30  # From 50
```

### Error: "No API key found"

**Fix:**
```bash
# Check .env file
cat .env
# Make sure keys are present and valid
```

### Error: "Spark memory error"

**Fix:**
```python
# Increase memory
spark:
  executor_memory: "64g"  # From 32g
```

---

## 📁 OUTPUT STRUCTURE

```
data/outputs/html/
├── Lesson_0001_lesson_0001.html
├── Lesson_0002_lesson_0002.html
├── Lesson_0003_lesson_0003.html
├── ...
└── Lesson_2000_lesson_2000.html

Each file contains:
- CBE-compliant HTML
- MS Word compatible
- Full lesson plan (3,000-5,000 words)
- Ready to use or further edit
```

---

## 🎯 KEY METRICS TO WATCH

### During Generation

```
✓ Embeddings/sec:     >1,000 (GPU working)
✓ API latency:        <5s per call
✓ Cost/lesson:        ~$0.12
✓ Quality score:      >0.85
✓ Validation rate:    >90%
```

### After Completion

```
✓ Total cost:         ~$246 for 2,000 lessons
✓ Total time:         2-3 hours
✓ Output files:       2,000 HTML files
✓ Quality avg:        0.90
✓ Manual edits:       <10% of lessons
```

---

## 💡 PRO TIPS

**1. Start Small**
- Test with 10 lessons first
- Verify quality before scaling
- Check costs are as expected

**2. Monitor Costs**
```python
# Set cost alert
monitoring:
  cost_alert_threshold: 100.0  # Alert at $100
```

**3. Use Selective Polishing**
- Polish only highest-priority lessons
- Save 50% on Claude costs

**4. Batch Similar Lessons**
- Group by subject for better caching
- Reuse curriculum context

**5. GPU Optimization**
```python
embedding:
  batch_size: 512  # Increase if GPU has memory
  use_mixed_precision: true  # Faster on modern GPUs
```

---

## 🔍 VALIDATION CHECKLIST

Before full production run, verify:

- [ ] All 3 API keys work (test with 1 lesson)
- [ ] GPU is accessible (check nvidia-smi)
- [ ] Spark runs without errors
- [ ] ChromaDB persists correctly
- [ ] Output HTML files look correct
- [ ] Costs match expectations (~$0.12/lesson)
- [ ] Quality scores acceptable (>0.85)

---

## 📞 NEED HELP?

1. **Check logs**: `logs/cbe_generation.log`
2. **Review README**: Complete docs in `README.md`
3. **Check configuration**: Verify `config/config.yaml`
4. **Test components**: Run individual stages
5. **Monitor costs**: Check cost tracker output

---

## ⚡ COMMAND CHEAT SHEET

```bash
# Setup
./setup.sh

# Activate
source venv/bin/activate

# Run
python src/main_pipeline.py

# Monitor
tail -f logs/cbe_generation.log
watch -n 1 nvidia-smi

# Check output
ls data/outputs/html/ | wc -l  # Count files
```

---

## 🎉 SUCCESS CRITERIA

Your system is production-ready when:

✅ Setup completes without errors  
✅ Test run (10 lessons) succeeds  
✅ Quality scores >0.85  
✅ Costs match estimates  
✅ GPU shows utilization  
✅ All 2,000 lessons generate successfully  
✅ Validation pass rate >90%  
✅ Total cost ~$246  
✅ Total time 2-3 hours  

**You're ready to generate the entire CBE curriculum!**

---

*Quick Reference v1.0 - January 25, 2026*
