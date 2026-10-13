#!/usr/bin/env python3
"""Strict candidate runner for line-art generation; proposal only, not product code."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image
import numpy as np

from coloring_book_generator import ColoringBookGenerator


def validate_generated_book(book_dir: Path, expected_pages: int) -> list[str]:
    """Validate generated artifacts independently of the generator's own status."""
    errors: list[str] = []
    if not book_dir.is_dir():
        return [f"Output directory does not exist: {book_dir}"]

    metadata_path = book_dir / "metadata.json"
    if not metadata_path.is_file():
        return [f"Missing metadata file: {metadata_path}"]

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Cannot read metadata: {type(exc).__name__}: {exc}"]

    pages = metadata.get("pages_data")
    if not isinstance(pages, list):
        return ["metadata.pages_data is missing or is not a list"]
    if len(pages) != expected_pages:
        errors.append(f"Expected {expected_pages} accepted pages, found {len(pages)}")

    images_dir = book_dir / "images"
    for index, page in enumerate(pages, start=1):
        filename = page.get("file") if isinstance(page, dict) else None
        if not isinstance(filename, str) or not filename:
            errors.append(f"Page record {index} has no valid filename")
            continue

        # Only accept simple filenames, not metadata-supplied paths outside images/.
        if Path(filename).name != filename:
            errors.append(f"Page record {index} contains a non-local filename: {filename!r}")
            continue

        image_path = images_dir / filename
        if not image_path.is_file():
            errors.append(f"Missing image for page {index}: {image_path}")
            continue

        try:
            with Image.open(image_path) as image:
                image.verify()
            with Image.open(image_path) as image:
                if image.width < 2550 or image.height < 3300:
                    errors.append(
                        f"{filename}: dimensions {image.width}x{image.height}; "
                        "expected at least 2550x3300 for 8.5x11 in at 300 DPI"
                    )
                dpi = image.info.get("dpi")
                if not isinstance(dpi, tuple) or len(dpi) < 2 or dpi[0] < 299 or dpi[1] < 299:
                    errors.append(f"{filename}: missing or insufficient 300-DPI metadata: {dpi!r}")

                rgb = np.asarray(image.convert("RGB"))
                channels_equal = (
                    np.array_equal(rgb[:, :, 0], rgb[:, :, 1])
                    and np.array_equal(rgb[:, :, 1], rgb[:, :, 2])
                )
                channel = rgb[:, :, 0]
                binary = bool(np.all((channel == 0) | (channel == 255)))
                if not channels_equal or not binary:
                    errors.append(f"{filename}: image is not strict black-and-white binary line art")
        except Exception as exc:  # include corrupt image and decoder errors in the test result
            errors.append(f"{filename}: image validation raised {type(exc).__name__}: {exc}")

    return errors


def run_method(method: str, pages: int) -> list[str]:
    output = Path("output/lineart_test_v2") / method
    generator = ColoringBookGenerator(
        output_dir=str(output),
        backend="pollinations",
        force_lineart=True,
        lineart_method=method,
    )
    book_dir = generator.generate_book(
        theme="mandalas",
        num_pages=pages,
        book_title=f"Test_{method.capitalize()}_Lineart_V2",
    )
    if not isinstance(book_dir, (str, Path)):
        return [f"{method}: generator returned unexpected value {type(book_dir).__name__}"]

    resolved = Path(book_dir)
    errors = validate_generated_book(resolved, expected_pages=pages)
    if errors:
        print(f"FAIL {method}:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"PASS {method}: {pages} validated page(s) in {resolved}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Generate one page")
    parser.add_argument("--full", action="store_true", help="Generate two pages for each method")
    args = parser.parse_args()

    if args.quick and args.full:
        parser.error("Choose either --quick or --full, not both")

    # This is a network-backed opt-in integration check. Do not use in ordinary CI.
    if args.full:
        plan = [("enhanced", 2), ("standard", 2), ("detailed", 2)]
    else:
        plan = [("enhanced", 1)]

    failures: list[tuple[str, str]] = []
    for method, pages in plan:
        try:
            errors = run_method(method, pages)
            failures.extend((method, error) for error in errors)
        except Exception as exc:
            failures.append((method, f"{type(exc).__name__}: {exc}"))
            print(f"FAIL {method}: {type(exc).__name__}: {exc}", file=sys.stderr)

    if failures:
        print(f"FAILED: {len(failures)} validation issue(s) across {len(plan)} method(s)")
        return 1
    print(f"PASS: all {len(plan)} requested method run(s) generated validated artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
