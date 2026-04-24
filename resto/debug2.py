import sys
from playwright.sync_api import sync_playwright

def find_selectors(url: str, target_value: str):
    print(f"\n[DEBUG] Procurando por '{target_value}' em: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(5000)  # Aguarda o JavaScript renderizar a página

            # Busca qualquer elemento que contenha o texto desejado
            elements = page.query_selector_all(f"text={target_value}")

            print(f"\n[{len(elements)}] elemento(s) encontrado(s) com o valor '{target_value}':")
            print("-" * 80)

            for i, el in enumerate(elements):
                # Extrai informações do elemento
                tag = el.evaluate("el => el.tagName").lower()
                el_id = el.evaluate("el => el.id")
                classes = el.evaluate("el => el.className")

                # Constrói sugestão de CSS
                css_suggestion = tag
                if el_id:
                    css_suggestion += f"#{el_id}"
                elif classes:
                    # Converte "class1 class2" em ".class1.class2"
                    class_formatted = ".".join(classes.split())
                    css_suggestion += f".{class_formatted}"

                # Constrói sugestão de XPath baseada no texto
                xpath_suggestion = f"//{tag}[contains(text(), '{target_value}')]"

                print(f"MATCH {i+1}:")
                print(f"  TAG: {tag.upper()}")
                if el_id: 
                    print(f"  ID: {el_id}")
                if classes: 
                    print(f"  CLASSES: {classes}")
                print(f"  [SUGESTÃO CSS]   -> {css_suggestion}")
                print(f"  [SUGESTÃO XPath] -> {xpath_suggestion}")
                print("-" * 80)

        except Exception as e:
            print(f"[ERRO] Falha ao escanear a página: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    target_url = input("URL: ").strip()
    target_val = input("Valor exato (ex: 400, USD, 39,95): ").strip()
    find_selectors(target_url, target_val)