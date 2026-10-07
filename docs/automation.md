# Release automation

## Repository layout

| Path | Role |
| --- | --- |
| `Casks/` | Generated Homebrew package definitions |
| `scripts/update_casks.py` | Reads GitHub releases and renders casks |
| `tests/test_update_casks.py` | Release validation tests |
| `cask_renames.json` | Maps retired cask names to their replacements |
| `.github/workflows/sync.yml` | Updates and commits release definitions |
| `.github/workflows/test.yml` | Validates the updater and installs packages |
| `docs/` | Maintainer setup and operating instructions |

The GitHub repository is `FarisZR/homebrew-tap`. Homebrew identifies it as
`fariszr/tap`; its default GitHub lookup adds the `homebrew-` prefix.
Packages are downloaded directly from each source repository's GitHub Releases.

## Source repositories

| Package | Source | ARM64 asset | x86_64 asset |
| --- | --- | --- | --- |
| `knocker-cli` | `FarisZR/knocker-cli` | `knocker-cli_Linux_arm64.tar.gz` | `knocker-cli_Linux_x86_64.tar.gz` |
| `komodo-agentic-cli` | `FarisZR/komodo-agentic-cli` | `km-aarch64` | `km-x86_64` |
| `whisper-stt-gnome-extension` | `FarisZR/whisper-stt-gnome-extension` | `whisper-stt-gnome-extension.tar.gz` | Same portable asset |

Knocker's `.goreleaser.yml` uses GoReleaser v2, fixes
`project_name: knocker-cli`, maps `amd64` to `x86_64` in archive names, and
builds the executable `knocker` with `CGO_ENABLED=0`. Its other release assets,
including DEB/RPM packages and `checksums.txt`, are independent of this tap.

Knocker's `.github/workflows/release.yml` runs when a release is published,
or manually with an existing release tag. It checks out that tag and runs
`goreleaser release --clean --skip=announce`. The `update-homebrew` job
depends on successful publication, then dispatches the tap's `sync.yml`.

Komodo's separate `.github/workflows/update-homebrew.yml` observes the
completion of the `Release CLI` workflow. It dispatches only after a successful
release or manual build from the same source repository. It can also be run
manually. The observer checks out no source and executes no release artifacts.
The original `release-cli.yml` pipeline is unchanged.

The extension's `.github/workflows/build.yml` tests and packages each pull request
and push to `main`. Successful current-main builds publish immutable bundles under
`build-<full commit hash>` and mark the release latest. Pull requests only build;
they never publish or dispatch. A separate notification job runs after publication.
Manual builds on `main` use the same process. GNOME metadata uses the commit count
as its numeric version and the full hash as `version-name`.

All three notifications POST to:

```text
repos/FarisZR/homebrew-tap/actions/workflows/sync.yml/dispatches
```

The request body is `{"ref":"main"}`. Authentication uses the source
repository's `TAP_GITHUB_TOKEN` secret; see [token setup](tokens.md).
Dispatch happens after build completion because release publication can precede
asset uploads.

## Tap synchronization

The `Sync release casks` workflow runs:

- On manual dispatch.
- At minute 17 every six hours (UTC).
- On pushes to `main` changing the updater or the sync workflow.

The sync job is restricted to `FarisZR/homebrew-tap`, runs on Ubuntu 24.04,
and has a 15-minute timeout. The concurrency group `sync-release-casks`
serializes updates without cancelling a running job.

Each run checks out `main`, tests the updater, generates casks, validates their
Ruby syntax, and commits changed files under `Casks/` to `main` as
`github-actions[bot]`. Unchanged releases produce no commit.

The updater queries GitHub's `releases/latest` endpoint for each configured
project. It accepts no caller-supplied repository, tag, or URL. Drafts and
prereleases are rejected. CLI tags must match the supported version pattern,
including stable suffixes such as `v2.2.0-agentic`. The extension accepts only
`build-` followed by a full 40-character lowercase commit hash and uses that hash
as its Homebrew version.

Each required asset must exist, have state `uploaded`, and use the expected
release URL. GitHub's SHA-256 asset digest is used when present; otherwise the
asset is downloaded and hashed without forwarding the GitHub token.
All casks are rendered before any are written, so a missing or invalid release
prevents updates to every package in that run.

Every trigger reads the current latest releases; a delayed notification cannot
supply an older version. A maintainer changing which GitHub release is marked
latest can still affect the selected version.

## Installation and compatibility

All casks declare `depends_on :linux` and support x86_64 and ARM64.
Knocker extracts its archive and links `knocker`. Komodo downloads a raw binary
using `container type: :naked` and links it as `km`.

Komodo uses the existing Ubuntu 24.04 GNU/Linux binaries, including their
glibc/OpenSSL runtime requirements. Packaging does not make these binaries
static or extend their distribution compatibility. Homebrew installation does
not install or restart Knocker's systemd service.

The extension is architecture independent. Its archive contains the directory
`whisper-stt@fariszr.com` with runtime modules, metadata, and compiled schemas.
Homebrew's directory artifact installs it under the invoking user's
`~/.local/share/gnome-shell/extensions/`. Homebrew owns directory replacement and
removal; it refuses to silently overwrite a manual installation. GNOME Shell
49/50 and system GStreamer tools/plugins, curl, and optional notification sound
support are still required. Log out and back in after installation or upgrade;
enable and configure the extension using `gnome-extensions`.

Synchronizing the tap makes releases available. Devices install those releases
when they run `brew update` followed by `brew upgrade`. Scheduling upgrades
on a device is separate from this repository's release automation.

## CI

The `Test tap` workflow runs on pushes to `main` and pull requests, with
read-only repository permissions and checkout credential persistence disabled.

Its updater job runs the Python release-validation suite and Ruby syntax checks.
Its installation matrix uses `ubuntu-24.04` and `ubuntu-24.04-arm`.
Each installation job verifies public tap discovery, then taps the checked-out
commit, grants trust, installs both packages by short name, runs `km --help`
and `knocker --help`, and uninstalls the casks. It also installs and reinstalls the extension, checks
its runtime modules and schemas, and verifies uninstall removes its directory.
These headless checks do not validate a live GNOME Shell session.

Adding a package requires extending the generator and installation checks;
see [maintenance](maintenance.md).
