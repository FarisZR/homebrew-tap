# FarisZR Homebrew tap

Prebuilt Linux x86_64 and ARM64 releases of [Knocker CLI](https://github.com/FarisZR/knocker-cli)
and [Komodo Agentic CLI](https://github.com/FarisZR/komodo-agentic-cli).

## Install

```bash
brew update
brew tap fariszr/tap
brew trust fariszr/tap
brew install --cask knocker-cli komodo-agentic-cli
```

Homebrew maps `fariszr/tap` to the GitHub repository `FarisZR/homebrew-tap`;
the `homebrew-` prefix is omitted from the tap command. Once tapped and trusted,
packages can be installed by their short names as shown above. Package tokens
use lowercase letters and hyphens, not spaces: `knocker-cli` and
`komodo-agentic-cli`. Commands installed: `knocker` and `km`.
Use Homebrew 6 or newer with Linux cask support. Review this tap before the
`brew trust` step; trust is required for third-party taps.

| Package | Installed command | Supported platforms |
| --- | --- | --- |
| `knocker-cli` | `knocker` | Linux x86_64 and ARM64 |
| `komodo-agentic-cli` | `km` | Linux x86_64 and ARM64 |

These packages currently require Linux; the tap does not provide macOS builds.

Komodo uses the existing Ubuntu 24.04 GNU/Linux release binaries, including their
glibc/OpenSSL runtime requirements. Homebrew packaging does not make them static
or compatible with older distributions. Knocker builds with `CGO_ENABLED=0`.
The tap does not automatically install or restart Knocker's systemd service.

## Update

```bash
brew update
brew upgrade --cask knocker-cli komodo-agentic-cli
```

Installing the tap makes new releases available to Homebrew. Run the update
commands above to install them on your device; syncing the tap does not upgrade
your local installation or restart running services.

### Existing installations

The tap name remains `fariszr/tap` after the repository rename. If you previously
added it with the old explicit URL, point its existing checkout at the new URL:

```bash
git -C "$(brew --repository fariszr/tap)" remote set-url origin https://github.com/FarisZR/homebrew-tap.git
brew update
brew trust fariszr/tap
brew upgrade --cask knocker-cli komodo-agentic-cli
```

The tap includes Homebrew rename metadata for the old `knocker` cask, so existing
installations can migrate to `knocker-cli`. The executable remains `knocker`.

## Release automation

1. Each project's existing workflow uploads its GitHub release assets.
2. Knocker triggers `sync.yml` after GoReleaser succeeds. Komodo's separate
   `update-homebrew.yml` observes successful completion of `Release CLI` without
   changing the original release pipeline.
3. This tap reads both repositories' latest stable releases, verifies that all
   required assets are uploaded, and writes their SHA-256 digests into the casks.
4. Its repository-scoped `GITHUB_TOKEN` commits the updated casks to `main`.

The updater accepts no repository, asset URL, or tag inputs. Every trigger reads
the current latest stable releases, so delayed/coalesced events cannot request
an older release. GitHub's SHA-256 asset digest is used when available; older
assets are downloaded and hashed. Missing assets stop the update before writing
either cask. Sync runs are serialized and unchanged releases produce no commit.

The tap also checks every six hours and can be run manually under
**Actions → Sync release casks → Run workflow**. Scheduled checks need no PAT;
the PAT below is only for immediate release notifications. Public repository
scheduled workflows may be disabled by GitHub after 60 days without activity;
re-enable the workflow if this happens.

## Token setup (immediate updates)

Create a **fine-grained personal access token** at
[GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens](https://github.com/settings/personal-access-tokens/new):

| Setting | Value |
| --- | --- |
| Token name | `homebrew-tap-dispatch` |
| Resource owner | `FarisZR` |
| Repository access | Only selected repositories: **`FarisZR/homebrew-tap`** |
| Repository permission | **Actions: Read and write** |
| Metadata | Read-only (automatically included) |
| All other permissions | None; no Contents write, Workflows, Secrets, Administration, or Pull requests |

Choose an expiry you can maintain and rotate before it expires.
GitHub requires Actions write for the workflow-dispatch endpoint, not Contents
write: [official API documentation](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event).
The token grants Actions write across the tap's Actions API, not only one workflow.

Add that same token as a **repository Actions secret**, named
**`TAP_GITHUB_TOKEN`**, in each of these repositories:

| Repository | Secret settings |
| --- | --- |
| `FarisZR/knocker-cli` | [Settings → Secrets and variables → Actions](https://github.com/FarisZR/knocker-cli/settings/secrets/actions) |
| `FarisZR/komodo-agentic-cli` | [Settings → Secrets and variables → Actions](https://github.com/FarisZR/komodo-agentic-cli/settings/secrets/actions) |

No PAT secret is needed in `FarisZR/homebrew-tap`. Missing source-repository secrets emit a
warning and leave scheduled/manual synchronization available.
After adding the secrets, run the tap's sync workflow once; no new release is
required. The existing latest releases are already represented in this tap.

The sync job requests `contents: write` for its built-in `GITHUB_TOKEN`; the
workflow's default permissions and test workflow are read-only. A rule requiring
all changes to `main` to pass through a PR would block the direct sync commit;
configure an appropriate bot exception or adapt publishing to PRs in that case.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/update_casks.py
```

The test workflow also installs both casks and runs their `--help` commands on
Linux x86_64 and ARM64, then uninstalls them.
