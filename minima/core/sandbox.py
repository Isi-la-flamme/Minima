import builtins

SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "str": str,
    "int": int,
    "float": float,
    "dict": dict,
    "list": list,
}

def run_sandboxed(code: str, globals_dict=None):
    env = {"__builtins__": SAFE_BUILTINS}
    if globals_dict:
        env.update(globals_dict)
    exec(code, env)
    return env
