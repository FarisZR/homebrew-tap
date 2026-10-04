#!/usr/bin/env python3
"""Synchronize the two casks with their latest published stable releases."""

import hashlib
import json
import os
from pathlib import Path
import re
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
}


def latest_release(repo):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "FarisZR-tap"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/{repo}/releases/latest", headers=headers)
    with urlopen(request, timeout=60) as response:
        return json.load(response)


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
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Only published stable releases can enter the tap")
    if not re.fullmatch(r"v?\d+\.\d+\.\d+(?:[.+-][A-Za-z0-9.-]+)?", tag):
        raise ValueError(f"Unsupported release tag: {tag!r}")
    version = tag.removeprefix("v")
    assets = {asset["name"]: asset for asset in release["assets"]}
    checksums = {}
    for architecture, name in project["assets"].items():
        if name not in assets:
            raise ValueError(f"{project['repo']} {tag}: missing {name}; release build may still be running")
        url = f"https://github.com/{project['repo']}/releases/download/{tag}/{name}"
        checksums[architecture] = asset_checksum(assets[name], url)
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
    # updates the tap. Every trigger re-reads both latest releases, so old or
    # coalesced dispatch events cannot select an old tag or arbitrary repository.
    rendered = {token: render_cask(token, latest_release(project["repo"]))
                for token, project in PROJECTS.items()}
    for token, content in rendered.items():
        path = ROOT / "Casks" / f"{token}.rb"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Synchronized {token}")


if __name__ == "__main__":
    main()
