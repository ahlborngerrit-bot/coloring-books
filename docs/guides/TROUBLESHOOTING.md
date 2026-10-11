# Troubleshooting Guide

## Common Issues and Solutions

---

## ✅ RESOLVED ISSUES (Fixed in Latest Version)

### Issue: Images Too Small for Print Quality ✅ FIXED

**Symptom**: Generated images were only 768x768 pixels (2.56" x 2.56" at 300 DPI)

**Impact**: Not suitable for Amazon KDP printing (needs 8.5" x 11")

**Root Cause**:
- Pollinations.ai was generating images at default size (1024x1024)
- Images were being used at received resolution without upscaling

**Fix Applied**:
- Added automatic upscaling to 2550x3300 pixels (8.5" x 11" at 300 DPI)
- Implemented `upscale_to_print_quality()` function
- Uses LANCZOS4 interpolation for best quality
- Applied to all backends (Pollinations, HuggingFace, Replicate)
- Works with and without line art processing

**Verification**:
```python
from PIL import Image
img = Image.open('output/[book_name]/images/page_001.png')
print(f'Size: {img.size}')  # Should show (2550, 3300)
print(f'DPI: {img.info.get("dpi")}')  # Should show ~300
```

**Status**: ✅ All new generations include automatic upscaling

---

## 🔧 Current Troubleshooting

### 1. "ModuleNotFoundError: No module named 'cv2'"

**Symptom**: Error when running with `--force-lineart`

**Cause**: OpenCV not installed

**Solution**:
```bash
pip install --break-system-packages opencv-python numpy
```

**Verification**:
```bash
python3 -c "import cv2; print(cv2.__version__)"
```

**Workaround**: Run without `--force-lineart` flag (no line art processing)

---

### 2. "ModuleNotFoundError: No module named 'reportlab'"

**Symptom**: Error when using `--pdf` flag

**Cause**: ReportLab not installed

**Solution**:
```bash
pip install --break-system-packages reportlab Pillow
```

**Workaround**: Skip `--pdf` flag and manually create PDF later

---

### 3. "externally-managed-environment" Error

**Symptom**: pip refuses to install packages

**Cause**: System Python protection

**Solution 1** (Recommended - Virtual Environment):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solution 2** (System-wide):
```bash
pip install --break-system-packages -r requirements.txt
```

**Solution 3** (System packages):
```bash
sudo apt install python3-opencv python3-numpy python3-pil
pip install --user reportlab
```

---

### 4. Slow Generation Speed

**Symptom**: Takes long time to generate pages

**Possible Causes**:
1. **Pollinations.ai server load** (most common)
   - Peak times can be slower
   - Wait times: 5-60 seconds per page
   - **Solution**: Run during off-peak hours or be patient

2. **Network connection**
   - Check internet speed
   - **Solution**: Use stable connection

3. **Upscaling processing**
   - Each image is upscaled to 2550x3300
   - Takes ~5 seconds per page (normal)
   - **Status**: This is expected and necessary for print quality

**Expected Times**:
- Single page: 10-20 seconds total
- 30-page book: 5-10 minutes
- 50-page book: 10-15 minutes

---

### 5. "Line art conversion failed" Warning

**Symptom**: Warning in logs but page still generated

**Cause**: Edge detection encountered an issue

**Impact**: Page may not have perfect line art but is still usable

**Solutions**:
1. **Retry**: Generate again (may work better with different AI output)
2. **Try different method**: Use `--lineart-method standard` or `--lineart-method detailed`
3. **Check logs**: Look for specific error details

**Prevention**: Use stable OpenCV version (4.8.0+)

---

### 6. Images Have Gray Tones (Not Pure B&W)

**Symptom**: Generated images have shading or gray pixels

**Diagnosis**:
```python
from PIL import Image
import numpy as np

img = Image.open('page_001.png')
arr = np.array(img)
unique_values = len(np.unique(arr))
print(f'Unique values: {unique_values}')
# Should be 2 for pure B&W
```

**Possible Causes**:
1. **Line art processing disabled**
   - **Solution**: Add `--force-lineart` flag

2. **OpenCV not installed**
   - Line art processing automatically skipped
   - **Solution**: Install OpenCV

3. **Processing failed silently**
   - Check logs for warnings
   - **Solution**: Reinstall OpenCV or try different method

**Verification**: Open image in viewer - should be only pure black and pure white

---

### 7. PDF Too Large

**Symptom**: PDF file is very large (>100 MB)

**Cause**: High-resolution images not compressed

**Normal Sizes**:
- 30-page book: 2-5 MB
- 50-page book: 4-8 MB

**Solutions**:
1. **Use line art processing** (better compression):
   ```bash
   --force-lineart --lineart-method enhanced
   ```

2. **PDF is fine**: KDP accepts large PDFs, but upload may be slow

**Not Recommended**: Reducing resolution (will hurt print quality)

---

### 8. Themes Not Generating Expected Content

**Symptom**: Generated pages don't match theme description

**Cause**: AI interpretation varies

**Solutions**:
1. **Regenerate**: Try again (AI results vary)
2. **Adjust page count**: More pages = more variety
3. **Check theme**: Use `--list-themes` to see available themes

**Understanding AI Variation**:
- Each generation is unique
- Results depend on AI model's training
- Some variation is expected and normal

---

### 9. Cover Generation Issues

**Symptom**: Cover doesn't generate or looks wrong

**Possible Causes**:
1. **Pollinations.ai server issue**
   - **Solution**: Retry later

