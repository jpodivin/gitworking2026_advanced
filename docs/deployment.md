# Deployment

Fernpress produces a self-contained directory of HTML, XML, and copied
assets. Build it with:

```sh
python -m fernpress build --config site.json
```

The configured `output_dir` can be uploaded to any static host. The generated
site has no runtime Python requirement.

## Generated files

- `index.html` and numbered pages under `page/`
- post pages under `posts/<slug>/`
- tag indexes under `tags/`
- `feed.xml`
- `sitemap.xml`
- files copied from the configured `static_dir`

## Incremental builds

A `.fern-cache.json` file is written inside the output directory. It records
source timestamps so unchanged pages do not need to be rendered again. Delete
it to force a full rebuild.

## Preview

```sh
python -m fernpress serve --config site.json --port 8000
```

The preview server is intended for local inspection only.
