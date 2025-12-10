# app/workflows.py
import asyncio
from typing import Dict

# --------------------
# Example nodes
# --------------------
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
    await asyncio.sleep(0.1)
    s = dict(state)
    s["saved"] = True
    return s

# --------------------
# Code Review Mini-Agent nodes
# --------------------
def extract_functions(state: Dict) -> Dict:
    s = dict(state)
    s.setdefault("issues", 0)
    s.setdefault("quality_score", 0)
    s["functions_extracted"] = 5
    return s

def check_complexity(state: Dict) -> Dict:
    s = dict(state)
    s["complexity_score"] = s.get("functions_extracted", 0) * 2
    s["quality_score"] += max(0, 10 - s["complexity_score"])
    return s

def detect_issues(state: Dict) -> Dict:
    s = dict(state)
    s["issues_found"] = 5 - s.get("quality_score", 0)//2
    s["quality_score"] += max(0, 5 - s["issues_found"])
    return s

def suggest_improvements(state: Dict) -> Dict:
    s = dict(state)
    s["suggestions"] = ["Refactor function A", "Simplify loop in function B"]
    s["quality_score"] += 2
    return s

async def review_wait(state: Dict) -> Dict:
    """
    Looping node: just a wait to simulate async check or delay.
    In the engine, this node can be used to loop until quality_score >= threshold.
    """
    await asyncio.sleep(0.1)
    return dict(state)

# --------------------
# Node registry
# --------------------
NODE_REGISTRY = {
    "extract_func": extract_func,
    "transform_func": transform_func,
    "save_func": async_save_func,
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_issues": detect_issues,
    "suggest_improvements": suggest_improvements,
    "review_wait": review_wait,
}
