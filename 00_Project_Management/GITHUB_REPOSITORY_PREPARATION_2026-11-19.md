# GitHub repository preparation audit — 19 November 2026

## Findings

- Initial audit found no Git repository. In the current continuation, `C:\Agastya` was initialized on `main` and the exact owner-supplied URL was added as `origin`; there are no commits.
- Git and Git LFS are installed. `gh` (GitHub CLI) is not on PATH.
- GitHub Desktop is installed, but launching it through the available computer-use surface returned an accessibility window-opened error and exposed no repository/account window. No authentication was attempted.
- Read-only GitHub repository access checked the exact owner-supplied URL. The destination exists, is empty, has default branch `main`, and is currently public.
- The connected account `icantchooseaname225` has repository admin permission. The owner chose to keep the repository public. No visibility change, commit, or upload has occurred.

## Data and privacy review required before upload

A full metadata inventory generated on 19 November 2026 enumerated 47,546 files totaling about 3.81 GB, with no traversal errors. It records paths, extensions, byte sizes and UTC modification times, not file contents. Large examples include a 1.37 GB EYE archive, a 145 MB EYE archive, a 78 MB historical virtual-simulation CSV and a 27.7 MB generated scenario CSV. EYE's local dataset image store is about 3.26 GB. `work/` is an approximately 290 MB scratch/audit tree. The complete path inventory is ignored by Git because it reveals local dataset paths and is not needed for reproducible source control.

The root contains outreach contact and tracker files, an outreach dossier and a source folder for correspondence. Those are excluded by the new `.gitignore`. EYE raw/processed image corpora, local captures, downloaded archives and model weights are excluded; their code, licenses, source manifests and small evaluation reports remain candidates for version control. `IRIS/` and its ZIP package are excluded pending review for personal/submission information. Generated simulation arrays are excluded where source and summary outputs already exist.

The `.gitignore` is a curated initial-publication filter: it excludes personal correspondence/contact files, the private enquiry folder, raw image corpora, model weights, local path inventories, submission packages, archived duplicates, and unreviewed PDF/Office binaries. Candidate text/code files were screened for email addresses, user-profile paths and credential patterns; contact sheets, a public-contact lead sheet, dataset group manifest, and generated inspection exports are excluded. No files were deleted or moved.

## Current state and next requirement

The owner supplied [`https://github.com/icantchooseaname225/agastya-photovoltaic-recovery.git`](https://github.com/icantchooseaname225/agastya-photovoltaic-recovery) and directed that the repository remain public. Connected metadata confirms the repository is empty, public, uses `main`, and grants the connected account admin permission. No visibility change or sign-in is needed under the current instruction; no credentials were entered.

The local `C:\Agastya` repository is initialized on branch `main`, with the exact URL configured as `origin`. No commit or push has occurred. Before adding the review manifest, the filtered candidate set contains 399 files totalling 2,726,177 working-tree bytes; no candidate exceeds 10 MiB. The text/code candidates were screened for email addresses, local profile paths and credential patterns. The final staged count and byte total, including the manifest itself, are recorded in `GITHUB_STAGED_FILE_REVIEW_2026-11-19.md`. The owner must review and approve this exact staged set before any initial commit or push.
