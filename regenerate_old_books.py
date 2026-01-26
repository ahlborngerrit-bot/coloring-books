#!/usr/bin/env python3
"""
Regenerate Old Coloring Books with Fixed Quality

This script identifies old coloring books that were generated before the
quality fixes (v2.0.1 and v2.1.0) and regenerates them with proper print quality.

Specifically fixes:
- Issue #001: Images too small (768x768 or 1024x1024)
- Should be: 2550x3300 pixels (8.5" x 11" @ 300 DPI)
- Missing DPI metadata
- Proper quality assurance
"""

import sys
import json
from pathlib import Path
from PIL import Image
from coloring_book_generator import ColoringBookGenerator


def check_book_quality(book_dir: Path) -> dict:
    """Check if a book needs regeneration.

    Returns:
        dict with 'needs_regen', 'reason', 'pages', 'theme', 'title'
    """
    result = {
        'needs_regen': False,
        'reason': '',
        'pages': 0,
        'theme': 'unknown',
        'title': 'Unknown'
    }

    # Check if metadata exists
    metadata_file = book_dir / 'metadata.json'
    if metadata_file.exists():
        metadata = json.loads(metadata_file.read_text())
        result['pages'] = metadata.get('pages', 0)
        result['theme'] = metadata.get('theme', 'unknown')
        result['title'] = metadata.get('title', 'Unknown')

    # Check images directory
    images_dir = book_dir / 'images'
    if not images_dir.exists():
        result['reason'] = 'No images directory'
        return result

    # Check first image
    images = list(images_dir.glob('*.png'))
    if not images:
        result['reason'] = 'No images found'
        return result

    img = Image.open(images[0])
    width, height = img.size
    dpi = img.info.get('dpi', (0, 0))

    # Check if needs regeneration
    if width < 2550 or height < 3300:
        result['needs_regen'] = True
        result['reason'] = f'Size {width}x{height} too small (need 2550x3300)'
    elif dpi[0] < 299 or dpi[1] < 299:
        # Use 299 tolerance (299.9994 is effectively 300)
        result['needs_regen'] = True
        result['reason'] = f'DPI {dpi} too low (need 300)'

    return result


def scan_books():
    """Scan all books and identify those needing regeneration."""
    output_dir = Path('output')
    if not output_dir.exists():
        print("No output directory found")
        return []

    books_to_regen = []

    # Scan all book directories
    for book_dir in sorted(output_dir.glob('*_*')):
        if not book_dir.is_dir():
            continue

        # Skip MAGA and test directories
        if 'MAGA' in book_dir.name or book_dir.name in ['lineart_test', 'quick_test']:
            continue

        # Skip if it's a simple test
        if book_dir.name.startswith('Test_') and 'Test_Mandalas' not in book_dir.name:
            continue

        # Check quality
        check = check_book_quality(book_dir)

        if check['needs_regen']:
            # Skip if theme is removed/unknown
            if check['theme'] in ['maga_rally', 'unknown']:
                print(f"⊘ Skipping {book_dir.name}: {check['theme']} theme (removed/unknown)")
                continue

            books_to_regen.append({
                'dir': book_dir,
                'theme': check['theme'],
                'title': check['title'],
                'pages': check['pages'],
                'reason': check['reason']
            })

    return books_to_regen


def regenerate_book(book_info: dict):
    """Regenerate a book with proper quality."""
    print(f"\n{'='*70}")
    print(f"Regenerating: {book_info['title']}")
    print(f"{'='*70}")
    print(f"Original: {book_info['dir'].name}")
    print(f"Theme: {book_info['theme']}")
    print(f"Pages: {book_info['pages']}")
    print(f"Reason: {book_info['reason']}")
    print()

    # Create generator with quality assurance
    gen = ColoringBookGenerator(
        backend="pollinations",
        force_lineart=True,
        lineart_method="enhanced"
    )

    # Generate with FIXED suffix
    new_title = f"{book_info['title']}_FIXED"

    try:
        book_dir = gen.generate_book(
            theme=book_info['theme'],
            num_pages=book_info['pages'],
            book_title=new_title
        )

        print(f"\n✓ Regenerated successfully!")
        print(f"  New location: {book_dir}")
        print(f"  Quality: Guaranteed 2550x3300 @ 300 DPI")

        return True

    except Exception as e:
        print(f"\n✗ Regeneration failed: {e}")
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  COLORING BOOK REGENERATION TOOL                                     ║
║  Version 2.1.0                                                       ║
║                                                                      ║
║  Purpose: Fix old books generated before quality fixes               ║
║  Issue #001: Images too small for print (768x768 or 1024x1024)       ║
║  Solution: Regenerate with v2.1.0 quality assurance                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    print("Scanning for books needing regeneration...\n")

    books_to_regen = scan_books()

    if not books_to_regen:
        print("✓ No books need regeneration - all are good quality!")
        return

    print(f"\nFound {len(books_to_regen)} book(s) needing regeneration:\n")

    for i, book in enumerate(books_to_regen, 1):
        print(f"{i}. {book['title']}")
        print(f"   Theme: {book['theme']}, Pages: {book['pages']}")
        print(f"   Issue: {book['reason']}")
        print()

    # Ask for confirmation
    try:
        response = input(f"Regenerate all {len(books_to_regen)} books? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    except EOFError:
        # Non-interactive mode
        if '--auto' not in sys.argv:
            print("Non-interactive mode - use --auto flag to regenerate automatically")
            return

    print("\nStarting regeneration...\n")

    success_count = 0
    for book in books_to_regen:
        if regenerate_book(book):
            success_count += 1

    print("\n" + "="*70)
    print("REGENERATION COMPLETE")
    print("="*70)
    print(f"Success: {success_count}/{len(books_to_regen)}")
    print()

    if success_count == len(books_to_regen):
        print("✓ All books regenerated successfully!")
        print("\nNew books have '_FIXED' suffix and proper print quality:")
        print("  - Size: 2550x3300 pixels")
        print("  - DPI: 300x300")
        print("  - Physical: 8.5\" x 11\"")
        print("  - Quality: Verified by v2.1.0 QA system")
    else:
        print(f"⚠ {len(books_to_regen) - success_count} book(s) failed to regenerate")
        print("  Check error messages above for details")


if __name__ == "__main__":
    main()
