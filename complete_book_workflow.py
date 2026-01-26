#!/usr/bin/env python3
"""
Complete workflow for creating a ready-to-publish coloring book.
This script:
1. Generates the interior pages with enhanced line art
2. Creates a professional cover
3. Compiles everything into a PDF
4. Provides publishing guidelines
"""

import sys
import time
import logging
from pathlib import Path
from coloring_book_generator import ColoringBookGenerator, THEMES
from cover_generator import generate_cover

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_complete_book(theme: str, num_pages: int = 30, book_title: str = None,
                        lineart_method: str = "enhanced") -> dict:
    """Create a complete coloring book ready for publishing.

    Args:
        theme: Theme name (e.g., "mandalas", "animals")
        num_pages: Number of coloring pages
        book_title: Custom title (optional)
        lineart_method: Line art quality (enhanced, standard, detailed)

    Returns:
        Dictionary with paths to generated files
    """

    logger.info("=" * 70)
    logger.info("COMPLETE COLORING BOOK CREATION WORKFLOW")
    logger.info("=" * 70)
    logger.info(f"Theme: {theme}")
    logger.info(f"Pages: {num_pages}")
    logger.info(f"Line Art Method: {lineart_method}")
    logger.info("=" * 70)

    if theme not in THEMES:
        logger.error(f"Unknown theme: {theme}")
        return None

    theme_data = THEMES[theme]
    title = book_title or theme_data["name"]

    # Step 1: Generate interior pages
    logger.info("\n📖 STEP 1/3: Generating Interior Pages")
    logger.info("-" * 70)

    generator = ColoringBookGenerator(
        output_dir="output",
        backend="pollinations",
        force_lineart=True,
        lineart_method=lineart_method
    )

    book_dir = generator.generate_book(
        theme=theme,
        num_pages=num_pages,
        book_title=title
    )

    if not book_dir:
        logger.error("Failed to generate book pages")
        return None

    logger.info(f"✓ Interior pages complete: {book_dir}")

    # Step 2: Create PDF
    logger.info("\n📄 STEP 2/3: Creating PDF")
    logger.info("-" * 70)

    pdf_path = generator.create_pdf(book_dir)

    if not pdf_path:
        logger.error("Failed to create PDF")
        return None

    logger.info(f"✓ PDF created: {pdf_path}")

    # Step 3: Generate cover
    logger.info("\n🎨 STEP 3/3: Generating Cover")
    logger.info("-" * 70)

    cover_dir = book_dir / "cover"
    success = generate_cover(theme, title, output_dir=cover_dir)

    cover_path = None
    if success:
        covers = list(cover_dir.glob("*.png"))
        if covers:
            cover_path = covers[0]
            logger.info(f"✓ Cover created: {cover_path}")
    else:
        logger.warning("Cover generation failed (optional)")

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("✅ COLORING BOOK COMPLETE!")
    logger.info("=" * 70)

    result = {
        "title": title,
        "theme": theme,
        "pages": num_pages,
        "book_directory": str(book_dir),
        "pdf_path": str(pdf_path) if pdf_path else None,
        "cover_path": str(cover_path) if cover_path else None,
    }

    logger.info(f"\n📁 Files Location:")
    logger.info(f"   Directory: {book_dir}")
    logger.info(f"   PDF: {pdf_path.name if pdf_path else 'N/A'}")
    logger.info(f"   Cover: {cover_path.name if cover_path else 'N/A'}")

    # Publishing guidelines
    print_publishing_guide(result)

    return result


