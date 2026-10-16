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
brew install --cask gseek
```

| Package | Command | Project and usage |
| --- | --- | --- |
| `knocker-cli` | `knocker` | [Knocker CLI](https://github.com/FarisZR/knocker-cli) |
| `komodo-agentic-cli` | `km` | [Komodo Agentic CLI](https://github.com/FarisZR/komodo-agentic-cli/blob/agentic-cli/bin/cli/README.md) |
| `whisper-stt-gnome-extension` | GNOME dictation shortcut | [Whisper STT GNOME Extension](https://github.com/FarisZR/whisper-stt-gnome-extension) |
| `gseek` | Native app and GNOME overview search | [GSeek](https://github.com/FarisZR/GSeek) |

The dictation extension requires GNOME Shell 49 or 50. It installs into
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

## GSeek

GSeek targets GNOME 51 (Fedora Workstation 45 and Ubuntu 26.10), on x86-64 and
ARM64. It uses your desktop’s GTK4, libadwaita, and LocalSearch libraries. The cask
registers the native app, background activation, and search provider.
Administrator permission is needed for the small system provider registration
under `/usr/local/share`.

Open GSeek from the application menu, choose folders, and select Download & Start.
The 865 MB EmbeddingGemma 2 model and selected official upstream runtime download
automatically. CPU, Vulkan, and NVIDIA CUDA are supported without an SDK or
inference compilation; AMD GPUs use Vulkan. Downloads are version-pinned and
checksum-verified.

GSeek reuses installed system readers: FFmpeg for media, Poppler utilities for
PDFs, and unzip for Office documents. It does not install a duplicate Homebrew
media stack. The cask requests zero formulas on hosts with OpenSSL 3; hosts missing
that ABI receive only its compatibility dependency. Setup and Preferences show
available formats, and missing readers produce system-install/retry guidance.
Folders must also be enabled in GNOME Search Locations. Setup replaces the Files
search provider after inference is validated.

```bash
brew upgrade --cask gseek
brew uninstall --cask gseek
```

Updates keep your settings and index. Uninstallation restores the previous Files
provider setting and preserves the library for a later reinstall. See GSeek’s
README for supported hardware, privacy, and current limits.

## Update

```bash
brew update
brew upgrade
```

This upgrades your installed Homebrew packages.
After upgrading the dictation extension, log out and back in to load the new build.
