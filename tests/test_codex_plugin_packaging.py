from __future__ import annotations

import json
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "jucho-kun"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SUBMISSION = ROOT / "docs" / "OPENAI_PLUGIN_DIRECTORY_SUBMISSION.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_and_skill_package() -> None:
    manifest = load_json(MANIFEST)
    assert manifest["name"] == "jucho-kun"
    assert manifest["version"] == "1.1.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["license"] == "MIT"
    assert manifest["repository"] == "https://github.com/signal-yield/jucho-kun"
    assert (PLUGIN / "skills" / "jucho-kun" / "SKILL.md").is_file()


def test_manifest_images_are_square_pngs() -> None:
    manifest = load_json(MANIFEST)
    for field in ("composerIcon", "logo"):
        image_path = PLUGIN / manifest["interface"][field].removeprefix("./")
        data = image_path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert width == height == 512


def test_marketplace_points_to_plugin() -> None:
    marketplace = load_json(MARKETPLACE)
    entry = marketplace["plugins"][0]
    assert entry["name"] == "jucho-kun"
    assert entry["source"] == {"source": "local", "path": "./plugins/jucho-kun"}
    assert entry["policy"] == {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }


def test_packaged_skill_matches_canonical() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/sync_codex_plugin_skill.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_public_policy_pages_and_submission_materials() -> None:
    manifest = load_json(MANIFEST)
    for path in ("privacy.html", "terms.html", "support.html"):
        assert (ROOT / "docs" / path).is_file()
    assert manifest["interface"]["privacyPolicyURL"].endswith("/privacy.html")
    assert manifest["interface"]["termsOfServiceURL"].endswith("/terms.html")
    text = SUBMISSION.read_text(encoding="utf-8")
    assert text.count("### Positive Test ") == 5
    assert text.count("### Negative Test ") == 3
    assert "https://platform.openai.com/plugins" in text
    assert "Submit for Review" in text


def test_guardrails_are_visible() -> None:
    text = "\n".join(
        [
            MANIFEST.read_text(encoding="utf-8"),
            (PLUGIN / "skills" / "jucho-kun" / "SKILL.md").read_text(encoding="utf-8"),
            SUBMISSION.read_text(encoding="utf-8"),
        ]
    )
    for required in ["一次スクリーニング", "宅地建物取引士", "最終確認"]:
        assert required in text
