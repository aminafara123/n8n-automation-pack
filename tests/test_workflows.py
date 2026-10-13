"""Test gate: every workflow in workflows/ must be structurally valid for n8n import.
Runs fully offline. `pytest -q` must pass with no network and no credentials."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from validate import validate_workflow  # noqa: E402

WORKFLOWS = sorted((ROOT / "workflows").glob("*.json"))


def test_pack_has_five_workflows():
    assert len(WORKFLOWS) == 5, f"expected 5 workflows, found {len(WORKFLOWS)}"


@pytest.mark.parametrize("path", WORKFLOWS, ids=lambda p: p.name)
def test_workflow_is_valid(path):
    errors = validate_workflow(path)
    assert not errors, f"{path.name} has structural errors:\n  " + "\n  ".join(errors)
