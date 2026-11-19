# GitHub repository preparation audit — 19 November 2026

## Findings

- Initial audit found no Git repository. `C:\Agastya` was initialized on `main` with the exact owner-supplied URL as `origin`; the reviewed initial set now has local root commit `e194ddb06275c48159356f85cea18c473b4f6f66`.
- Git and Git LFS are installed. `gh` (GitHub CLI) is not on PATH.
- GitHub Desktop is installed, but launching it through the available computer-use surface returned an accessibility window-opened error and exposed no repository/account window. No authentication was attempted.
- Read-only GitHub repository access checked the exact owner-supplied URL. The destination exists, is empty, has default branch `main`, and is currently public.
- The connected account `icantchooseaname225` has repository admin permission. The owner chose to keep the repository public. The local commit exists; a command-line push was rejected because no Git credentials were available, and the remote remains empty.

## Data and privacy review required before upload

A full metadata inventory generated on 19 November 2026 enumerated 47,546 files totaling about 3.81 GB, with no traversal errors. It records paths, extensions, byte sizes and UTC modification times, not file contents. Large examples include a 1.37 GB EYE archive, a 145 MB EYE archive, a 78 MB historical virtual-simulation CSV and a 27.7 MB generated scenario CSV. EYE's local dataset image store is about 3.26 GB. `work/` is an approximately 290 MB scratch/audit tree. The complete path inventory is ignored by Git because it reveals local dataset paths and is not needed for reproducible source control.

The root contains outreach contact and tracker files, an outreach dossier and a source folder for correspondence. Those are excluded by the new `.gitignore`. EYE raw/processed image corpora, local captures, downloaded archives and model weights are excluded; their code, licenses, source manifests and small evaluation reports remain candidates for version control. `IRIS/` and its ZIP package are excluded pending review for personal/submission information. Generated simulation arrays are excluded where source and summary outputs already exist.

The `.gitignore` is a curated initial-publication filter: it excludes personal correspondence/contact files, the private enquiry folder, raw image corpora, model weights, local path inventories, submission packages, archived duplicates, and unreviewed PDF/Office binaries. Candidate text/code files were screened for email addresses, user-profile paths and credential patterns; contact sheets, a public-contact lead sheet, dataset group manifest, and generated inspection exports are excluded. No files were deleted or moved.

## Current state and next requirement

The owner supplied [`https://github.com/icantchooseaname225/agastya-photovoltaic-recovery.git`](https://github.com/icantchooseaname225/agastya-photovoltaic-recovery) and directed that the repository remain public. Connected metadata confirms the repository is empty, public, uses `main`, and grants the connected account admin permission. No sign-in is needed to change visibility. A Git sign-in is required to push the local commit.

The local `C:\Agastya` repository is on branch `main`, with the exact URL configured as `origin`. The complete staged set was reconciled against the manifest and committed locally as `e194ddb06275c48159356f85cea18c473b4f6f66`. The text/code candidates were screened for email addresses, local profile paths and credential patterns; no candidate exceeds 10 MiB. The manifest contains the exact count, byte total, paths and exclusions. A regular `git push -u origin main` failed because command-line Git had no saved credentials. The repository remains empty/public; no force-push or alternative partial upload was attempted.

The connected GitHub tools expose Git object operations, but no action for creating the initial branch ref in an empty repository. The local commit is ready to publish after the owner signs in through Git Credential Manager or GitHub Desktop.
