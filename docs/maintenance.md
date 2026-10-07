# Maintenance

## Manual synchronization

In GitHub, open the tap's **Actions → Sync release casks → Run workflow**
and select `main`. From an authenticated GitHub CLI:

```bash
gh workflow run sync.yml --repo FarisZR/homebrew-tap --ref main
gh run list --repo FarisZR/homebrew-tap --workflow sync.yml
```

No new source release is required; the updater reads the latest releases.

## Local validation

From the tap checkout, with Python 3 and Ruby installed:

```bash
python3 -m unittest discover -s tests -v
ruby -c Casks/knocker-cli.rb
ruby -c Casks/komodo-agentic-cli.rb
ruby -c Casks/whisper-stt-gnome-extension.rb
git diff --check
```

To regenerate package definitions against live public releases:

```bash
python3 scripts/update_casks.py
git diff -- Casks/
```

An optional `GH_TOKEN` authenticates release API reads. The generator needs no
write permission; publishing the resulting Git changes is a separate step.
Keep generated casks aligned with the generator, since later synchronization
overwrites manual cask edits.

## Adding a project

1. Publish complete release assets for the supported platforms. Choose stable
   asset filenames and a tag format accepted by the updater.
2. Add the package token, repository, display name, description, and asset names
   to `PROJECTS` in `scripts/update_casks.py`.
3. Extend `render_cask` for the new project's architecture names, URL template,
   archive format, and executable. It handles the extension as a portable directory artifact and the two
   CLIs as architecture-specific binaries. Adding a dictionary entry alone is
   insufficient.
4. Add meaningful coverage for the new asset contract and run the updater.
5. Extend Ruby checks in both workflows and installation/help/uninstall
   commands in the test workflow. Update platform matrices if required.
6. Add the package to the user README with its command and project link.
7. Optionally add a notification after successful release publication in the
   source repository, using `TAP_GITHUB_TOKEN` as described in
   [token setup](tokens.md). Scheduled synchronization requires no source PAT.

Use lowercase, hyphenated package tokens. Keep the token, cask filename, and
`cask` declaration consistent. Avoid ambiguous names shared by unrelated
projects. Add new rename mappings to `cask_renames.json` when retiring a token.

The current updater processes all projects together. A missing asset in one
project blocks the entire sync, which should be considered when adding projects.

## Rolling extension builds

Each successful build of current `main` in the extension repository publishes a
`build-<full commit hash>` release. Reruns retain published assets. The tap uses
GitHub's latest release selection and the commit hash as the cask version; it
never parses commit hashes as semantic versions. Homebrew casks compare installed
and available version strings for equality, so a new hash is offered as an update.

The first package is seeded from the existing `main` commit. Merge the extension
build workflow to enable subsequent builds, then merge the tap integration.
Add `TAP_GITHUB_TOKEN` to the extension for immediate notifications; the six-hour
schedule also finds new builds. See [tokens](tokens.md).

A draft release is kept unpublished until all three assets are uploaded and
validated. Delete an incomplete draft and rerun on `main` to recover a failed
upload. Published assets must never be replaced, since casks pin their checksums.

## Repository and package migrations

The repository is `FarisZR/homebrew-tap`, while the Homebrew tap name remains
`fariszr/tap`. A checkout originally installed from the old explicit repository
URL can be updated in place:

```bash
git -C "$(brew --repository fariszr/tap)" remote set-url origin https://github.com/FarisZR/homebrew-tap.git
brew update
brew trust fariszr/tap
brew upgrade
```

The rename mapping `knocker → knocker-cli` is recorded in
`cask_renames.json`. The executable remains `knocker`.

For a future repository rename, update the sync job's repository guard,
both source dispatch URLs, token documentation, project links, and public tap
discovery checks. Verify token access still covers the renamed repository.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Release not reflected in the tap | Source build completion, required asset names, upload state, latest-release selection, and sync logs |
| Notification succeeds without a tap run | Missing `TAP_GITHUB_TOKEN` warning in the source job |
| Dispatch returns 401/403/404 | Token expiry, repository selection, Actions write permission, and target workflow path |
| Sync job is skipped | Repository guard in `sync.yml` |
| Sync cannot push | Branch rules and the sync job's Contents write permission |
| Scheduled runs stop | Workflow enabled state; GitHub can disable public-repository schedules after 60 days without activity |
| Package cannot load by short name | Tap is present and explicitly trusted |
| Binary already exists | Another installation owns `knocker` or `km`; resolve the conflicting installation before retrying |
| Komodo cannot start | Distribution compatibility and required glibc/OpenSSL libraries |
| Service still runs an older binary | Upgrade the package, then restart the configured service separately |

Changes pushed with the built-in `GITHUB_TOKEN` do not ordinarily trigger
another push workflow. Do not assume an automated cask commit also ran
`Test tap`; inspect the Actions runs when checking publication. See GitHub's
[workflow trigger rules](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
and [workflow enablement guidance](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).

## Device upgrade scheduling

This repository does not create a device timer. On Linux, schedule
`brew update` and `brew upgrade` with a systemd service/timer or an existing
scheduler. Run Homebrew as its owning user, not root. Use a persistent timer if
missed runs should execute when the device comes back online. Restart long-lived
services separately when their running processes need the new executable.
