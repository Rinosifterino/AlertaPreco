import re
from playwright.sync_api import sync_playwright


def scan_all_price_candidates(url):
    """
    Varre a página em busca de todos os elementos que se parecem com preços.
    
    Imprime a tag, a classe e o conteúdo de cada candidato para ajudar
    na escolha do seletor correto.
    """
    print(f"\n[DEBUG] Scanning all price candidates at: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(5000)  # Aguarda renderização do JS

            # Seleciona todos os elementos que possuem texto
            elements = page.query_selector_all("span, div, p, b, strong")
            
            # Padrão para identificar formatos de moeda ($, R$, EUR, etc)
            price_pattern = r"(?:EUR|R\$|\$|€)\s?[\d.,]+"

            print(f"{'TAG':<10} | {'CLASSES':<50} | {'CONTENT'}")
            print("-" * 100)

            found_any = False
            for el in elements:
                text = el.inner_text().strip()
                if text and re.search(price_pattern, text):
                    tag = el.evaluate("el => el.tagName")
                    classes = el.evaluate("el => el.className")
                    
                    # Filtra apenas textos curtos para evitar pegar parágrafos inteiros
                    if len(text) < 30:
                        print(f"{tag:<10} | {classes[:50]:<50} | {text}")
                        found_any = True

            if not found_any:
                print("[DEBUG] No price-like patterns found on the page.")

        except Exception as error:
            print(f"[ERROR] Debug scan failed: {error}")
        finally:
            browser.close()


if __name__ == "__main__":
    # Teste diretamente aqui ou chame esta função no seu menu do debug.py
    target_url = input("Enter URL to debug: ").strip()
    scan_all_price_candidates(target_url)