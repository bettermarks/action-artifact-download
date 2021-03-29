import json
import os
import urllib3

token = os.environ["INPUT_TOKEN"]
artifact_name = os.environ["INPUT_ARTIFACT_NAME"]
repo = os.getenv("INPUT_REPO", os.getenv("GITHUB_REPOSITORY"))

artifacts_url = f"https://api.github.com/repos/{repo}/actions/artifacts"
headers = {
    "Authorization": f"token {token}",
    "User-Agent": "Python",
}

http = urllib3.PoolManager()


def get_artifact(name):
    r = http.request("GET", artifacts_url, headers=headers)
    data = json.loads(r.data.decode("utf-8"))
    for artifact in data["artifacts"]:
        if artifact["name"] == name:
            return artifact


def download_artifact(artifact):
    r = http.request("GET", artifact["archive_download_url"], headers=headers)
    with open(artifact["name"], "wb") as f:
        f.write(r.data)
        print(f"::set-output name=myOutput::Artifact downloaded: {artifact['name']}")


if __name__ == "__main__":
    download_artifact(get_artifact(artifact_name))
