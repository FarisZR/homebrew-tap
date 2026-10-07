import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("updater", Path(__file__).resolve().parents[1] / "scripts/update_casks.py")
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def release(token, tag=None):
    tag = tag or ("build-" + "b" * 40 if token == "whisper-stt-gnome-extension" else "v1.2.3")
    project = updater.PROJECTS[token]
    return {
        "tag_name": tag, "draft": False, "prerelease": False,
        "assets": [{"name": name, "state": "uploaded", "digest": "sha256:" + "a" * 64,
                    "browser_download_url": f"https://github.com/{project['repo']}/releases/download/{tag}/{name}"}
                   for name in project["assets"].values()],
    }


class ReleaseValidation(unittest.TestCase):
    def test_extension_version_is_commit_hash(self):
        cask = updater.render_cask("whisper-stt-gnome-extension", release("whisper-stt-gnome-extension"))
        self.assertIn('version "' + "b" * 40 + '"', cask)

    def test_extension_rejects_non_commit_versions(self):
        for tag in ["v1.2.3", "build-main", "build-abcdef0"]:
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, "tag"):
                updater.render_cask("whisper-stt-gnome-extension", release("whisper-stt-gnome-extension", tag))

    def test_extension_uses_one_portable_asset_and_user_extension_directory(self):
        cask = updater.render_cask("whisper-stt-gnome-extension", release("whisper-stt-gnome-extension"))
        self.assertIn('whisper-stt-gnome-extension.tar.gz"', cask)
        self.assertIn('sha256 "' + "a" * 64 + '"', cask)
        self.assertIn('artifact "whisper-stt@fariszr.com"', cask)
        self.assertIn('target: "~/.local/share/gnome-shell/extensions/whisper-stt@fariszr.com"', cask)
        self.assertIn('depends_on :linux', cask)
        self.assertNotIn('arch ', cask)
        self.assertNotIn('binary ', cask)

    def test_extension_missing_bundle_is_rejected(self):
        data = release("whisper-stt-gnome-extension")
        data["assets"] = []
        with self.assertRaisesRegex(ValueError, "missing whisper-stt-gnome-extension.tar.gz"):
            updater.render_cask("whisper-stt-gnome-extension", data)

    def test_extension_untrusted_url_is_rejected(self):
        data = release("whisper-stt-gnome-extension")
        data["assets"][0]["browser_download_url"] = "https://example.com/extension.tar.gz"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            updater.render_cask("whisper-stt-gnome-extension", data)

    def test_no_cli_changes_written_when_extension_bundle_is_incomplete(self):
        data = [release(token) for token in updater.PROJECTS]
        data[-1]["assets"] = []
        with patch.object(updater, "latest_release", side_effect=data), patch.object(Path, "write_text") as write:
            with self.assertRaisesRegex(ValueError, "missing"):
                updater.main()
            write.assert_not_called()

    def test_missing_architecture_is_rejected(self):
        data = release("knocker-cli")
        data["assets"].pop()
        with self.assertRaisesRegex(ValueError, "missing"):
            updater.render_cask("knocker-cli", data)

    def test_draft_and_prerelease_are_rejected(self):
        for flag in ["draft", "prerelease"]:
            data = release("knocker-cli")
            data[flag] = True
            with self.assertRaisesRegex(ValueError, "stable"):
                updater.render_cask("knocker-cli", data)

    def test_untrusted_url_is_rejected(self):
        data = release("knocker-cli")
        data["assets"][0]["browser_download_url"] = "https://example.com/binary"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            updater.render_cask("knocker-cli", data)

    def test_incomplete_upload_is_rejected(self):
        data = release("knocker-cli")
        data["assets"][0]["state"] = "new"
        with self.assertRaises(ValueError):
            updater.render_cask("knocker-cli", data)

    def test_tag_cannot_inject_ruby(self):
        with self.assertRaisesRegex(ValueError, "tag"):
            updater.render_cask("knocker-cli", release("knocker-cli", 'v1.2.3#{system("bad")}'))

    def test_agentic_tag_is_a_stable_release(self):
        cask = updater.render_cask("komodo-agentic-cli", release("komodo-agentic-cli", "v2.2.0-agentic"))
        self.assertIn('version "2.2.0-agentic"', cask)
        self.assertIn('binary "km-#{arch}", target: "km"', cask)

    def test_no_files_written_when_one_release_is_incomplete(self):
        first = release("komodo-agentic-cli")
        second = release("knocker-cli")
        second["assets"] = []
        with patch.object(updater, "latest_release", side_effect=[first, second]), patch.object(Path, "write_text") as write:
            with self.assertRaises(ValueError):
                updater.main()
            write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
