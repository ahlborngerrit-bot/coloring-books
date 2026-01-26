#!/usr/bin/env python3
"""
Generate professional covers for adult coloring books.
Suitable for Amazon KDP publishing.
"""

import os
import requests
import urllib.parse
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cover designs for each theme
COVER_DESIGNS = {
    "mandalas": {
        "title": "Mystical Mandalas",
        "subtitle": "Adult Coloring Book",
        "description": "elegant mandala patterns, intricate geometric designs, spiritual symbols, professional book cover layout, purple and gold color scheme, calming zen aesthetic"
    },
    "animals": {
        "title": "Enchanted Animals",
        "subtitle": "Adult Coloring Book",
        "description": "decorated animals with intricate patterns, lion owl elephant, vibrant nature colors, professional book cover design, whimsical artistic style"
    },
    "nature": {
        "title": "Botanical Gardens",
        "subtitle": "Adult Coloring Book",
        "description": "beautiful flowers and plants, tropical leaves, botanical illustration style, fresh green and floral colors, elegant book cover design"
    },
    "geometric": {
        "title": "Sacred Geometry",
        "subtitle": "Adult Coloring Book",
        "description": "complex geometric patterns, mathematical art, sacred geometry symbols, modern minimalist design, blue and gold color scheme"
    },
    "fantasy": {
        "title": "Fantasy Realms",
        "subtitle": "Adult Coloring Book",
        "description": "magical creatures, dragons and fairies, enchanted fantasy landscape, vibrant magical colors, dreamy whimsical book cover"
    },
    "patterns": {
        "title": "Relaxing Patterns",
        "subtitle": "Adult Coloring Book",
        "description": "abstract paisley and zentangle designs, decorative patterns, soothing art nouveau style, calming pastel colors, elegant cover"
    },
    "inspirational": {
        "title": "Mindful Words",
        "subtitle": "Adult Coloring Book",
        "description": "decorative inspirational words, peace love breathe, ornate lettering with floral elements, uplifting soft colors, motivational book cover"
    }
}


def generate_cover(theme: str, custom_title: str = None, custom_subtitle: str = None,
                  output_dir: Path = Path("output/covers")) -> bool:
    """Generate a professional book cover for a theme.

    Args:
        theme: Theme name (must be in COVER_DESIGNS)
        custom_title: Optional custom title (default: theme's title)
        custom_subtitle: Optional custom subtitle (default: "Adult Coloring Book")
        output_dir: Output directory for covers

    Returns:
        True if successful, False otherwise
    """

    if theme not in COVER_DESIGNS:
        logger.error(f"Unknown theme: {theme}")
        return False

    design = COVER_DESIGNS[theme]
    title = custom_title or design["title"]
    subtitle = custom_subtitle or design["subtitle"]

    # Cover prompt - professional and eye-catching
    prompt = f"""professional book cover design for "{title}" - {subtitle},
    featuring {design['description']},
    bold elegant typography, title prominently displayed,
    high quality commercial book cover, amazon KDP style,
    vertical portrait orientation, professional graphic design,
    print-ready quality, eye-catching and marketable"""

    encoded_prompt = urllib.parse.quote(prompt)

    # KDP cover dimensions
    # For 8.5x11 book: approximately 2550x3300 at 300 DPI
    # Using 1700x2200 for good quality at reasonable size
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1700&height=2200&nologo=true&model=flux"

    try:
        logger.info(f"Generating cover for theme: {theme}")
        logger.info(f"  Title: {title}")
        response = requests.get(url, timeout=180)

        if response.status_code == 200 and len(response.content) > 10000:
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save cover
            safe_title = title.replace(" ", "_").replace("'", "").replace(":", "")
            cover_path = output_dir / f"cover_{theme}_{safe_title}.png"
            cover_path.write_bytes(response.content)

            logger.info(f"✓ Cover saved: {cover_path.name}")
            logger.info(f"  Size: {len(response.content) / 1024:.1f} KB")
            return True
        else:
            logger.error(f"✗ Failed: HTTP {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"✗ Error: {e}")
        return False


def generate_all_covers(output_dir: Path = Path("output/covers")) -> dict:
    """Generate covers for all themes.

    Returns:
        Dictionary with results for each theme
    """

    results = {}
    themes = list(COVER_DESIGNS.keys())

    logger.info("=" * 60)
    logger.info(f"Generating {len(themes)} covers...")
    logger.info("=" * 60)

    for i, theme in enumerate(themes, 1):
        logger.info(f"\n[{i}/{len(themes)}] {theme}")
        success = generate_cover(theme, output_dir=output_dir)
        results[theme] = "success" if success else "failed"

        # Rate limiting
        if i < len(themes):
            time.sleep(3)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("COVER GENERATION COMPLETE")
    logger.info("=" * 60)

    success_count = sum(1 for v in results.values() if v == "success")
    logger.info(f"Success: {success_count}/{len(themes)}")

    for theme, status in results.items():
        symbol = "✓" if status == "success" else "✗"
        logger.info(f"  {symbol} {theme}: {COVER_DESIGNS[theme]['title']}")

    logger.info(f"\nCovers saved to: {output_dir.absolute()}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate professional covers for adult coloring books",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all covers
  python cover_generator.py --all

  # Generate cover for specific theme
  python cover_generator.py --theme mandalas

  # Generate with custom title
  python cover_generator.py --theme animals --title "My Amazing Animals"

  # Generate multiple themes
  python cover_generator.py --themes mandalas animals nature
        """
    )

    parser.add_argument("--all", action="store_true",
                       help="Generate covers for all themes")
    parser.add_argument("--theme", type=str, choices=list(COVER_DESIGNS.keys()),
                       help="Generate cover for specific theme")
    parser.add_argument("--themes", nargs="+", choices=list(COVER_DESIGNS.keys()),
                       help="Generate covers for multiple themes")
    parser.add_argument("--title", type=str,
                       help="Custom title for the book")
    parser.add_argument("--subtitle", type=str,
                       help="Custom subtitle (default: 'Adult Coloring Book')")
    parser.add_argument("--output", type=str, default="output/covers",
                       help="Output directory (default: output/covers)")
    parser.add_argument("--list-themes", action="store_true",
                       help="List available themes and exit")

    args = parser.parse_args()

    if args.list_themes:
        print("\nAvailable Themes:")
        print("=" * 60)
        for theme, design in COVER_DESIGNS.items():
            print(f"  {theme}")
            print(f"    Title: {design['title']}")
            print(f"    Style: {design['description'][:60]}...")
            print()
        return

    output_dir = Path(args.output)

    if args.all:
        generate_all_covers(output_dir)
    elif args.theme:
        generate_cover(args.theme, args.title, args.subtitle, output_dir)
    elif args.themes:
        for theme in args.themes:
            generate_cover(theme, args.title, args.subtitle, output_dir)
            time.sleep(3)  # Rate limiting
    else:
        parser.print_help()
        print("\nError: Specify --all, --theme, or --themes")


if __name__ == "__main__":
    main()
