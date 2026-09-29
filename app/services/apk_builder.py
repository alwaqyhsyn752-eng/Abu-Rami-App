import os
import base64
import asyncio
import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

GITHUB_OWNER = "alwaqyhsyn752-eng"
GITHUB_REPO = "Abu-Rami-App"
WORKFLOW_FILE = "build-apk.yml"


class APKBuilder:
    def __init__(self):
        self.token = os.getenv("GITHUB_ACTIONS_TOKEN", "").strip()
        if not self.token:
            logger.warning("GITHUB_ACTIONS_TOKEN not set - APK build disabled")

    async def trigger_build(
        self, app_name: str, html_content: str, build_id: str
    ) -> bool:
        if not self.token:
            raise RuntimeError("GITHUB_ACTIONS_TOKEN not configured")

        url = (
            "https://api.github.com/repos/"
            + GITHUB_OWNER + "/" + GITHUB_REPO
            + "/actions/workflows/" + WORKFLOW_FILE + "/dispatches"
        )

        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        payload = {
            "ref": "main",
            "inputs": {
                "app_name": app_name,
                "app_html_base64": base64.b64encode(
                    html_content.encode("utf-8")
                ).decode("ascii"),
                "build_id": build_id,
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=payload, headers=headers)
            if res.status_code not in (200, 204):
                raise RuntimeError(
                    "GitHub API: " + str(res.status_code) + " " + res.text[:200]
                )
            logger.info("APK build triggered: %s", build_id)
            return True

    async def poll_build(
        self, build_id: str, timeout: int = 20
    ) -> Optional[str]:
        if not self.token:
            return None

        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
        }

        url = (
            "https://api.github.com/repos/"
            + GITHUB_OWNER + "/" + GITHUB_REPO
            + "/releases/tags/apk-" + build_id
        )

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.get(url, headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    for asset in data.get("assets", []):
                        name = asset.get("name", "")
                        if name.endswith(".apk"):
                            return asset.get("browser_download_url")
        except Exception as e:
            logger.warning("Poll failed: %s", e)

        return None


apk_builder = APKBuilder()
