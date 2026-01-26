# Quick Reference Guide

Complete command reference for the Adult Coloring Book Generator.

## 🚀 Quick Start (Most Common)

```bash
# Install dependencies
pip install -r requirements.txt

# Create a complete book ready for KDP
python complete_book_workflow.py --theme mandalas --pages 30
```

## 📚 Available Scripts

### 1. `coloring_book_generator.py` - Main Generator

Generate individual coloring books with full control.

```bash
# Basic usage
python coloring_book_generator.py --theme animals --pages 30 --force-lineart --pdf

# All options
python coloring_book_generator.py \
  --theme mandalas \
  --pages 40 \
  --title "Zen Mandalas" \
  --force-lineart \
  --lineart-method enhanced \
  --backend pollinations \
  --output output/ \
  --pdf
```

**Options:**
- `--theme`: mandalas, animals, nature, geometric, fantasy, patterns, inspirational
- `--pages`: Number of pages (default: 30)
- `--title`: Custom book title
- `--force-lineart`: Enable enhanced line art (RECOMMENDED)
- `--lineart-method`: enhanced (thick), standard (medium), detailed (fine)
- `--backend`: pollinations (free), huggingface (free), replicate (paid)
- `--output`: Output directory
- `--pdf`: Also create PDF
- `--list-themes`: Show all themes

### 2. `complete_book_workflow.py` - All-in-One

Creates interior + cover + PDF + publishing guide.

```bash
# Create complete book
python complete_book_workflow.py \
  --theme animals \
  --pages 50 \
  --title "Wild Animals" \
  --lineart-method enhanced
```

**What it does:**
1. Generates all interior pages
2. Creates PDF
3. Generates cover image
4. Shows KDP publishing guide

### 3. `batch_generator.py` - Multiple Books

Generate multiple books in one run.

```bash
# Generate all themes (7 books)
python batch_generator.py --all-themes --pages 30

# Generate specific themes
python batch_generator.py \
  --themes mandalas animals nature \
  --pages 40 \
  --force-lineart \
  --lineart-method enhanced
```

**Options:**
- `--all-themes`: Generate all 7 themes
- `--themes`: Specific themes (space-separated)
- `--pages`: Pages per book (default: 30)
- `--backend`: AI backend to use
- `--force-lineart`: Enable line art (default: True)
- `--no-lineart`: Disable line art
- `--lineart-method`: Quality level

### 4. `cover_generator.py` - Book Covers

Generate professional covers for your books.

```bash
# Generate all covers
python cover_generator.py --all

# Generate one cover
python cover_generator.py --theme mandalas

# Custom title
python cover_generator.py \
  --theme animals \
  --title "My Amazing Animals" \
  --subtitle "A Coloring Journey"
```

### 5. `test_improved_lineart.py` - Testing

Test the line art generation quality.

```bash
# Quick test (1 page)
python test_improved_lineart.py --quick

# Compare all methods (6 pages)
python test_improved_lineart.py --full
```

## 🎨 Themes Reference

| Theme | Name | Description | Difficulty |
|-------|------|-------------|------------|
| `mandalas` | Mystical Mandalas | Circular patterns, geometric | Medium |
| `animals` | Enchanted Animals | Decorated creatures | Easy-Medium |
| `nature` | Botanical Gardens | Flowers, plants | Medium |
| `geometric` | Sacred Geometry | Math patterns | Hard |
| `fantasy` | Fantasy Realms | Dragons, fairies | Medium |
| `patterns` | Relaxing Patterns | Abstract designs | Easy |
| `inspirational` | Mindful Words | Decorated text | Easy-Medium |

## 📐 Line Art Methods

| Method | Line Thickness | Best For | Use Case |
|--------|---------------|----------|----------|
| **enhanced** | 2-3 pixels | Easy coloring | Adult books, beginners |
| **standard** | 1-2 pixels | General use | Balanced detail |
| **detailed** | 1 pixel | Intricate | Advanced colorers |

## 🆓 Backends

| Backend | Cost | Speed | Quality | API Key Required |
|---------|------|-------|---------|------------------|
| **pollinations** | FREE | Fast | Good | ❌ No |
| **huggingface** | FREE | Medium | Good | ✅ Yes (HF_TOKEN) |
| **replicate** | ~$0.01/page | Fast | Best | ✅ Yes (REPLICATE_API_TOKEN) |

**Recommended:** Use `pollinations` (default) for free unlimited generation.

## 💡 Common Workflows

### Create One Book for KDP

```bash
python complete_book_workflow.py \
  --theme mandalas \
  --pages 30 \
  --lineart-method enhanced
```

### Test Before Full Generation

```bash
# Test with 5 pages first
python coloring_book_generator.py \
  --theme animals \
  --pages 5 \
  --force-lineart \
  --pdf
```

### Generate Multiple Books for Publishing

```bash
python batch_generator.py \
  --themes mandalas animals nature geometric \
  --pages 40 \
  --force-lineart
```

### Compare Line Art Quality

```bash
python test_improved_lineart.py --full
```

### Create Covers for Existing Books

```bash
python cover_generator.py --all
```

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install opencv-python numpy
```

### "externally-managed-environment"

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Line art not being applied

Make sure to use `--force-lineart` flag:
```bash
python coloring_book_generator.py --theme mandalas --pages 5 --force-lineart
```

### Generation is slow

The free backends (Pollinations, HuggingFace) can be slow during peak times. Try:
- Use fewer pages for testing
- Run during off-peak hours
- Consider Replicate backend (paid but faster)

### Images don't look like coloring book pages

Make sure you're using `--force-lineart`:
```bash
python coloring_book_generator.py --theme animals --force-lineart --lineart-method enhanced
```

## 📖 Documentation

- **[README.md](README.md)** - Overview and quick start
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Detailed usage guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation instructions
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and technical details
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - This file

## 🎯 Recommended Settings for Amazon KDP

```bash
python complete_book_workflow.py \
  --theme mandalas \
  --pages 30 \
  --lineart-method enhanced \
  --title "Zen Mandalas: Adult Coloring Book"
```

This creates:
- ✅ 30 coloring pages + title page
- ✅ 8.5 x 11 inches (KDP standard)
- ✅ 300 DPI (print quality)
- ✅ Pure black & white line art
- ✅ PDF ready for upload
- ✅ Cover image (optional)
- ✅ Publishing guidelines

## 📊 Page Count Recommendations

| Book Type | Recommended Pages | Price Range |
|-----------|------------------|-------------|
| **Quick Book** | 20-25 pages | $5.99-7.99 |
| **Standard Book** | 30-40 pages | $7.99-9.99 |
| **Premium Book** | 50-100 pages | $9.99-14.99 |

## 🚀 Production Workflow

1. **Test** (5 pages)
   ```bash
   python coloring_book_generator.py --theme animals --pages 5 --force-lineart --pdf
   ```

2. **Review** the output quality

3. **Generate Full Book** (30+ pages)
   ```bash
   python complete_book_workflow.py --theme animals --pages 30
   ```

4. **Create Cover** (if needed)
   ```bash
   python cover_generator.py --theme animals --title "My Book"
   ```

5. **Upload to KDP**
   - Follow the publishing guide printed by `complete_book_workflow.py`

## 📞 Support

For issues or questions:
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for installation help
- See [IMPROVEMENTS.md](IMPROVEMENTS.md) for usage examples
- File issues on GitHub

## 📄 License

MIT - Free for commercial use on Amazon KDP
