import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("updater", Path(__file__).resolve().parents[1] / "scripts/update_casks.py")
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def release(token, tag=None):
    tag = tag or ("build-" + "b" * 40 if "extension" in updater.PROJECTS[token] and token != "knocker-gnome" else "v1.2.3")
    project = updater.PROJECTS[token]
    return {
        "tag_name": tag, "draft": False, "prerelease": token.endswith("@main"),
        "assets": [{"name": name, "state": "uploaded", "digest": "sha256:" + "a" * 64,
                    "browser_download_url": f"https://github.com/{project['repo']}/releases/download/{tag}/{name}"}
                   for name in project["assets"].values()],
    }


class ReleaseValidation(unittest.TestCase):
    def test_jabra_tracks_commits_without_a_preferences_window(self):
        cask = updater.render_cask("jabra-gnome-integration", release("jabra-gnome-integration"))
        self.assertIn('version "' + "b" * 40 + '"', cask)
        self.assertIn('jabra-gnome-integration.tar.gz"', cask)
        self.assertIn('artifact "jabra-integration@fariszr.com"', cask)
        self.assertIn('GNOME Shell 48/49/50/51', cask)
        self.assertIn('jabridge setup', cask)
        self.assertNotIn('gnome-extensions prefs', cask)
        with self.assertRaisesRegex(ValueError, "tag"):
            updater.render_cask("jabra-gnome-integration", release("jabra-gnome-integration", "v1.2.3"))

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
        data[list(updater.PROJECTS).index("whisper-stt-gnome-extension")]["assets"] = []
        with patch.object(updater, "latest_release", side_effect=data), patch.object(Path, "write_text") as write:
            with self.assertRaisesRegex(ValueError, "missing"):
                updater.main()
            write.assert_not_called()

    def test_knocker_stable_and_main_channels_use_separate_versions_and_conflict(self):
        for token, tag in [("knocker-gnome", "v1.1.0"), ("knocker-gnome@main", "build-" + "b" * 40)]:
            with self.subTest(token=token):
                cask = updater.render_cask(token, release(token, tag))
                self.assertIn(f"/download/{tag}/knocker-gnome.tar.gz", cask)
                self.assertIn('artifact "Knocker@fariszr.com"', cask)
                self.assertIn('target: "~/.local/share/gnome-shell/extensions/Knocker@fariszr.com"', cask)
                self.assertIn("GNOME Shell 48/49/50/51", cask)
                other = "knocker-gnome" if token.endswith("@main") else "knocker-gnome@main"
                self.assertIn(f'conflicts_with cask: "{other}"', cask)
                self.assertNotIn("whisper", cask)

    def test_knocker_stable_rejects_commit_builds_and_prereleases(self):
        with self.assertRaisesRegex(ValueError, "tag"):
            updater.render_cask("knocker-gnome", release("knocker-gnome", "build-" + "b" * 40))
        data = release("knocker-gnome")
        data["prerelease"] = True
        with self.assertRaisesRegex(ValueError, "stable"):
            updater.render_cask("knocker-gnome", data)
        with self.assertRaisesRegex(ValueError, "tag"):
            updater.render_cask("knocker-gnome@main", release("knocker-gnome@main", "v1.1.0"))

    def test_main_channel_resolves_moving_tag_to_immutable_release(self):
        commit = "c" * 40
        expected = release("knocker-gnome@main", "build-" + commit)
        with patch.object(updater, "github_json", side_effect=[{"object": {"type": "commit", "sha": commit}}, expected]) as fetch:
            self.assertEqual(updater.latest_release("FarisZR/knocker-gnome", "@main"), expected)
            self.assertEqual(fetch.call_args_list[0].args, ("FarisZR/knocker-gnome/git/ref/tags/%40main",))
            self.assertEqual(fetch.call_args_list[1].args, (f"FarisZR/knocker-gnome/releases/tags/build-{commit}",))

    def test_main_channel_rejects_untrusted_tag_target(self):
        with patch.object(updater, "github_json", return_value={"object": {"type": "commit", "sha": "main"}}):
            with self.assertRaisesRegex(ValueError, "reference a commit"):
                updater.latest_release("FarisZR/knocker-gnome", "@main")

    def test_knocker_extension_missing_asset_or_untrusted_tag_is_rejected(self):
        data = release("knocker-gnome")
        data["assets"] = []
        with self.assertRaisesRegex(ValueError, "missing knocker-gnome.tar.gz"):
            updater.render_cask("knocker-gnome", data)
        for tag in ["main", "build-short", 'v1.0.0#{system("bad")}']:
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, "tag"):
                updater.render_cask("knocker-gnome", release("knocker-gnome", tag))

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
