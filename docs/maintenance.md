# Maintenance policy

Fernpress follows semantic versioning. The `stable/1.x` branch is the
maintenance home for the 1.x series.

## What goes into 1.x

- Security fixes.
- Regressions introduced in a 1.x release.
- Small compatibility fixes for supported Python versions.
- Documentation corrections.

New site-building features are developed on `main` and land in the next major
release. Once a new major release is available, the previous stable branch
remains open for critical fixes for at least six months.

## Releases

Patch releases are cut directly from `stable/1.x`. Minor releases may include
backward-compatible features and are tagged on the same branch. Every release
tag is annotated and includes the supported Python range in its release notes.

## Backporting

A fix should land on `main` first when the affected code still exists there.
When the code has diverged, the stable branch fix is written against the 1.x
implementation and linked in the accompanying issue.
