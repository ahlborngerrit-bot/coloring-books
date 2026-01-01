# Adult Coloring Book Generator for Amazon KDP

AI-powered generator for creating print-ready adult coloring books.

## Features

- **7 Themes**: Mandalas, Animals, Nature, Geometric, Fantasy, Patterns, Inspirational
- **AI Line Art**: Uses Replicate API to generate intricate black & white designs
- **KDP Ready**: Creates print-ready PDFs at 300 DPI
- **Batch Mode**: Generate multiple books automatically

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# List available themes
python coloring_book_generator.py --list-themes

# Generate a 30-page mandala coloring book
python coloring_book_generator.py --theme mandalas --pages 30 --pdf

# Generate with custom title
python coloring_book_generator.py --theme animals --pages 40 --title "Wild Spirit Animals" --pdf
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

## Requirements

- Python 3.8+
- Replicate API token (set `REPLICATE_API_TOKEN` env var)
- ~$0.01-0.02 per page for image generation

## License

MIT
