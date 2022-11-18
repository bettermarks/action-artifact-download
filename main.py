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
GITHUB_OUTPUT = os.environ["GITHUB_OUTPUT"]

artifacts_url = f"https://api.github.com/repos/{REPO}/actions/artifacts?name={NAME}"
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
            return data["artifacts"][0] if data["artifacts"] else None

        waiting = time.time() - t_started < WAIT_SECONDS
        time.sleep(1)
        print("Waiting...", etag, resp.status)


def set_output(name, value):
    with open(GITHUB_OUTPUT, "a") as github_output:
        github_output.write("{}={}".format(name, value))


def download_artifact(name, new_name):
    artifact = get_artifact(name)
    if artifact is None:
        set_output("error", "Artifact not found: {}".format(name))
        exit(1)

    r = http.request("GET", artifact["archive_download_url"], headers=headers)
    with open(new_name, "wb") as f:
        f.write(r.data)
        set_output("success", "Artifact downloaded: {}".format(artifact["name"]))
        set_output("commit", artifact["workflow_run"]["head_sha"])


if __name__ == "__main__":
    download_artifact(ARTIFACT_NAME, NAME)
