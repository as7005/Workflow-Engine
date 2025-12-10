# app/workflows.py
import asyncio
from typing import Dict, Tuple

# Example node functions. Each must accept state: dict and return dict (state changes).
def extract_func(state: Dict) -> Dict:
    s = dict(state)
    s.setdefault("rows_processed", 0)
    s["extracted"] = True
    s["rows_processed"] += 10
    return s

def transform_func(state: Dict) -> Dict:
    s = dict(state)
    s["transformed"] = True
    s["rows_processed"] = s.get("rows_processed", 0) + 90
    return s

async def async_save_func(state: Dict) -> Dict:
    # example async node: simulate IO
    await asyncio.sleep(0.1)
    s = dict(state)
    s["saved"] = True
    return s

# Registry
NODE_REGISTRY = {
    "extract_func": extract_func,
    "transform_func": transform_func,
    "save_func": async_save_func,
}
