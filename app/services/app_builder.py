import os
import uuid
import re
from datetime import datetime


class AppBuilderService:
    @staticmethod
    def _safe_name(name: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_-]", "_", name.strip())[:40] or "app"

    @staticmethod
    async def build_pwa(app_name: str, html_content: str) -> str:
        os.makedirs("static/apps", exist_ok=True)
        safe = AppBuilderService._safe_name(app_name)
        token = str(uuid.uuid4())[:8]
        filename = safe + "_" + token + ".html"
        path = os.path.join("static/apps", filename)

        manifest = (
            '{"name":"' + app_name + '","short_name":"' + app_name[:12] + '",'
            '"start_url":".","display":"standalone","background_color":"#0f172a",'
            '"theme_color":"#06b6d4","icons":[]}'
        )

        full_html = (
            '<!DOCTYPE html><html lang="ar" dir="rtl"><head>'
            '<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<meta name="theme-color" content="#06b6d4">'
            '<title>' + app_name + '</title>'
            '<link rel="manifest" href="data:application/json;charset=utf-8,'
            + manifest.replace("#", "%23") + '">'
            '<style>body{font-family:system-ui;margin:0;padding:20px;'
            'background:#0f172a;color:#f8fafc}</style>'
            '</head><body>' + html_content + '</body></html>'
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)

        return "/static/apps/" + filename
