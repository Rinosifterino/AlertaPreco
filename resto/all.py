import re
from playwright.sync_api import sync_playwright

def debug_all_numbers(url):
    print(f"\n[DEBUG] Scanning ALL numbers at: {url}")
    
    with sync_playwright() as p:
        # 1. Added headless=False to see the browser
        # 2. Added a standard User-Agent to avoid immediate blocking
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win 64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(url, timeout=30000)
            # 3. Increased wait time to ensure JS loads
            page.wait_for_timeout(7000) 

            elements = page.query_selector_all("b, span, div, p, strong, td")
            broad_number_pattern = r"[\d.,]+"

            print(f"{'TAG':<10} | {'CONTENT'}")
            print("-" * 50)

            for el in elements:
                try:
                    text = el.inner_text().strip()
                    if text and re.search(broad_number_pattern, text) and len(text) < 50:
                        tag = el.evaluate("el => el.tagName")
                        print(f"{tag:<10} | {text}")
                except:
                    continue

        except Exception as error:
            print(f"[ERROR] Debug script failed: {error}")
        finally:
            # Keep browser open for a few seconds so you can see the screen
            page.wait_for_timeout(5000)
            browser.close()

if __name__ == "__main__":
    target_url = input("Enter the URL to debug: ").strip()
    debug_all_numbers(target_url)