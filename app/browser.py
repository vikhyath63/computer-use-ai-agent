from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def execute_steps(url: str, steps: list[dict], allowed_hosts: set[str]) -> dict:
    host = (urlparse(url).hostname or "").lower()
    if host not in allowed_hosts:
        raise ValueError(f"Host is not allow-listed: {host}")
    actions = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width":1280,"height":800})
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        for step in steps:
            action = step.get("action")
            selector = step.get("selector")
            if action == "click" and selector:
                await page.locator(selector).first.click(timeout=10000)
            elif action == "fill" and selector:
                await page.locator(selector).first.fill(str(step.get("value", "")))
            elif action == "screenshot":
                path = "artifacts/latest.png"
                import os
                os.makedirs("artifacts", exist_ok=True)
                await page.screenshot(path=path, full_page=True)
                actions.append({"action":"screenshot","path":path})
                continue
            else:
                await browser.close()
                raise ValueError(f"Unsupported or incomplete action: {step}")
            actions.append({"action":action,"selector":selector})
        result = {"final_url":page.url,"title":await page.title(),"actions":actions}
        await browser.close()
        return result
