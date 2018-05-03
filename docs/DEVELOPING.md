# To document some developer-specific items

## Doing a release

Tag in `git` and push to GitHub

```shell
git tag -a `cat VERSION` -m "tagging for `cat VERSION`"
git push origin `cat VERSION`
```

Use the web interface in GitHub to create the release notes and an actual "release".
