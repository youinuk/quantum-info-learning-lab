"""Keep page modules compatible with a long-running Streamlit process."""

from __future__ import annotations

import importlib
import inspect
from types import ModuleType
from typing import Collection, Mapping


def ensure_module_api(
    module: ModuleType,
    *,
    minimum_version: int = 0,
    required_attributes: Collection[str] = (),
    required_parameters: Mapping[str, Collection[str]] | None = None,
) -> ModuleType:
    """Reload a cached module only when the page needs a newer public API.

    ``minimum_version`` remains in the signature so pages already loaded by a
    development server can call this newer implementation safely. New code
    should describe the API through attributes and function parameters.
    """
    required_parameters = required_parameters or {}

    def api_is_current(candidate: ModuleType) -> bool:
        if any(not hasattr(candidate, name) for name in required_attributes):
            return False
        for function_name, parameters in required_parameters.items():
            function = getattr(candidate, function_name, None)
            if function is None:
                return False
            if not set(parameters) <= set(inspect.signature(function).parameters):
                return False
        return True

    if not api_is_current(module):
        module = importlib.reload(module)
    if not api_is_current(module):
        required = ", ".join(required_attributes) or "the requested API"
        raise RuntimeError(f"{module.__name__} does not provide {required}.")
    return module
