#!/usr/bin/env python3
"""Generate sample coloring pages for each line-art method.

This is a review proposal, not the production script. It returns a non-zero
process exit code if any requested method fails, so CI/automation cannot
mistake a partial failure for success.
"""
import argparse
import sys
from pathlib import Path

from coloring_book_generator import ColoringBookGenerator


def test_lineart_methods() -> int:
    """Attempt every method and report aggregate failure accurately."""
    print("=" * 60)
    print("COLORING BOOK LINE ART QUALITY TEST")
    print("=" * 60)
    print("Methods: enhanced, standard, detailed")
    print("Backend: Pollinations (provider availability/terms may change)")
    print()

    theme = "mandalas"
    output_base = Path("output/lineart_test")
    output_base.mkdir(parents=True, exist_ok=True)
    failures: list[tuple[str, str]] = []

    for method in ("enhanced", "standard", "detailed"):
        print(f"\n{'=' * 60}\nTesting {method.upper()} method...\n{'=' * 60}")
        try:
            generator = ColoringBookGenerator(
                output_dir=str(output_base / method),
                backend="pollinations",
                force_lineart=True,
                lineart_method=method,
            )
            book_dir = generator.generate_book(
                theme=theme,
                num_pages=2,
                book_title=f"Test_{method.capitalize()}_Lineart",
            )
            if not book_dir:
                raise RuntimeError("Generator returned no output directory")
            print(f"PASS: {method}; output: {book_dir}")
        except Exception as exc:
            failures.append((method, f"{type(exc).__name__}: {exc}"))
            print(f"FAIL: {method}: {type(exc).__name__}: {exc}", file=sys.stderr)

    print("\n" + "=" * 60)
    if failures:
        print(f"FAILED: {len(failures)} of 3 methods")
        for method, reason in failures:
            print(f"- {method}: {reason}")
        return 1

    print("PASS: all three methods completed")
    print(f"Results saved under: {output_base.resolve()}")
    return 0


def test_quick_sample() -> int:
    """Generate one sample and return a meaningful process status."""
    output_dir = Path("output/quick_test")
    try:
        generator = ColoringBookGenerator(
            output_dir=str(output_dir),
            backend="pollinations",
            force_lineart=True,
            lineart_method="enhanced",
        )
        book_dir = generator.generate_book(
            theme="mandalas",
            num_pages=1,
            book_title="Quick_Test_Coloring_Page",
        )
        if not book_dir:
            raise RuntimeError("Generator returned no output directory")
        print(f"PASS: sample generated at {book_dir}")
        return 0
    except Exception as exc:
        print(f"FAIL: quick sample: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Test improved line-art generation")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--quick", action="store_true", help="Generate one sample page")
    group.add_argument("--full", action="store_true", help="Compare all three methods")
    args = parser.parse_args()

    if args.full:
        return test_lineart_methods()
    return test_quick_sample()


if __name__ == "__main__":
    raise SystemExit(main())
