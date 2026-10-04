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
```

| Package | Command | Project and usage |
| --- | --- | --- |
| `knocker-cli` | `knocker` | [Knocker CLI](https://github.com/FarisZR/knocker-cli) |
| `komodo-agentic-cli` | `km` | [Komodo Agentic CLI](https://github.com/FarisZR/komodo-agentic-cli/blob/agentic-cli/bin/cli/README.md) |

## Update

```bash
brew update
brew upgrade
```

This upgrades your installed Homebrew packages.
