# Tokens and permissions

## Immediate release notifications

Create a [fine-grained personal access token](https://github.com/settings/personal-access-tokens/new)
with the following settings:

| Setting | Value |
| --- | --- |
| Suggested name | `homebrew-tap-dispatch` |
| Resource owner | `FarisZR` |
| Repository access | Only `FarisZR/homebrew-tap` |
| Repository permission | Actions: read and write |
| Metadata | Read-only, automatically included |
| All other permissions | None |

The [workflow-dispatch API](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event)
requires Actions write. The token can access other Actions operations in the
selected repository too; its scope is not limited to one workflow. It needs no
Contents write permission.

Add the token as a repository Actions secret named `TAP_GITHUB_TOKEN` in
each source repository:

| Repository | Secret settings |
| --- | --- |
| `FarisZR/knocker-cli` | [Actions secrets](https://github.com/FarisZR/knocker-cli/settings/secrets/actions) |
| `FarisZR/komodo-agentic-cli` | [Actions secrets](https://github.com/FarisZR/komodo-agentic-cli/settings/secrets/actions) |

No PAT is required in the tap repository. Never commit credentials or print
their values in workflow logs.

If a source secret is absent, its notification job warns and exits successfully
without dispatching. The tap's scheduled and manual synchronization remain
available. A successful notification job alone therefore does not prove a
dispatch happened; inspect its warning output and the tap's workflow runs.

## Built-in workflow permissions

| Workflow job | Built-in `GITHUB_TOKEN` permissions | Purpose |
| --- | --- | --- |
| Tap sync | Contents: write | Checkout and commit casks within the tap |
| Tap tests | Contents: read | Read the checked-out tap |
| Knocker release publication | Contents: write | Publish release assets in Knocker's repository |
| Knocker notification | None | Uses the separate PAT for tap dispatch |
| Komodo notification | None | Uses the separate PAT for tap dispatch |

The tap's sync workflow defaults to Contents read; only the sync job requests
write. The source repositories' built-in tokens cannot substitute for the PAT
when dispatching to another repository.

A rule requiring pull requests for every change to `main` can block direct
sync commits. Configure a permitted bot exception or change the sync workflow
to publish pull requests if such rules are enabled.

## Activation and rotation

1. Create the token and set `TAP_GITHUB_TOKEN` in each source repository.
2. For Komodo, manually run `Update Homebrew tap` and confirm a corresponding
   `Sync release casks` run appears in the tap.
3. For Knocker, confirm its notification on the next successful release build.
   Running its release workflow manually rebuilds an existing tag; it is not
   a notification-only test.
4. To synchronize immediately without rebuilding a source release, run the
   tap's `Sync release casks` workflow manually.

Choose a manageable expiry. Before expiration, create a replacement with the
same repository scope and permissions, update both source secrets, verify
dispatch, and revoke the old token. The secret name stays unchanged.
