#!/usr/bin/env python3
"""Synchronize casks with their latest complete published releases."""

import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "komodo-agentic-cli": {
        "repo": "FarisZR/komodo-agentic-cli",
        "name": "Komodo Agentic CLI",
        "description": "Agent-oriented CLI for Komodo deployment management",
        "assets": {"arm64_linux": "km-aarch64", "x86_64_linux": "km-x86_64"},
    },
    "knocker-cli": {
        "repo": "FarisZR/knocker-cli",
        "name": "Knocker CLI",
        "description": "Keep your external IP address whitelisted",
        "assets": {
            "arm64_linux": "knocker-cli_Linux_arm64.tar.gz",
            "x86_64_linux": "knocker-cli_Linux_x86_64.tar.gz",
        },
    },
    "whisper-stt-gnome-extension": {
        "repo": "FarisZR/whisper-stt-gnome-extension",
        "name": "Whisper STT GNOME Extension",
        "description": "GNOME dictation using an OpenAI-compatible speech-to-text endpoint",
        "assets": {"portable": "whisper-stt-gnome-extension.tar.gz"},
        "extension": {
            "uuid": "whisper-stt@fariszr.com",
            "tags": "commits",
            "requirements": [
                "Requires GNOME Shell 49/50/51, GStreamer tools/plugins (including pulseaudio),",
                "curl, and libcanberra's canberra-gtk-play for notification sounds.",
            ],
            "configuration": "Configure your transcription endpoint in:",
        },
    },
    "knocker-gnome": {
        "conflicts_with": "knocker-gnome@main",
        "repo": "FarisZR/knocker-gnome",
        "name": "Knocker GNOME Extension",
        "description": "GNOME Quick Settings for the Knocker port knocking service",
        "assets": {"portable": "knocker-gnome.tar.gz"},
        "extension": {
            "uuid": "Knocker@fariszr.com",
            "tags": "versions",
            "requirements": [
                "Requires GNOME Shell 48/49/50/51 and a configured knocker.service user unit.",
                "Install the CLI separately: brew install --cask fariszr/tap/knocker-cli",
            ],
            "configuration": "Configure extension preferences in:",
        },
    },
}
PROJECTS["knocker-gnome@main"] = {
    **PROJECTS["knocker-gnome"],
    "name": "Knocker GNOME Extension (main)",
    "release": "@main",
    "conflicts_with": "knocker-gnome",
    "extension": {**PROJECTS["knocker-gnome"]["extension"], "tags": "commits"},
}


