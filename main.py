import time
import json
import os
import urllib3

TOKEN = os.environ["INPUT_TOKEN"]
ARTIFACT_NAME = os.environ["INPUT_ARTIFACT_NAME"]
NAME = os.environ["INPUT_RENAME"] or ARTIFACT_NAME
REPO = os.getenv("INPUT_REPO") or os.getenv("GITHUB_REPOSITORY")
WAIT_SECONDS = int(os.getenv("INPUT_WAIT_SECONDS") or "60")
WAIT_SLEEP = 0.5

artifacts_url = f"https://api.github.com/repos/{REPO}/actions/artifacts"
headers = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "Python",
}

http = urllib3.PoolManager()


def get_artifact(name):
    print(f"Download `{name}` from: {artifacts_url}")

    t_started = time.time()
    waiting = True
    etag = None

    while waiting:
        if etag:
            resp = http.request(
                "GET", artifacts_url, headers={**headers, "If-None-Match": etag}
            )
        else:
            resp = http.request("GET", artifacts_url, headers=headers)
            etag = resp.headers.get("etag")

        if resp.status == 200:
            data = json.loads(resp.data.decode("utf-8"))
            for artifact in data["artifacts"]:
                print("Check artifact", artifact["name"])
                if artifact["name"] == name:
                    return artifact

        waiting = time.time() - t_started < WAIT_SECONDS
        time.sleep(1)
        print("Waiting...", etag, resp.status)


def download_artifact(name, new_name):
    artifact = get_artifact(name)
    if artifact is None:
        print(f"::set-output name=error::Artifact not found: {name}")
        exit(1)

    r = http.request("GET", artifact["archive_download_url"], headers=headers)
    with open(new_name, "wb") as f:
        f.write(r.data)
        print(f"::set-output name=success::Artifact downloaded: {artifact['name']}")


if __name__ == "__main__":
    download_artifact(ARTIFACT_NAME, NAME)
