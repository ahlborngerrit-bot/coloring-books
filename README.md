# Adult Coloring Book Generator for Amazon KDP

AI-powered generator for creating **professional, print-ready** adult coloring books with **clean black-and-white line art**.

## ✨ NEW: Enhanced Line Art Quality

This generator now features **advanced edge detection** that produces genuine coloring book pages:
- ✅ **Pure black lines on white background** (no gray tones)
- ✅ **Thick, bold outlines** perfect for easy coloring
- ✅ **Professional print quality** at 300 DPI
- ✅ **100% FREE** using Pollinations.ai (no API keys!)

## Features

- **7 Family-Friendly Themes**: Mandalas, Animals, Nature, Geometric, Fantasy, Patterns, Inspirational
- **Enhanced Line Art Processing**: 3 quality levels (Enhanced, Standard, Detailed)
- **Multiple AI Backends**: Pollinations (free), HuggingFace (free), Replicate (paid)
- **KDP Ready**: Creates print-ready PDFs at 300 DPI
- **Batch Mode**: Generate multiple books automatically

## Quick Start

```bash
# Install dependencies (see SETUP_GUIDE.md for details)
pip install -r requirements.txt

# Quick test - generate 1 sample page
python test_improved_lineart.py --quick

# Generate a professional coloring book with enhanced line art
python coloring_book_generator.py \
  --theme mandalas \
  --pages 30 \
  --force-lineart \
  --lineart-method enhanced \
  --pdf

# List all available themes
python coloring_book_generator.py --list-themes
```

## Themes

| Theme | Description | Example Prompts |
|-------|-------------|-----------------|
| `mandalas` | Mystical Mandalas | Geometric, floral, celestial patterns |
| `animals` | Enchanted Animals | Decorated lions, owls, elephants, wolves |
| `nature` | Botanical Gardens | Flowers, forests, underwater scenes |
| `geometric` | Sacred Geometry | Tessellations, optical illusions, 3D patterns |
| `fantasy` | Fantasy Realms | Dragons, fairies, mermaids, unicorns |
| `patterns` | Relaxing Patterns | Paisley, zentangle, damask, art nouveau |
| `inspirational` | Mindful Words | Decorated text: BREATHE, PEACE, LOVE |

## KDP Specifications

- **Interior**: 8.5 x 11 inches (letter size)
- **Resolution**: 300 DPI
- **Format**: PDF
- **Paper**: White or cream (your choice at upload)

## Batch Generation

```bash
# Generate all themes
python batch_generator.py --all-themes --pages 30

# Generate specific themes
python batch_generator.py --themes mandalas animals nature --pages 40
```

## Output Structure

```
output/
└── Book_Title_YYYYMMDD_HHMMSS/
    ├── images/
    │   ├── page_001.png
    │   ├── page_002.png
    │   └── ...
    ├── metadata.json
    └── Book_Title.pdf
```

## Documentation

- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Complete usage guide and examples
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation instructions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and technical details

## Requirements

- Python 3.8+
- OpenCV 4.8+ (`opencv-python`)
- NumPy 1.24+
- Pillow 9.0+
- ReportLab 4.0+

**No API keys required!** The default backend (Pollinations.ai) is completely free.

Optional backends:
- **HuggingFace**: Free (rate limited) - Set `HF_TOKEN`
- **Replicate**: ~$0.01-0.02/page - Set `REPLICATE_API_TOKEN`

## What's New in v2.0

🎨 **Enhanced line art conversion** with professional edge detection
🆓 **100% free generation** using Pollinations.ai
📚 **Improved documentation** with detailed guides
🧹 **Family-friendly themes** only (removed controversial content)
⚙️ **Better CLI** with more options and control

See [CHANGELOG.md](CHANGELOG.md) for full details.

## License

MIT - Free for commercial use on Amazon KDP
