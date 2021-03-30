# Download Artifact Action

[![Action](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/bettermarks/action-artifact-download)
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
      token: "${{ secrets.PERSONAL_ACCESS_TOKEN }}"
      checkName: artifact

  - uses: actions/checkout@master
  - name: Self test
    id: selftest

    # Put your action repo here
    uses: ./
    with:
      artifact_name: "${{ github.sha }}"
      token: "${{ secrets.PERSONAL_ACCESS_TOKEN }}"
      rename: foobar

  - name: Check outputs
    run: |
      test "${{ steps.selftest.outputs.success }}" == "Artifact downloaded: ${{ github.sha }}"
      test -f foobar
```