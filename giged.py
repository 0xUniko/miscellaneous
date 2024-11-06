# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
# ]
# ///
import logging
import sys

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(module)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("hack.log"),
    ],
)

auth_token = "Bearer eyJ"

client = httpx.Client(
    base_url="https://gt-java-api.giged.cn:9003/api/v2",
    headers={"Authorization": auth_token},
)


def get_courses(page=1, size=20) -> list:
    res = client.get(
        "/courses",
        params={"page": page, "size": size, "category_id": 0},
    ).json()
    assert res["code"] == 0, f'failed to get courses: {res["msg"]}'
    return res["data"]["data"]


def get_videos(course_id: int) -> dict[int, list]:
    assert (res := client.get(f"/course/{course_id}").json())[
        "code"
    ] == 0, f'failed to get course {course_id}: {res["msg"]}'
    return res["data"]["videos"]


def hack_duration(video_id: int, duration=10):
    res = client.post(
        f"/video/{video_id}/record",
        json={"duration": duration},
    ).json()
    if res["code"] == 0:
        logging.info(f"hack video {video_id} success")
    else:
        logging.error(f"hack video {video_id} failed: {res['msg']}")


def main() -> None:
    courses = get_courses(6)
    for c in courses:
        logging.info(f"hack course {c["id"]}")
        videos = get_videos(c["id"])
        for v in videos:
            for vv in videos[v]:
                hack_duration(vv["id"], vv["duration"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(f"failed to hack: {e}")
