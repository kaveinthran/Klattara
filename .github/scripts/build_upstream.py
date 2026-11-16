"""Run the unmodified builder using explicit, architecture-matched interpreters.

GitHub setup-python does not guarantee that Windows py.exe registrations point
to its interpreters. Route the builder's two launcher calls, retaining its
Cargo builds, driver tests, error handling and package assembly.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import types


def route_command(command, python_x64, python_x86):
    command = list(command)
    if command and str(command[0]).lower() in {"py", "py.exe"}:
        interpreters = {"-3-64": str(python_x64), "-3-32": str(python_x86)}
        if len(command) < 3 or command[1] not in interpreters:
            raise ValueError("Unexpected upstream Python-launcher command; review required")
        return [interpreters[command[1]], *command[2:]]
    return command


def build(source, python_x64, python_x86):
    pins = json.loads((Path(__file__).resolve().parent.parent / "nvda-test-sources.json").read_text(encoding="utf-8"))
    for architecture, executable, width in (("x64", python_x64, 8), ("x86", python_x86, 4)):
        version = tuple(int(part) for part in pins[architecture]["python"].split("."))
        subprocess.run([str(executable), "-c", "import ctypes, sys; "
                        f"assert ctypes.sizeof(ctypes.c_void_p) == {width}; "
                        f"assert sys.version_info[:2] == {version!r}"], check=True)
    for folder in ("nvda", "nvda-release-2025.1"):
        if not (source / folder / "source/synthDriverHandler.py").is_file():
            raise ValueError(f"Required official NVDA source missing: {folder}")
    path = source / "src/plat/nvda/build.py"
    spec = importlib.util.spec_from_file_location("klattara_upstream_builder", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def dispatch(command, *args, **kwargs):
        return subprocess.run(route_command(command, python_x64, python_x86), *args, **kwargs)

    # Change only this imported module's subprocess reference, not the stdlib.
    module.subprocess = types.SimpleNamespace(run=dispatch)
    module.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--python-x64", type=Path, required=True)
    parser.add_argument("--python-x86", type=Path, required=True)
    args = parser.parse_args()
    build(args.source.resolve(), args.python_x64.resolve(), args.python_x86.resolve())


if __name__ == "__main__":
    main()
