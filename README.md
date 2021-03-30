# Download Artifact Action

[![Actions Status](https://github.com/bettermarks/action-artifact-download/workflows/Lint/badge.svg)](https://github.com/bettermarks/action-artifact-download/actions)
[![Actions Status](https://github.com/bettermarks/action-artifact-download/workflows/Integration%20Test/badge.svg)](https://github.com/bettermarks/action-artifact-download/actions)

This downloads an artifact from your build implemented in python.

## Usage

Specify a repository and an artifact name to download it. To allow
access you have to pass your personal access token.
Optionally a name for the downloaded artifact can be passed and the
time to wait for an artifact to be available for download.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Download artifact from build
      uses: bettermarks/action-artifact-download@0.1.0
      with:
        repo: organization/the-repo-to-use
        token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
        artifact_name: my-artifact
        rename: new-artifact-name    
        wait_seconds: 60  
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `repo`  | The repository to download from    |
| `token`  | The personal access token    |
| `artifact_name`  | The name of the artifact to download    |
| `rename` _(optional)_  | An optional name for the downloaded artifact. Defaults to `artifact_name`.    |
| `wait_seconds` _(optional)_  | Time to wait for the artifact to be available for download. Defaults to 1 minute.    |

### Using outputs

Check the example to see how to use the output of the action

```yaml
steps:
  - name: Wait for artifact to succeed
    uses: fountainhead/action-wait-for-check@v1.0.0
    id: wait-for-build
    with:
      token: "${{ secrets.GITHUB_TOKEN }}"
      checkName: artifact

  - uses: actions/checkout@master
  - name: Self test
    id: selftest

    # Put your action repo here
    uses: ./
    with:
      artifact_name: "${{ github.sha }}"
      token: "${{ secrets.GITHUB_TOKEN }}"
      rename: foobar

  - name: Check outputs
    run: |
      test "${{ steps.selftest.outputs.success }}" == "Artifact downloaded: ${{ github.sha }}"
      test -f foobar
```