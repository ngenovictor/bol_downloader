import datetime

from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright


def main(keyword: str = "samsung+phone"):
    url = f"https://www.bol.com/nl/nl/s/?searchtext={keyword}"
    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch(
            # headless=False,  # Uncomment this line to see the browser in action
        )
        context = browser.new_context(
            # add custom user agent to remove Headless notations in the request headers
            extra_http_headers={
                "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            }
        )
        page = context.new_page()
        default_timeout = 5 * 60 * 1000  # 5 minutes in ms
        page.goto(url, timeout=default_timeout)
        page.wait_for_selector("li.product-item--row", timeout=default_timeout)
        page_content = page.content()
        # -----------------------------------------------------------------------------------------#
        # DEBUG: Save the page content to a file
        with open("bol.html", "w") as f:
            f.write(page_content)
        # DEBUG: Save a screenshot of the page
        page.screenshot(
            path=f"screenshots/example-{browser_type.name}_{datetime.datetime.now()}.png"
        )
        # -----------------------------------------------------------------------------------------#
        browser.close()
        print("Done loading page. Parsing products")
        soup = BeautifulSoup(page_content, "html.parser")
        items = []
        for product in soup.find_all("li", class_="product-item--row"):
            items.append(
                {
                    "product": product.find("div", attrs={"class": "product-title--inline"}).text,
                    "price": product.find("span", attrs={"class": "promo-price"}).text,
                }
            )
        print(items)


if __name__ == "__main__":
    main()  # you can pass a keyword to search for a specific product eg main("iphone")
