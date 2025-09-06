# Contributing

Thanks for helping improve Fernpress. The project has no runtime dependencies
outside the Python standard library, and contributions should keep it that
way.

## Development setup

Use Python 3.9 or newer. From the repository root:

```sh
python -m unittest discover -s tests
python -m fernpress build --config example/site.json
```

The generated example output is ignored by Git. Delete `example/public/` to
force a clean build.

## Branch and release flow

- `main` carries development for the next release.
- Stable branches are named `stable/<major>.x`.
- Release tags are annotated and use `vMAJOR.MINOR.PATCH`.
- Bug fixes should include a regression test where practical.

## Commit style

Use a short imperative subject. Prefixes such as `feat:`, `fix:`, `test:`,
`docs:`, and `refactor:` are welcome but not mandatory. Keep unrelated changes
in separate commits.

## Reporting bugs

Include the Fernpress version, Python version, a minimal site configuration,
and the command that reproduces the problem. Do not include credentials or
private content in reports.