def print_publishing_guide(result: dict):
    """Print guidelines for publishing to Amazon KDP."""

    logger.info("\n" + "=" * 70)
    logger.info("📚 PUBLISHING GUIDELINES - AMAZON KDP")
    logger.info("=" * 70)

    logger.info("\n✓ Your book is ready for Amazon KDP!")
    logger.info("\nWhat you have:")
    logger.info(f"  • Interior PDF: {Path(result['pdf_path']).name}")
    logger.info(f"  • Pages: {result['pages']} coloring pages + title page")
    logger.info(f"  • Size: 8.5 x 11 inches (US Letter)")
    logger.info(f"  • Resolution: 300 DPI (print quality)")
    logger.info(f"  • Format: Black & white line art")

    logger.info("\n📋 NEXT STEPS:")

    logger.info("\n1. CREATE KDP ACCOUNT")
    logger.info("   → Go to kdp.amazon.com")
    logger.info("   → Sign up or log in")

    logger.info("\n2. CREATE NEW PAPERBACK")
    logger.info("   → Click 'Create' → 'Paperback'")
    logger.info("   → Enter your book details:")
    logger.info(f"     - Title: {result['title']}")
    logger.info("     - Subtitle: Adult Coloring Book")
    logger.info("     - Author: Your Name")
    logger.info("     - Description: Write engaging description")

    logger.info("\n3. CONTENT SETUP")
    logger.info("   → Trim Size: 8.5 x 11 inches")
    logger.info("   → Interior Type: Black & White")
    logger.info("   → Paper Type: White or Cream (your choice)")
    logger.info("   → Bleed: No bleed")
    logger.info(f"   → Upload Interior PDF: {Path(result['pdf_path']).name}")

    logger.info("\n4. COVER SETUP")
    logger.info("   Option A: Use generated cover")
    if result.get('cover_path'):
        logger.info(f"     → Upload: {Path(result['cover_path']).name}")
        logger.info("     → You'll need to add text/title using KDP Cover Creator")
    logger.info("\n   Option B: Use KDP Cover Creator")
    logger.info("     → Choose a template")
    logger.info("     → Add your title and design elements")
    logger.info("\n   Option C: Design your own")
    logger.info("     → Download cover template from KDP")
    logger.info("     → Design in Photoshop/GIMP/Canva")

    logger.info("\n5. PRICING")
    logger.info("   → KDP calculates minimum based on page count")
    logger.info("   → Typical pricing: $7-12 for adult coloring books")
    logger.info("   → Higher quality = higher price point")

    logger.info("\n6. PUBLISH")
    logger.info("   → Preview your book")
    logger.info("   → Submit for review (takes 24-72 hours)")
    logger.info("   → Once approved, it's live on Amazon!")

    logger.info("\n💡 TIPS:")
    logger.info("   • Add 'Look Inside' preview pages")
    logger.info("   • Use relevant keywords in description")
    logger.info("   • Consider creating a series")
    logger.info("   • Price competitively with similar books")
    logger.info("   • High-quality preview images help sales")

    logger.info("\n🔍 CATEGORIES (choose 2):")
    logger.info("   • Crafts & Hobbies > Coloring Books for Grown-Ups")
    logger.info("   • Self-Help > Stress Management")
    logger.info("   • Art > Techniques > Coloring")

    logger.info("\n" + "=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Complete workflow for creating a ready-to-publish coloring book",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a 30-page mandala book
  python complete_book_workflow.py --theme mandalas --pages 30

  # Create a 50-page animal book with custom title
  python complete_book_workflow.py \\
    --theme animals \\
    --pages 50 \\
    --title "Amazing Wildlife Coloring Adventures"

  # Create with detailed line art
  python complete_book_workflow.py \\
    --theme geometric \\
    --pages 40 \\
    --lineart-method detailed
        """
    )

    parser.add_argument("--theme", type=str, choices=list(THEMES.keys()),
                       required=True,
                       help="Coloring book theme")
    parser.add_argument("--pages", type=int, default=30,
                       help="Number of coloring pages (default: 30)")
    parser.add_argument("--title", type=str,
                       help="Custom book title")
    parser.add_argument("--lineart-method", type=str,
                       choices=["enhanced", "standard", "detailed"],
                       default="enhanced",
                       help="Line art quality (default: enhanced)")
    parser.add_argument("--list-themes", action="store_true",
                       help="List available themes and exit")

    args = parser.parse_args()

    if args.list_themes:
        print("\nAvailable Themes:")
        print("=" * 60)
        for theme, data in THEMES.items():
            print(f"  {theme}: {data['name']}")
            print(f"    Prompts: {len(data['prompts'])}")
        print()
        return

    create_complete_book(
        theme=args.theme,
        num_pages=args.pages,
        book_title=args.title,
        lineart_method=args.lineart_method
    )


if __name__ == "__main__":
    main()
