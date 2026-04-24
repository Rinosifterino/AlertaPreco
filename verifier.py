"""
Módulo responsável por extrair preços, moedas e prefixos de páginas web.
"""

import re
from typing import Optional, Tuple
from playwright.sync_api import sync_playwright


def extract_price_and_currency(url: str, selector: Optional[str] = None) -> Optional[Tuple[float, str, str]]:
    """
    Acessa uma URL e extrai o valor numérico, a moeda e o texto de contexto (prefixo).

    :param url: Endereço web do produto.
    :param selector: (Opcional) Seletor CSS ou XPath.
    :return: Tupla (preço, moeda, prefixo) ou None se falhar.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print(f"\n[LOG] Opening URL: {url}")
            page.goto(url, timeout=15000)
            page.wait_for_timeout(4000)

            raw_text = None
            
            # 1. Tenta seletores (Usuário ou Heurística)
            targets = [selector] if selector else [
                ".x-price-primary", ".x-price-approx__price", 
                "span[itemprop='price']", ".price", ".a-price .a-offscreen"
            ]

            for target in targets:
                if not target: continue
                element = page.locator(target)
                if element.count() > 0:
                    raw_text = element.first.inner_text().strip()
                    print(f"[LOG] Found content via {target}: '{raw_text}'")
                    break

            # 2. Fallback: Regex global no HTML se os seletores falharem
            if not raw_text:
                html = page.content()
                # Padrão básico para achar algo que pareça preço no HTML bruto
                fallback_pattern = r"(?:R\$|EUR|US\$|\$|€|GBP)\s?[\d.,]+"
                match = re.search(fallback_pattern, html)
                if match:
                    raw_text = match.group()
                    print(f"[LOG] Found via Global Regex: {raw_text}")

            browser.close()

            if raw_text:
                # 3. Padrão Universal para separar (Prefixo)(Moeda Inicial)(Número)(Código Final)
                currencies = r"R\$|US\$|EUR|USD|BRL|GBP|\$|€|£"
                universal_pattern = rf"(.*?)\b({currencies})?\s?([\d.,]+)\s?({currencies})?"
                
                data_match = re.search(universal_pattern, raw_text)
                
                if data_match:
                    prefix = data_match.group(1).strip()
                    curr_start = data_match.group(2)
                    num_str = data_match.group(3)
                    curr_end = data_match.group(4)

                    # Define a moeda final (prioriza o que foi achado)
                    currency = curr_start or curr_end or "Unit"

                    # Limpeza e conversão do número para float
                    if "," in num_str and "." in num_str:
                        num_str = num_str.replace(".", "").replace(",", ".")
                    elif "," in num_str:
                        num_str = num_str.replace(",", ".")
                    
                    price = float(num_str)
                    
                    return currency, price, prefix

            return None

    except Exception as error:
        print(f"[ERROR] Extraction failed: {error}")
        return None