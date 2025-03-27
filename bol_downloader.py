import datetime

from playwright.sync_api import Playwright, sync_playwright


def main():
    url = "https://www.bol.com/nl/nl/s/?searchtext=samsung+phone"
    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch(headless=False)
        context = browser.new_context(
            extra_http_headers={
                "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            }
        )
        page = context.new_page()
        default_timeout = 5 * 60 * 1000
        page.goto(url, timeout=default_timeout)
        page.wait_for_selector("li.product-item--row", timeout=default_timeout)
        print(page.title())
        page.screenshot(
            path=f"screenshots/example-{browser_type.name}_{datetime.datetime.now()}.png"
        )
        browser.close()
    # soup = BeautifulSoup(resp.text, "html.parser")
    # for product in soup.find_all("li", class_="product-item--row"):
    #     print(product.find("a", class_="product-title").text)
    #     print(product.find("span", class_="promo-price").text)
    #     print(product.find("span", class_="promo-bol-logo").text)


if __name__ == "__main__":
    main()
