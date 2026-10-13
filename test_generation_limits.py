"""Safety regression tests for bounded generation before any provider work."""

import pytest

import coloring_book_generator as generator_module


@pytest.mark.parametrize("num_pages", [0, -1, 101, 1.5, True, "10", None])
def test_invalid_page_count_is_rejected_before_preflight(tmp_path, monkeypatch, num_pages):
    def unexpected_preflight(**_kwargs):
        pytest.fail("invalid page counts must be rejected before preflight/provider work")

    monkeypatch.setattr(generator_module, "preflight_checks", unexpected_preflight)
    generator = generator_module.ColoringBookGenerator(output_dir=str(tmp_path / "output"))

    with pytest.raises(ValueError, match="num_pages must be an integer"):
        generator.generate_book(theme="geometric", num_pages=num_pages)


@pytest.mark.parametrize("num_pages", [1, 100])
def test_page_count_boundaries_reach_preflight_without_provider_calls(
    tmp_path, monkeypatch, num_pages
):
    monkeypatch.setattr(generator_module, "preflight_checks", lambda **_kwargs: False)
    generator = generator_module.ColoringBookGenerator(output_dir=str(tmp_path / "output"))

    with pytest.raises(RuntimeError, match="Pre-flight checks failed"):
        generator.generate_book(theme="geometric", num_pages=num_pages)