2. **Theme not recognized**
   - **Solution**: Check `cover_generator.py --list-themes`

3. **Network timeout**
   - Covers take longer (higher resolution)
   - **Solution**: Increase timeout or retry

**Workaround**: Create cover manually using KDP Cover Creator

---

### 10. "Unknown theme" Error

**Symptom**: Error when specifying theme

**Cause**: Theme name misspelled or doesn't exist

**Solution**:
```bash
# List all available themes
python3 coloring_book_generator.py --list-themes

# Use exact theme name
python3 coloring_book_generator.py --theme mandalas
```

**Available Themes**:
- mandalas
- animals
- nature
- geometric
- fantasy
- patterns
- inspirational

---

## 🔍 Diagnostic Commands

### Check Installation Status
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"
python3 -c "import numpy; print('NumPy:', numpy.__version__)"
python3 -c "from PIL import Image; print('Pillow: OK')"
python3 -c "from reportlab.pdfgen import canvas; print('ReportLab: OK')"
```

### Verify Image Quality
```python
from PIL import Image
import numpy as np

img = Image.open('output/[book]/images/page_001.png')

print('=== Image Quality Report ===')
print(f'Size: {img.size} pixels')
print(f'DPI: {img.info.get("dpi", "Not set")}')
print(f'Mode: {img.mode}')
print(f'Physical: {img.size[0]/300:.2f}" x {img.size[1]/300:.2f}"')

arr = np.array(img)
print(f'Unique values: {len(np.unique(arr))}')
print(f'Min/Max: {arr.min()}/{arr.max()}')

# Quality checks
if img.size[0] >= 2550 and img.size[1] >= 3300:
    print('✓ Size: PASS (print quality)')
else:
    print('✗ Size: FAIL (too small for print)')

if len(np.unique(arr)) == 2:
    print('✓ Binary: PASS (pure B&W)')
else:
    print(f'⚠ Binary: {len(np.unique(arr))} values (expected 2)')
```

### Test Generation
```bash
# Quick test (1 page)
python3 test_improved_lineart.py --quick

# Full test (compare all methods)
python3 test_improved_lineart.py --full
```

---

## 🚨 Critical Issues

### Issue: No Images Generated

**Check**:
1. Network connection
2. Pollinations.ai service status
3. Disk space
4. Permissions on output directory

**Debug**:
```bash
# Check disk space
df -h

# Check output directory
ls -la output/

# Check permissions
mkdir -p output/test
```

### Issue: Process Hangs

**Possible Causes**:
1. Network timeout waiting for AI
2. Processing very large image
3. System resource limits

**Solutions**:
```bash
# Kill hung process
Ctrl+C

# Check system resources
free -h
df -h

# Retry with smaller page count
python3 coloring_book_generator.py --theme mandalas --pages 1
```

---

## 📊 Performance Optimization

### Faster Generation

**Use Pollinations** (default, fastest free option):
```bash
python3 coloring_book_generator.py --backend pollinations
```

**Reduce Pages for Testing**:
```bash
# Test with 5 pages first
python3 coloring_book_generator.py --pages 5
```

**Batch Wisely**:
```bash
# Generate during off-peak hours
# Avoid generating 100+ pages at once
```

### Lower Quality for Testing

**Skip Line Art Processing** (faster testing):
```bash
python3 coloring_book_generator.py --theme mandalas --pages 3
# (No --force-lineart flag)
```

**Note**: Always use `--force-lineart` for final production books

---

## 🆘 Getting Help

### Before Asking for Help

1. **Check this guide** - Most issues covered here
2. **Run diagnostics** - Use commands above
3. **Check logs** - Look for ERROR or WARNING messages
4. **Try quick test** - `python3 test_improved_lineart.py --quick`

### When Reporting Issues

Include:
```bash
# System info
python3 --version
uname -a

# Dependency versions
python3 -c "import cv2; print('OpenCV:', cv2.__version__)"

# Command used
# Error message (full text)
# Log output

# Image diagnostics (if applicable)
```

### Documentation

- **README.md** - Overview
- **QUICK_REFERENCE.md** - Commands
- **IMPROVEMENTS.md** - Usage guide
- **SETUP_GUIDE.md** - Installation
- **TEST_RESULTS.md** - Quality verification
- **TROUBLESHOOTING.md** - This file

---

## ✅ Known Good Configuration

**Working Setup**:
```
OS: Ubuntu 22.04 / Debian 12 / macOS / WSL2
Python: 3.10-3.12
OpenCV: 4.8.0+
NumPy: 1.24.0+
Pillow: 9.0.0+
ReportLab: 4.0.0+
```

**Verified Commands**:
```bash
# Installation
pip install --break-system-packages opencv-python numpy Pillow reportlab

# Generation
python3 coloring_book_generator.py \
  --theme mandalas \
  --pages 30 \
  --force-lineart \
  --lineart-method enhanced \
  --pdf

# Testing
python3 test_improved_lineart.py --quick
```

---

## 📝 Change Log

### 2026-01-26
- ✅ Fixed: Image resolution too low for print
- ✅ Added: Automatic upscaling to 2550x3300 (8.5x11" @ 300 DPI)
- ✅ Added: DPI metadata to all generated images
- ✅ Applied: Upscaling to all backends (Pollinations, HuggingFace, Replicate)
- ✅ Verified: All test cases pass with print-quality output

---

*Last updated: 2026-01-26*
*Version: 2.0.1*
