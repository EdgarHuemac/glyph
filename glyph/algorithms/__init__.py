import importlib
import pkgutil
import os
from .base import Algorithm
from typing import List, Optional

_registry = []


def register(cls):
    """Decorator to register an algorithm class."""
    instance = cls()
    _registry.append(instance)
    return cls


def get_all(mode=None, category=None, exclude=None):
    results = list(_registry)
    if mode:
        results = [a for a in results if a.mode in (mode, "both")]
    if category:
        results = [a for a in results if a.category == category]
    if exclude:
        excl = [x.strip().lower() for x in exclude.split(",")]
        results = [a for a in results if a.name.lower() not in excl]
    return results


def _autodiscover():
    pkg_dir = os.path.dirname(__file__)
    for _, module_name, _ in pkgutil.iter_modules([pkg_dir]):
        if module_name not in ("__init__", "base"):
            importlib.import_module(f".{module_name}", package=__name__)


_autodiscover()