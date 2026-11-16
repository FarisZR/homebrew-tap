# FarisZR Homebrew tap

Homebrew packages for projects maintained by [FarisZR](https://github.com/FarisZR).

## Setup

Requires [Homebrew](https://brew.sh) 6 or newer. Current packages support Linux
x86_64 and ARM64.

```bash
brew update
brew tap fariszr/tap
brew trust fariszr/tap
```

## Install

Install the packages you want:

```bash
brew install --cask knocker-cli
brew install --cask komodo-agentic-cli
brew install --cask whisper-stt-gnome-extension
brew install --cask knocker-gnome
```

| Package | Command | Project and usage |
| --- | --- | --- |
| `knocker-cli` | `knocker` | [Knocker CLI](https://github.com/FarisZR/knocker-cli) |
| `komodo-agentic-cli` | `km` | [Komodo Agentic CLI](https://github.com/FarisZR/komodo-agentic-cli/blob/agentic-cli/bin/cli/README.md) |
| `whisper-stt-gnome-extension` | GNOME dictation shortcut | [Whisper STT GNOME Extension](https://github.com/FarisZR/whisper-stt-gnome-extension) |
| `knocker-gnome` | GNOME Quick Settings | [Knocker GNOME Extension](https://github.com/FarisZR/knocker-gnome) |

The dictation extension requires GNOME Shell 49, 50 or 51. It installs into
`~/.local/share/gnome-shell/extensions/whisper-stt@fariszr.com` for the user
running Homebrew. Install your distribution's GStreamer tools/plugins (including
PulseAudio), curl, and `canberra-gtk-play` for sounds. Log out and back in, then run:

```bash
gnome-extensions enable whisper-stt@fariszr.com
gnome-extensions prefs whisper-stt@fariszr.com
```

Configure your speech-to-text endpoint in preferences. The package uses rolling
builds identified by full Git commit hashes. If the extension is already installed
manually, move its directory out of the way before installing the cask. Homebrew
manages that directory through installation, upgrades, and uninstall.

The Knocker extension supports GNOME Shell 48–51 and installs into
`~/.local/share/gnome-shell/extensions/Knocker@fariszr.com`. It requires a configured
`knocker.service` user unit; installing the extension does not change the service.
After installation, log out/in and run `gnome-extensions enable Knocker@fariszr.com`.
Use `gnome-extensions prefs Knocker@fariszr.com` for extension preferences. Back up
any existing manual extension directory before the first cask installation.
Commit builds and version releases are both synchronized automatically.

## Update

```bash
brew update
brew upgrade
```

This upgrades your installed Homebrew packages.
After upgrading either GNOME extension, log out and back in to load the new build.
