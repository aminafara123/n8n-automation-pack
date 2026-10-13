#!/usr/bin/env python3
"""Structural validator for n8n workflow exports.

No network, no n8n install. Checks what import actually needs:
  - top-level object with a `nodes` array and a `connections` object
  - every node has id, name, type, typeVersion, position, parameters
  - node names are unique and no node type is empty
  - every connection source + target names a node that exists

Run:  python validate.py [workflows_dir]   (exit 0 = all valid)
"""
import json
import sys
from pathlib import Path

NODE_KEYS = ("id", "name", "type", "typeVersion", "position", "parameters")


def validate_workflow(path: Path) -> list[str]:
    """Return a list of human-readable errors for one workflow file ([] = valid)."""
    errors: list[str] = []
    try:
        wf = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return [f"could not parse JSON: {e}"]

    if not isinstance(wf, dict):
        return ["top level is not a JSON object"]
    if not isinstance(wf.get("nodes"), list) or not wf["nodes"]:
        errors.append("missing non-empty 'nodes' array")
    if not isinstance(wf.get("connections"), dict):
        errors.append("missing 'connections' object")

    names: set[str] = set()
    for i, node in enumerate(wf.get("nodes") or []):
        label = node.get("name", f"#{i}") if isinstance(node, dict) else f"#{i}"
        if not isinstance(node, dict):
            errors.append(f"node {label}: not an object")
            continue
        for key in NODE_KEYS:
            if key not in node:
                errors.append(f"node {label}: missing '{key}'")
        if not str(node.get("type", "")).strip():
            errors.append(f"node {label}: empty 'type'")
        pos = node.get("position")
        if not (isinstance(pos, list) and len(pos) == 2):
            errors.append(f"node {label}: 'position' must be [x, y]")
        name = node.get("name")
        if name in names:
            errors.append(f"duplicate node name: {name!r}")
        if name is not None:
            names.add(name)

    # connections must only reference existing node names (source and target)
    for src, outputs in (wf.get("connections") or {}).items():
        if src not in names:
            errors.append(f"connection source {src!r} is not a node")
        if not isinstance(outputs, dict):
            errors.append(f"connection {src!r}: outputs not an object")
            continue
        for out_type, branches in outputs.items():
            for branch in branches or []:
                for conn in branch or []:
                    target = (conn or {}).get("node")
                    if target not in names:
                        errors.append(
                            f"connection {src!r} -> {target!r} ({out_type}): target is not a node"
                        )
    return errors


def validate_dir(workflows_dir: Path) -> dict[Path, list[str]]:
    files = sorted(workflows_dir.glob("*.json"))
    return {f: validate_workflow(f) for f in files}


def main(argv: list[str]) -> int:
    workflows_dir = Path(argv[1]) if len(argv) > 1 else Path(__file__).parent / "workflows"
    results = validate_dir(workflows_dir)
    if not results:
        print(f"no workflow JSON files found in {workflows_dir}")
        return 1
    ok = True
    for path, errors in results.items():
        if errors:
            ok = False
            print(f"FAIL {path.name}")
            for e in errors:
                print(f"       - {e}")
        else:
            print(f"OK   {path.name}")
    print(f"\n{sum(not e for e in results.values())}/{len(results)} workflows valid")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
