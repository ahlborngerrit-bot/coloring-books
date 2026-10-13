"""Deterministic unit tests for the proposed artifact validator; no provider/network calls."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
import sys

from PIL import Image

# Make the adjacent proposal module importable when tests are run from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_improved_lineart_v2 import validate_generated_book


class ArtifactValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "book"
        (self.root / "images").mkdir(parents=True)

    def write_metadata(self, filenames: list[str]) -> None:
        (self.root / "metadata.json").write_text(
            json.dumps({"pages_data": [{"file": name} for name in filenames]}),
            encoding="utf-8",
        )

    def test_accepts_print_size_binary_image_with_300_dpi(self) -> None:
        path = self.root / "images" / "page_001.png"
        Image.new("1", (2550, 3300), 1).save(path, dpi=(300, 300))
        self.write_metadata(["page_001.png"])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertEqual(errors, [])

    def test_rejects_missing_metadata(self) -> None:
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("Missing metadata" in error for error in errors))

    def test_rejects_partial_book(self) -> None:
        self.write_metadata([])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("Expected 1 accepted pages, found 0" in error for error in errors))

    def test_rejects_missing_referenced_image(self) -> None:
        self.write_metadata(["page_001.png"])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("Missing image" in error for error in errors))

    def test_rejects_color_pixels(self) -> None:
        path = self.root / "images" / "page_001.png"
        Image.new("RGB", (20, 20), (255, 0, 0)).save(path, dpi=(72, 72))
        self.write_metadata(["page_001.png"])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("not strict black-and-white binary" in error for error in errors))

    def test_rejects_path_traversal_in_metadata(self) -> None:
        self.write_metadata(["../../outside.png"])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("non-local filename" in error for error in errors))

    def test_rejects_corrupt_image(self) -> None:
        (self.root / "images" / "page_001.png").write_bytes(b"not a PNG")
        self.write_metadata(["page_001.png"])
        errors = validate_generated_book(self.root, expected_pages=1)
        self.assertTrue(any("image validation raised" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
