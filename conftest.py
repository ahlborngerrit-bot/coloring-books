"""Test harness (tests only; no generator code changed).

- Network is blocked by default: the three live tests that call Pollinations.ai are skipped unless
  RUN_NETWORK_TESTS=1, and any other outbound connection fails fast instead of hanging.
- Script-style tests here signal failure by *returning* False (pytest ignores return values and would
  report them as passed). A test that returns False is turned into a real failure.
- Generated files go to a temp dir, not ./output.
"""
from __future__ import annotations

import os
import socket

import pytest

NETWORK_TESTS = {
    "test_improved_lineart.py::test_lineart_methods",
    "test_improved_lineart.py::test_quick_sample",
    "test_quality_assurance.py::test_integration_single_page",
}
RUN_NETWORK = os.environ.get("RUN_NETWORK_TESTS") == "1"


def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.nodeid in NETWORK_TESTS:
            item.add_marker(pytest.mark.network)
            if not RUN_NETWORK:
                item.add_marker(pytest.mark.skip(reason="live API call (Pollinations.ai); set RUN_NETWORK_TESTS=1"))


def pytest_configure(config):
    config.addinivalue_line("markers", "network: calls a live external API")


@pytest.fixture(autouse=True)
def _offline(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    if RUN_NETWORK:
        return
    real_connect = socket.socket.connect

    def guarded(self, address):
        host = address[0] if isinstance(address, tuple) else address
        if host in ("127.0.0.1", "::1", "localhost") or isinstance(address, (str, bytes)):
            return real_connect(self, address)
        raise OSError(f"network disabled in tests (tried {address}); set RUN_NETWORK_TESTS=1")

    monkeypatch.setattr(socket.socket, "connect", guarded)


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    outcome = yield
    if outcome.excinfo is None and outcome.get_result() is False:
        pytest.fail("test returned False (script-style failure signal)", pytrace=False)
