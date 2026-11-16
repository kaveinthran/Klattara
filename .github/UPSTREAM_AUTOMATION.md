# Automatic original Klattara builds

This community fork tracks **RetroBunn/Klattara**, the original project. It checks upstream main at minute 37 of every hour, building and publishing only when the source commit has no complete published release. GitHub schedules can be delayed. These jobs use no Codex/model tokens and run on standard public-repository GitHub runners. No personal access token, paid runner or runtime AI service is needed.

- [Latest release](https://github.com/kaveinthran/Klattara/releases/latest)
- [Latest installer](https://github.com/kaveinthran/Klattara/releases/latest/download/klattara.nvda-addon)
- [Workflow status and manual run](https://github.com/kaveinthran/Klattara/actions/workflows/upstream-nvda.yml)

## Build and support

The add-on includes **both x64 and x86 DLLs** and preserves the upstream minimum NVDA **2025.1** and last-tested **2026.2** declarations. The Rust/static-CRT configuration, engine and driver remain upstream code. The automated community build changes only manifest packaging metadata: an increasing numeric community version, label and homepage.

The test setup is pinned in nvda-test-sources.json. Python 3.13 x64 tests the 64-bit DLL against official NVDA 2026.2 source; Python 3.11 x86 tests the 32-bit DLL against official NVDA 2025.1 source. Release-mode Rust workspace tests run on x64, with engine and C-interface tests also on x86. The original upstream builder assembles the add-on and runs both driver suites. A small trusted bootstrap routes its two `py` launcher calls to the exact setup-python executable paths, avoiding runner registry ambiguity without changing upstream build/test files. Real NVDA modules are used with stand-ins for runtime/audio services; live NVDA speech and installation are not established by these tests.

NVDA sources are test dependencies only and are never shipped. The package contains its manifest, driver, both architecture DLLs, upstream MIT licence and THIRD-PARTY-NOTICES.txt. Unexpected payload or architecture changes stop publication for review.

## Releases and change information

Each upstream source commit gets an immutable `upstream-<full-SHA>` release. Community versions use `YEAR.MONTHDAY.RUN_NUMBER` (UTC), retaining the original upstream version and source commit in provenance and release notes. An interrupted draft retains its original numeric version and asset name across retries.

Every release attaches a versioned installer, stable klattara.nvda-addon alias, SHA256SUMS.txt, source.json, MIT licence, third-party notices, INSTALL.txt, full CHANGELOG.md and CURRENT_FEATURES.md. The first release includes all upstream commit messages; later releases include every full message since the previous successful automated build, plus comparison/diff links. CURRENT_FEATURES.md is an exact upstream README snapshot. Large notes remain complete in attachments if they exceed the inline-description budget.

## Permissions, failure and maintenance

Only trusted fork scripts run with write access in the sync/publish jobs. Upstream code runs in a separate read-only build job, with checkout credentials not persisted. Publish treats downloaded artifacts as data and revalidates the package, licences, both PE architectures, provenance and hashes. It uploads/verifies a draft before publication, then anonymously checks the public installer. All official actions are pinned by SHA, jobs have timeouts and runs are serialized.

The normal source merge preserves the fork-owned .github directory so upstream cannot replace privileged automation. Unresolved source conflicts fail rather than force-push. Existing public releases are preserved on failures; later hourly runs retry an unpublished source. A small status commit initially and at most every 28 days avoids GitHub's 60-day inactivity disabling. No hourly empty commits are created.

Use the workflow page to inspect failures, retry manually or disable the schedule. Future upstream package-layout/build/API changes may require maintenance. The stable download is the latest successful build; no local NVDA installation, settings or restart is automated.

## Mirror listing

The Serrebi mirror requires a distinct ID for an intentionally included fork. A separate optional pin uses kaveinthran-klattara and the versioned installer asset, retaining the package's compatibility declarations. The mirror's existing repackager changes the manifest ID for that listing. Inclusion requires maintainer acceptance and deployment; publishing a GitHub release alone does not establish live store inclusion.

## References

- [Original Klattara source](https://github.com/RetroBunn/Klattara)
- [GitHub scheduling rules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Public-repository runner billing](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [Job token permissions](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
