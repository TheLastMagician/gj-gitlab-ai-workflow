from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def import_order_approval():
    root = Path(__file__).resolve().parent
    module_path = root / "demo-project" / "src" / "order_approval.py"
    spec = importlib.util.spec_from_file_location("order_approval", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
