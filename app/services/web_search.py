import logging
import httpx
from typing import List, Dict

logger = logging.getLogger(__name__)


async def search_web(query: str, max_results: int = 5) -> List[Dict]:
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
        )
    }
    data = {"q": query}

    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as c:
            r = await c.post(url, data=data, headers=headers)
            if r.status_code != 200:
                return []

            html = r.text
            results = []
            # استخراج بسيط بدون مكتبات إضافية
            import re
            blocks = re.findall(
                r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
                r'.*?<a class="result__snippet"[^>]*>(.*?)</a>',
                html, re.DOTALL
            )
            for link, title, snippet in blocks[:max_results]:
                snippet = re.sub(r"<[^>]+>", "", snippet).strip()
                results.append({
                    "title": title.strip(),
                    "url": link.strip(),
                    "snippet": snippet[:400],
                })
            return results
    except Exception as e:
        logger.warning("Search error: %s", e)
        return []
