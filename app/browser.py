from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def execute_steps(url: str, steps: list[dict], allowed_hosts: set[str]) -> dict:
    host = (urlparse(url).hostname or "").lower()
    normalized_hosts = {item.lower() for item in allowed_hosts}
    if host not in normalized_hosts:
        raise ValueError(f"Host is not allow-listed: {host}")

    actions = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})

        async def guard_request(route):
            request_host = (urlparse(route.request.url).hostname or "").lower()
            if request_host in normalized_hosts:
                await route.continue_()
            else:
                await route.abort()

        # Enforce the allow-list for redirects, scripts, frames and clicked links too.
        await context.route("**/*", guard_request)
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            for step in steps:
                action = step.get("action")
                selector = step.get("selector")
                if action == "click" and selector:
                    await page.locator(selector).first.click(timeout=10000)
                elif action == "fill" and selector:
                    await page.locator(selector).first.fill(str(step.get("value", "")))
                elif action == "screenshot":
                    import os
                    os.makedirs("artifacts", exist_ok=True)
                    path = "artifacts/latest.png"
                    await page.screenshot(path=path, full_page=True)
                    actions.append({"action": "screenshot", "path": path})
                    continue
                else:
                    raise ValueError(f"Unsupported or incomplete action: {step}")
                actions.append({"action": action, "selector": selector})
            return {"final_url": page.url, "title": await page.title(), "actions": actions}
        finally:
            await browser.close()
