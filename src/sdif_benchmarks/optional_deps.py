"""Helpers for loading optional benchmark dependencies."""

from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType


def optional_module(name: str) -> ModuleType | None:
    """Return an optional module when importable, otherwise None."""
    if importlib.util.find_spec(name) is None:
        return None
    return importlib.import_module(name)
