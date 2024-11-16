# Maintenance policy

Fernpress follows semantic versioning. The `stable/2.x` branch is the
maintenance home for the 2.x series.

## What goes into 2.x

- Security fixes.
- Regressions in 2.x releases.
- Small compatibility fixes.
- Documentation corrections.

New site-building features are developed on `main` for the next major release.
Backports should be written against the 2.x code and should include a
regression test whenever the behavior can be tested locally.

## Release tags

Release tags are annotated and point at the commit that contains the version
and changelog update. Patch releases are cut from `stable/2.x`; minor releases
may also include backward-compatible features.
