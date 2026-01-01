#!/usr/bin/env python3
"""
Batch generator for creating multiple coloring books.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

from coloring_book_generator import ColoringBookGenerator, THEMES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_all_books(themes: list = None, pages_per_book: int = 30, output_dir: str = "output"):
    """Generate coloring books for multiple themes."""

    if themes is None:
        themes = list(THEMES.keys())

    generator = ColoringBookGenerator(output_dir=output_dir)

    results = []

    for i, theme in enumerate(themes, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Generating book {i}/{len(themes)}: {THEMES[theme]['name']}")
        logger.info(f"{'='*60}")

        try:
            book_dir = generator.generate_book(
                theme=theme,
                num_pages=pages_per_book,
            )

            if book_dir:
                pdf_path = generator.create_pdf(book_dir)
                results.append({
                    "theme": theme,
                    "title": THEMES[theme]['name'],
                    "directory": str(book_dir),
                    "pdf": str(pdf_path) if pdf_path else None,
                    "status": "success"
                })
            else:
                results.append({
                    "theme": theme,
                    "status": "failed"
                })

        except Exception as e:
            logger.error(f"Error generating {theme}: {e}")
            results.append({
                "theme": theme,
                "status": "error",
                "error": str(e)
            })

        # Pause between books
        if i < len(themes):
            logger.info("Waiting 30 seconds before next book...")
            time.sleep(30)

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("BATCH GENERATION COMPLETE")
    logger.info(f"{'='*60}")

    success = sum(1 for r in results if r.get("status") == "success")
    logger.info(f"Success: {success}/{len(themes)}")

    for r in results:
        status = "✓" if r.get("status") == "success" else "✗"
        logger.info(f"  {status} {r.get('title', r['theme'])}")
        if r.get("pdf"):
            logger.info(f"    PDF: {r['pdf']}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Batch generate coloring books")
    parser.add_argument("--all-themes", action="store_true",
                       help="Generate all themes")
    parser.add_argument("--themes", nargs="+", choices=list(THEMES.keys()),
                       help="Specific themes to generate")
    parser.add_argument("--pages", type=int, default=30,
                       help="Pages per book (default: 30)")
    parser.add_argument("--output", type=str, default="output",
                       help="Output directory")

    args = parser.parse_args()

    if args.all_themes:
        themes = list(THEMES.keys())
    elif args.themes:
        themes = args.themes
    else:
        print("Specify --all-themes or --themes")
        parser.print_help()
        return

    generate_all_books(
        themes=themes,
        pages_per_book=args.pages,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()
