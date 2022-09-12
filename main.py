import os
import requests
import json
import shutil

TOKEN = os.environ["INPUT_TOKEN"]
ARTIFACT_NAME = os.environ["INPUT_ARTIFACT_NAME"]
NEW_ARTIFACT_NAME = os.environ["INPUT_NEW_ARTIFACT_NAME"]
REPO = os.getenv("INPUT_REPO") or os.getenv("GITHUB_REPOSITORY")
BRANCH = os.environ["INPUT_BRANCH"]
OWNER = os.environ["INPUT_OWNER"]

artifacts_url = f"https://api.github.com/repos/{REPO}/actions/artifacts"
headers = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Python",
}

def get_artifact_id(branch):
    artifacts_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts?per_page=100"
    r = requests.get(artifacts_url, headers=headers)
    j = json.loads(r.content)
    if not r.ok:
        print(f"::set-output name=error::{r.content}") # TODO change error

    print(f"::set-output name=error::{r.content}") # TODO change error
    for artifact in j['artifacts']:
        if artifact["workflow_run"]["head_branch"] == branch and artifact["name"] == ARTIFACT_NAME:
            return artifact["archive_download_url"]

    print(f"::set-output name=error::Could not find the requested artifact: {ARTIFACT_NAME}") # TODO change error
    exit(1)

def get_branch_name():
    if BRANCH == "main":
        return BRANCH
    else:
        check_branch_url = f"https://api.github.com/repos/{OWNER}/{REPO}/branches/{BRANCH}"
        r = requests.get(check_branch_url, headers=headers)

        if r.ok:
            return BRANCH
        else:
            print(f"::set-output name=error::Cant find branch: {BRANCH} falling back to main")
            return "main"

def download_artifact():
    branch = get_branch_name()
    
    archive_download_url = get_artifact_id(branch)

    with requests.get(archive_download_url, headers=headers, stream=True) as r:
        with open(NEW_ARTIFACT_NAME, "wb") as f:
            shutil.copyfileobj(r.raw, f)
            print(f"::set-output name=success::Artifact downloaded: {ARTIFACT_NAME}")

if __name__ == "__main__":
    download_artifact()
