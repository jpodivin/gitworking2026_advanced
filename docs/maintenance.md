# Maintenance policy

Fernpress follows semantic versioning. Each major release has a stable branch
for maintenance, while `main` carries development for the next release.

## Supported releases

- The current major release receives fixes and compatibility updates.
- The previous major release receives security and critical regression fixes.
- Older releases are maintained only when a security issue requires it.

## Branch flow

Fixes for the current release land on `main` and are backported to the
corresponding stable branch when the code has not diverged. Fixes for older
releases are written against that branch's implementation.

## Release tags

Every release is tagged with an annotated `vMAJOR.MINOR.PATCH` tag on the
branch that contains the release commit. Tags are never moved.
