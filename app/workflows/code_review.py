NODE_REGISTRY = {}


def tool(name):
    def wrap(fn):
        NODE_REGISTRY[name] = fn
        return fn
    return wrap


@tool("extract")
def extract_functions(state):
    code = state.get("code", "")
    functions = code.count("def ")
    return {"functions": functions}


@tool("check_complexity")
def check_complexity(state):
    complexity = state.get("functions", 0) * 2
    return {"complexity": complexity}


@tool("detect_issues")
def detect_issues(state):
    issues = max(1, int(state.get("complexity", 0) / 3))
    return {"issues": issues}


@tool("suggest_improvements")
def suggest(state):
    score = max(0, 100 - (state.get("issues", 0) * 10))
    return {"quality_score": score}
