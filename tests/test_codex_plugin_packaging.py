from __future__ import annotations

import json
import struct
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "jucho-kun"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
SUBMISSION = ROOT / "docs" / "OPENAI_PLUGIN_DIRECTORY_SUBMISSION.md"
CANONICAL_SKILL = ROOT / "skills" / "jucho-kun" / "SKILL.md"
PACKAGED_SKILL = PLUGIN / "skills" / "jucho-kun" / "SKILL.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_and_skill_package() -> None:
    manifest = load_json(MANIFEST)
    assert manifest["name"] == "jucho-kun"
    assert manifest["version"] == "1.1.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["license"] == "MIT"
    assert manifest["repository"] == "https://github.com/signal-yield/jucho-kun"
    assert PACKAGED_SKILL.is_file()


def test_listing_metadata_limits_and_urls() -> None:
    manifest = load_json(MANIFEST)
    interface = manifest["interface"]
    assert len(interface["displayName"]) <= 30
    assert len(interface["shortDescription"]) <= 30
    assert len(interface["longDescription"]) <= 4000
    assert len(interface["defaultPrompt"]) <= 3
    for prompt in interface["defaultPrompt"]:
        assert len(prompt) <= 128
    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        parsed = urlparse(interface[field])
        assert parsed.scheme == "https"
        assert parsed.netloc


def test_manifest_images_are_square_pngs() -> None:
    manifest = load_json(MANIFEST)
    for field in ("composerIcon", "logo"):
        image_path = PLUGIN / manifest["interface"][field].removeprefix("./")
        assert image_path.is_file()
        data = image_path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        width, height = struct.unpack(">II", data[16:24])
        assert width == height == 512


def test_packaged_skill_is_byte_identical_to_canonical() -> None:
    assert PACKAGED_SKILL.read_bytes() == CANONICAL_SKILL.read_bytes()


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


def test_untrusted_external_content_guardrails_are_visible() -> None:
    text = PACKAGED_SKILL.read_text(encoding="utf-8")
    for required in [
        "未信頼データ",
        "操作指示として扱わない",
        "秘密情報・認証情報",
        "権限のない資料収集",
        "出典URL、確認日、確認済み／要確認",
    ]:
        assert required in text


def test_environment_fallback_policy_is_visible() -> None:
    text = PACKAGED_SKILL.read_text(encoding="utf-8")
    for required in [
        "Web検索が利用できない場合",
        "Excel生成が利用できない場合",
        "Markdown表またはCSV向けデータ",
        "未実施項目と理由",
        "常に存在するとは仮定しない",
    ]:
        assert required in text


def test_public_descriptions_do_not_use_overstated_claims() -> None:
    public_text = "\n".join(
        [
            MANIFEST.read_text(encoding="utf-8"),
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
            SUBMISSION.read_text(encoding="utf-8"),
            (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"),
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"),
        ]
    )
    forbidden = [
        "完全自動取得",
        "住所だけで完了",
        "住所を入力するだけ",
        "1 hour",
        "few minutes",
        "fetches publicly available data",
        "crawls municipal sites",
    ]
    for phrase in forbidden:
        assert phrase not in public_text
