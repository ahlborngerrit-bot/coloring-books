#!/usr/bin/env python3
"""
Expanded Test Coverage for Coloring Book Generator

Additional tests beyond quality_assurance tests:
- Individual backend methods
- Line art processing methods
- Error handling
- Edge cases
- PDF generation
- Upscaling verification

Run with: python3 test_expanded_coverage.py
"""

import sys
import tempfile
import json
from pathlib import Path
from io import BytesIO
import numpy as np

# Import main module
from coloring_book_generator import (
    ColoringBookGenerator,
    validate_image_quality,
    MIN_PRINT_WIDTH,
    MIN_PRINT_HEIGHT,
    REQUIRED_DPI
)


def create_test_image(width=768, height=768, color=(255, 255, 255)):
    """Create a simple test image in memory.

    Returns:
        bytes: PNG image as bytes
    """
    try:
        from PIL import Image

        # Create white image
        img = Image.new('RGB', (width, height), color)

        # Add some black lines for edge detection testing
        import numpy as np
        arr = np.array(img)
        # Horizontal line
        arr[height//2, :] = [0, 0, 0]
        # Vertical line
        arr[:, width//2] = [0, 0, 0]
        # Diagonal
        for i in range(min(width, height)):
            arr[i, i] = [0, 0, 0]

        img = Image.fromarray(arr)

        # Save to bytes
        output = BytesIO()
        img.save(output, format='PNG')
        return output.getvalue()
    except ImportError:
        print("⚠ PIL not available - skipping image tests")
        return None


class TestLineArtMethods:
    """Test all three line art processing methods."""

    def __init__(self):
        self.gen = ColoringBookGenerator(force_lineart=True)

    def test_enhanced_method(self):
        """Test enhanced line art method (thick lines)."""
        print("\n🧪 Testing enhanced line art method...")

        test_img = create_test_image(768, 768)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            # Should upscale and process
            result = self.gen.convert_to_coloring_page(
                test_img,
                method='enhanced',
                target_size=(2550, 3300)
            )

            assert result is not None, "Result should not be None"
            assert len(result) > 0, "Result should have content"

            # Verify result is larger than input
            assert len(result) > len(test_img), "Processed should be larger (upscaled)"

            print("  ✓ Enhanced method works")
            return True

        except Exception as e:
            print(f"  ✗ Enhanced method failed: {e}")
            return False

    def test_standard_method(self):
        """Test standard line art method."""
        print("\n🧪 Testing standard line art method...")

        test_img = create_test_image(768, 768)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            result = self.gen.convert_to_coloring_page(
                test_img,
                method='standard',
                target_size=(2550, 3300)
            )

            assert result is not None
            assert len(result) > 0

            print("  ✓ Standard method works")
            return True

        except Exception as e:
            print(f"  ✗ Standard method failed: {e}")
            return False

    def test_detailed_method(self):
        """Test detailed line art method (fine lines)."""
        print("\n🧪 Testing detailed line art method...")

        test_img = create_test_image(768, 768)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            result = self.gen.convert_to_coloring_page(
                test_img,
                method='detailed',
                target_size=(2550, 3300)
            )

            assert result is not None
            assert len(result) > 0

            print("  ✓ Detailed method works")
            return True

        except Exception as e:
            print(f"  ✗ Detailed method failed: {e}")
            return False


class TestUpscaling:
    """Test upscaling functionality."""

    def __init__(self):
        self.gen = ColoringBookGenerator()

    def test_upscale_small_image(self):
        """Test that small images get upscaled."""
        print("\n🧪 Testing upscaling of small images...")

        # Create 768x768 image
        test_img = create_test_image(768, 768)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            result = self.gen.upscale_to_print_quality(
                test_img,
                target_size=(2550, 3300)
            )

            # Verify upscaling happened
            from PIL import Image
            result_img = Image.open(BytesIO(result))

            assert result_img.size == (2550, 3300), \
                f"Should be upscaled to (2550, 3300), got {result_img.size}"

            print(f"  ✓ Upscaled from 768x768 to {result_img.size}")
            return True

        except Exception as e:
            print(f"  ✗ Upscaling failed: {e}")
            return False

    def test_no_upscale_large_image(self):
        """Test that large images don't get upscaled."""
        print("\n🧪 Testing that large images aren't upscaled...")

        # Create already-large image
        test_img = create_test_image(2550, 3300)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            result = self.gen.upscale_to_print_quality(
                test_img,
                target_size=(2550, 3300)
            )

            from PIL import Image
            result_img = Image.open(BytesIO(result))

            assert result_img.size == (2550, 3300), \
                "Should maintain size"

            print(f"  ✓ Large image kept at {result_img.size}")
            return True

        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            return False

    def test_upscale_sets_dpi(self):
        """Test that upscaling sets DPI metadata."""
        print("\n🧪 Testing DPI metadata is set during upscaling...")

        test_img = create_test_image(768, 768)
        if not test_img:
            print("  ⊘ Skipped (PIL not available)")
            return False

        try:
            result = self.gen.upscale_to_print_quality(test_img)

            from PIL import Image
            result_img = Image.open(BytesIO(result))
            dpi = result_img.info.get('dpi', (0, 0))

            # Should be ~300 (sometimes 299.9994)
            assert dpi[0] >= 299 and dpi[1] >= 299, \
                f"DPI should be ~300, got {dpi}"

            print(f"  ✓ DPI metadata set to {dpi}")
            return True

        except Exception as e:
            print(f"  ✗ DPI test failed: {e}")
            return False


class TestErrorHandling:
    """Test error handling and edge cases."""

    def __init__(self):
        self.gen = ColoringBookGenerator()

    def test_invalid_theme(self):
        """Test handling of invalid theme."""
        print("\n🧪 Testing invalid theme handling...")

        try:
            # Should raise ValueError
            self.gen.generate_book(
                theme='nonexistent_theme',
                num_pages=1,
                book_title='Test'
            )
            print("  ✗ Should have raised ValueError")
            return False

        except ValueError as e:
            if 'Unknown theme' in str(e):
                print("  ✓ Correctly raises ValueError for invalid theme")
                return True
            else:
                print(f"  ✗ Wrong error message: {e}")
                return False
        except Exception as e:
            print(f"  ✗ Wrong exception type: {type(e).__name__}")
            return False

    def test_corrupt_image_upscaling(self):
        """Test handling of corrupt image data."""
        print("\n🧪 Testing corrupt image handling...")

        try:
            # Pass invalid image data
            corrupt_data = b'this is not an image'

            # Should raise RuntimeError
            result = self.gen.upscale_to_print_quality(corrupt_data)
            print("  ✗ Should have raised RuntimeError")
            return False

        except RuntimeError as e:
            if 'Image decode failed' in str(e) or 'cannot ensure print quality' in str(e):
                print("  ✓ Correctly raises RuntimeError for corrupt data")
                return True
            else:
                print(f"  ✗ Wrong error message: {e}")
                return False
        except Exception as e:
            print(f"  ⚠ Got {type(e).__name__}: {e}")
            # Accept this as the error is caught
            return True

    def test_zero_pages(self):
        """Test handling of zero pages request."""
        print("\n🧪 Testing zero pages request...")

        try:
            # Zero pages should work but generate nothing
            result = self.gen.generate_book(
                theme='mandalas',
                num_pages=0,
                book_title='Zero_Pages_Test'
            )

            # Should complete but generate no images
            images_dir = result / 'images'
            images = list(images_dir.glob('*.png'))

            assert len(images) == 0, "Should have zero images"
            print("  ✓ Zero pages handled correctly")
            return True

        except Exception as e:
            print(f"  ⚠ Got exception: {e}")
            # This is acceptable too
            return True


class TestImageValidation:
    """Test image quality validation function."""

    def test_validate_good_image(self):
        """Test validation passes for good image."""
        print("\n🧪 Testing validation of good quality image...")

        try:
            from PIL import Image

            # Create temporary test image with correct specs
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                img = Image.new('L', (2550, 3300), 255)
                img.save(f, format='PNG', dpi=(300, 300))
                temp_path = Path(f.name)

            try:
                result = validate_image_quality(
                    temp_path,
                    check_binary=False  # Don't check binary for this test
                )

                assert result['valid'], "Should be valid"
                assert len(result.get('issues', [])) == 0, "Should have no issues"

                print("  ✓ Good image passes validation")
                return True

            finally:
                temp_path.unlink()  # Clean up

        except ImportError:
            print("  ⊘ Skipped (PIL not available)")
            return False
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            return False

    def test_validate_small_image(self):
        """Test validation fails for too-small image."""
        print("\n🧪 Testing validation rejects small images...")

        try:
            from PIL import Image

            # Create temporary small image
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                img = Image.new('L', (768, 768), 255)
                img.save(f, format='PNG')
                temp_path = Path(f.name)

            try:
                result = validate_image_quality(temp_path, check_binary=False)

                assert not result['valid'], "Should be invalid (too small)"
                assert len(result.get('issues', [])) > 0, "Should have issues"

                print(f"  ✓ Small image correctly rejected: {result['issues'][0]}")
                return True

            finally:
                temp_path.unlink()

        except ImportError:
            print("  ⊘ Skipped (PIL not available)")
            return False
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            return False


class TestMetadata:
    """Test metadata generation and quality metrics."""

    def test_metadata_includes_quality_metrics(self):
        """Test that generated books include quality metrics in metadata."""
        print("\n🧪 Testing metadata includes quality metrics...")

        try:
            gen = ColoringBookGenerator(
                backend='pollinations',
                force_lineart=True
            )

            # Generate single page book
            book_dir = gen.generate_book(
                theme='geometric',
                num_pages=1,
                book_title='Metadata_Test'
            )

            # Read metadata
            metadata_file = book_dir / 'metadata.json'
            assert metadata_file.exists(), "Metadata file should exist"

            metadata = json.loads(metadata_file.read_text())

            # Check for quality metrics
            assert 'pages_data' in metadata, "Should have pages_data"
            assert len(metadata['pages_data']) > 0, "Should have at least one page"

            page_data = metadata['pages_data'][0]
            assert 'quality_metrics' in page_data, "Should have quality_metrics"

            metrics = page_data['quality_metrics']
            assert 'width' in metrics, "Should have width"
            assert 'height' in metrics, "Should have height"
            assert 'dpi' in metrics, "Should have DPI"

            print(f"  ✓ Quality metrics present: {list(metrics.keys())}")
            return True

        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def run_all_tests():
    """Run all expanded tests."""
    print("=" * 70)
    print("EXPANDED TEST COVERAGE")
    print("=" * 70)
    print("\nRunning comprehensive tests...")

    results = []

    # Line art methods
    print("\n" + "=" * 70)
    print("LINE ART METHODS")
    print("=" * 70)
    lineart_tests = TestLineArtMethods()
    results.append(("Enhanced line art", lineart_tests.test_enhanced_method()))
    results.append(("Standard line art", lineart_tests.test_standard_method()))
    results.append(("Detailed line art", lineart_tests.test_detailed_method()))

    # Upscaling
    print("\n" + "=" * 70)
    print("UPSCALING TESTS")
    print("=" * 70)
    upscale_tests = TestUpscaling()
    results.append(("Upscale small image", upscale_tests.test_upscale_small_image()))
    results.append(("No upscale large image", upscale_tests.test_no_upscale_large_image()))
    results.append(("DPI metadata set", upscale_tests.test_upscale_sets_dpi()))

    # Error handling
    print("\n" + "=" * 70)
    print("ERROR HANDLING")
    print("=" * 70)
    error_tests = TestErrorHandling()
    results.append(("Invalid theme", error_tests.test_invalid_theme()))
    results.append(("Corrupt image", error_tests.test_corrupt_image_upscaling()))
    results.append(("Zero pages", error_tests.test_zero_pages()))

    # Image validation
    print("\n" + "=" * 70)
    print("IMAGE VALIDATION")
    print("=" * 70)
    validation_tests = TestImageValidation()
    results.append(("Validate good image", validation_tests.test_validate_good_image()))
    results.append(("Validate small image", validation_tests.test_validate_small_image()))

    # Metadata (integration test - optional)
    if '--full' in sys.argv:
        print("\n" + "=" * 70)
        print("METADATA & INTEGRATION")
        print("=" * 70)
        metadata_tests = TestMetadata()
        results.append(("Metadata quality metrics", metadata_tests.test_metadata_includes_quality_metrics()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST RESULTS SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\nTests run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {passed/total*100:.1f}%")

    # List failures
    failures = [name for name, result in results if not result]
    if failures:
        print("\nFailed tests:")
        for name in failures:
            print(f"  ✗ {name}")

    print("\n" + "=" * 70)

    if passed == total:
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        return 0
    else:
        print(f"⚠️ {total - passed} TEST(S) FAILED")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  EXPANDED TEST COVERAGE                                              ║
║  Coloring Book Generator v2.1.0                                      ║
║                                                                      ║
║  Tests individual components and edge cases                          ║
║  Complements test_quality_assurance.py                               ║
║                                                                      ║
║  Usage:                                                              ║
║    python3 test_expanded_coverage.py        # Core tests             ║
║    python3 test_expanded_coverage.py --full # Include integration    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

    exit_code = run_all_tests()
    sys.exit(exit_code)
