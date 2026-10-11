"""Run the script-style test classes in test_expanded_coverage.py that pytest cannot collect
(they define __init__). Tests only: each method is called as-is; returning False is a failure."""
from __future__ import annotations

import inspect

import pytest

import test_expanded_coverage as tec

CLASSES = [c for _, c in inspect.getmembers(tec, inspect.isclass)
           if c.__module__ == tec.__name__ and c.__name__.startswith("Test") and "__init__" in c.__dict__]
CASES = [(c, m) for c in CLASSES for m in sorted(n for n in c.__dict__ if n.startswith("test_"))]


@pytest.mark.parametrize("cls,method", CASES, ids=[f"{c.__name__}.{m}" for c, m in CASES])
def test_script_class_method(cls, method):
    result = getattr(cls(), method)()
    assert result is not False, f"{cls.__name__}.{method} returned False"
