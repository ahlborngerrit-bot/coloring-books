#!/usr/bin/env python3
"""
Test script to demonstrate improved line art conversion for coloring books.
This shows before/after comparisons of the enhanced edge detection.
"""

import os
import sys
from pathlib import Path
from coloring_book_generator import ColoringBookGenerator

def test_lineart_methods():
    """Generate sample pages with different line art methods."""

    print("=" * 60)
    print("COLORING BOOK LINE ART QUALITY TEST")
    print("=" * 60)
    print()
    print("This test will generate 3 sample coloring pages using:")
    print("  1. Enhanced method (thick bold lines) - RECOMMENDED")
    print("  2. Standard method (balanced)")
    print("  3. Detailed method (fine lines)")
    print()
    print("Using Pollinations.ai (free, no API key required)")
    print("=" * 60)
    print()

    # Test with a simple theme
    theme = "mandalas"
    output_base = Path("output/lineart_test")
    output_base.mkdir(parents=True, exist_ok=True)

    methods = ["enhanced", "standard", "detailed"]

    for method in methods:
        print(f"\n{'='*60}")
        print(f"Testing {method.upper()} method...")
        print(f"{'='*60}\n")

        generator = ColoringBookGenerator(
            output_dir=str(output_base / method),
            backend="pollinations",
            force_lineart=True,
            lineart_method=method
        )

        try:
            book_dir = generator.generate_book(
                theme=theme,
                num_pages=2,  # Just 2 pages for quick test
                book_title=f"Test_{method.capitalize()}_Lineart"
            )

            print(f"\n✓ {method.capitalize()} method completed!")
            print(f"  Output: {book_dir}")

        except Exception as e:
            print(f"\n✗ {method.capitalize()} method failed: {e}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    print(f"\nResults saved to: {output_base.absolute()}")
    print("\nCompare the three methods to see which works best for your needs:")
    print("  • ENHANCED: Thick bold lines - best for easy coloring")
    print("  • STANDARD: Balanced - good general purpose")
    print("  • DETAILED: Fine lines - best for intricate designs")
    print()


def test_quick_sample():
    """Generate a quick single page sample with enhanced method."""

    print("=" * 60)
    print("QUICK COLORING BOOK PAGE TEST")
    print("=" * 60)
    print("\nGenerating a single mandala coloring page...")
    print("Using: Enhanced line art method (recommended)")
    print("Backend: Pollinations.ai (free)")
    print()

    generator = ColoringBookGenerator(
        output_dir="output/quick_test",
        backend="pollinations",
        force_lineart=True,
        lineart_method="enhanced"
    )

    try:
        book_dir = generator.generate_book(
            theme="mandalas",
            num_pages=1,
            book_title="Quick_Test_Coloring_Page"
        )

        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print(f"\nYour coloring page is ready:")
        print(f"  {book_dir.absolute()}")
        print()

    except Exception as e:
        print(f"\n✗ FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test improved line art generation")
    parser.add_argument("--quick", action="store_true",
                       help="Quick test - generate just 1 page")
    parser.add_argument("--full", action="store_true",
                       help="Full test - compare all 3 methods")

    args = parser.parse_args()

    if args.full:
        test_lineart_methods()
    elif args.quick:
        test_quick_sample()
    else:
        # Default: quick test
        print("Running quick test (use --full for comprehensive comparison)")
        print()
        test_quick_sample()