def github_json(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "FarisZR-tap"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{path}", headers=headers)
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def latest_release(repo, tag=None):
    if not tag:
        return github_json(f"{repo}/releases/latest")
    ref = github_json(f"{repo}/git/ref/tags/{quote(tag, safe='')}")
    commit = ref.get("object", {})
    if commit.get("type") != "commit" or not re.fullmatch(r"[0-9a-f]{40}", commit.get("sha", "")):
        raise ValueError("Main channel must reference a commit")
    return github_json(f"{repo}/releases/tags/build-{commit['sha']}")


def asset_checksum(asset, expected_url):
    if asset.get("browser_download_url") != expected_url or asset.get("state") != "uploaded":
        raise ValueError("Unexpected or incomplete release asset")
    digest = asset.get("digest") or ""
    if re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        return digest.removeprefix("sha256:")
    # Older assets may not have GitHub's server-calculated digest. Download only
    # the fixed public release URL, without sending the GitHub token to it.
    checksum = hashlib.sha256()
    with urlopen(Request(expected_url, headers={"User-Agent": "FarisZR-tap"}), timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            checksum.update(chunk)
    return checksum.hexdigest()


def render_cask(token, release):
    project = PROJECTS[token]
    tag = release.get("tag_name", "")
    main_channel = project.get("release") == "@main"
    if release.get("draft") or bool(release.get("prerelease")) != main_channel:
        raise ValueError("Only published stable releases belong in the default channel; @main requires a prerelease")
    extension = project.get("extension")
    commit_tag = re.fullmatch(r"build-[0-9a-f]{40}", tag)
    version_tag = re.fullmatch(r"v?\d+\.\d+\.\d+(?:[.+-][A-Za-z0-9.-]+)?", tag)
    accepts_version = not extension or extension["tags"] == "versions"
    accepts_commit = extension and extension["tags"] == "commits"
    if not ((accepts_commit and commit_tag) or (accepts_version and version_tag)):
        raise ValueError(f"Unsupported release tag: {tag!r}")
    version = tag.removeprefix("build-") if commit_tag else tag.removeprefix("v")
    assets = {asset["name"]: asset for asset in release["assets"]}
    checksums = {}
    for architecture, name in project["assets"].items():
        if name not in assets:
            raise ValueError(f"{project['repo']} {tag}: missing {name}; release build may still be running")
        url = f"https://github.com/{project['repo']}/releases/download/{tag}/{name}"
        checksums[architecture] = asset_checksum(assets[name], url)
    if extension:
        uuid = extension["uuid"]
        asset_name = project["assets"]["portable"]
        return "\n".join([
            f'cask "{token}" do',
            f'  version "{version}"',
            f'  sha256 "{checksums["portable"]}"',
            "",
            f'  url "https://github.com/{project["repo"]}/releases/download/{tag}/{asset_name}"',
            f'  name "{project["name"]}"',
            f'  desc "{project["description"]}"',
            f'  homepage "https://github.com/{project["repo"]}"',
            "",
            "  depends_on :linux",
            *([f'  conflicts_with cask: "{project["conflicts_with"]}"'] if "conflicts_with" in project else []),
            "",
            f'  artifact "{uuid}",',
            f'           target: "~/.local/share/gnome-shell/extensions/{uuid}"',
            "",
            "  caveats <<~EOS",
            *[f"    {line}" for line in extension["requirements"]],
            "    Log out and back in, then enable the extension:",
            f"      gnome-extensions enable {uuid}",
            f"    {extension['configuration']}",
            f"      gnome-extensions prefs {uuid}",
            "    After upgrading, log out and back in to load the new build.",
            "  EOS",
            "end", "",
        ])
    arch = 'arch arm: "aarch64", intel: "x86_64"' if token == "komodo-agentic-cli" else 'arch arm: "arm64", intel: "x86_64"'
    asset_name = 'km-#{arch}' if token == "komodo-agentic-cli" else 'knocker-cli_Linux_#{arch}.tar.gz'
    lines = [
        f'cask "{token}" do',
        f"  {arch}",
        "",
        f'  version "{version}"',
        f'  sha256 arm64_linux:  "{checksums["arm64_linux"]}",',
        f'         x86_64_linux: "{checksums["x86_64_linux"]}"',
        "",
        f'  url "https://github.com/{project["repo"]}/releases/download/{tag}/{asset_name}"',
        f'  name "{project["name"]}"',
        f'  desc "{project["description"]}"',
        f'  homepage "https://github.com/{project["repo"]}"',
        "",
        "  depends_on :linux",
    ]
    if token == "komodo-agentic-cli":
        lines.extend(["  container type: :naked", "", '  binary "km-#{arch}", target: "km"'])
    else:
        lines.extend(["", '  binary "knocker"'])
    lines.extend(["end", ""])
    return "\n".join(lines)


def main():
    # Render everything before writing: an incomplete release never partially
    # updates the tap. Every trigger re-reads all latest releases, so old or
    # coalesced dispatch events cannot select an old tag or arbitrary repository.
    rendered = {token: render_cask(token, latest_release(project["repo"], project.get("release")))
                for token, project in PROJECTS.items()}
    for token, content in rendered.items():
        path = ROOT / "Casks" / f"{token}.rb"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Synchronized {token}")


if __name__ == "__main__":
    main()
