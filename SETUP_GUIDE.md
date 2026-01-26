# Setup Guide for Enhanced Coloring Book Generator

## Quick Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
cd /mnt/e/projects/amazon/coloring-books

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test it works
python test_improved_lineart.py --quick
```

### Option 2: System-wide Installation (if permitted)

```bash
pip install --break-system-packages -r requirements.txt
```

### Option 3: Using pipx + System Packages

```bash
# Install OpenCV via system package manager
sudo apt install python3-opencv python3-numpy python3-pil

# Or on macOS
brew install opencv python-pillow

# Install reportlab separately
pip install --user reportlab
```

## Verify Installation

```bash
python3 -c "import cv2, numpy; print('OpenCV:', cv2.__version__, '| NumPy:', numpy.__version__)"
```

Should output something like:
```
OpenCV: 4.8.1 | NumPy: 1.24.3
```

## Dependencies Required

- **opencv-python** (≥4.8.0) - For line art edge detection
- **numpy** (≥1.24.0) - For image processing
- **Pillow** (≥9.0.0) - For image handling
- **reportlab** (≥4.0.0) - For PDF generation
- **requests** (≥2.28.0) - For API calls

## Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"

OpenCV isn't installed. Try:
```bash
pip install opencv-python
```

### "externally-managed-environment" error

Your system blocks pip installations. Use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Line art conversion is skipped

If you see "OpenCV not installed, skipping line art conversion", the generator will still work but won't produce clean line art. Install OpenCV to enable the enhanced processing.

## Testing Your Setup

```bash
# Quick test (generates 1 page)
python test_improved_lineart.py --quick

# Full comparison test (generates 6 pages total)
python test_improved_lineart.py --full

# Generate a real book
python coloring_book_generator.py --theme mandalas --pages 5 --force-lineart --pdf
```

## Next Steps

Once setup is complete:

1. Read [IMPROVEMENTS.md](IMPROVEMENTS.md) for usage guide
2. Run `python test_improved_lineart.py --quick` to test
3. Generate your first book with `python coloring_book_generator.py --help`

## API Keys (Optional)

The default backend (Pollinations.ai) is **completely free** and requires **no API keys**.

If you want to use alternate backends:

### HuggingFace (Free)
```bash
export HF_TOKEN="your_token_here"
```

### Replicate (Paid)
```bash
export REPLICATE_API_TOKEN="your_token_here"
```

Then use `--backend huggingface` or `--backend replicate` when running the generator.
