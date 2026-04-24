import pytest
from unittest.mock import MagicMock
from verifier import extract_price_and_currency

def test_extract_price_and_currency_success(mocker):
    # Simula o contexto do Playwright
    mock_playwright = mocker.patch("verifier.sync_playwright")
    
    mock_page = MagicMock()
    
    # [CORREÇÃO AQUI]: Ensina o mock a encontrar o elemento (count = 1)
    mock_page.locator.return_value.count.return_value = 1
    # Ensina o mock a retornar o texto completo de dentro do elemento
    mock_page.locator.return_value.first.inner_text.return_value = "Valor Atual: EUR 39,95"
    
    # Cria a hierarquia de mocks (Browser -> Page)
    mock_browser = MagicMock()
    mock_browser.new_page.return_value = mock_page
    mock_p = MagicMock()
    mock_p.chromium.launch.return_value = mock_browser
    mock_playwright.return_value.__enter__.return_value = mock_p

    # Testa a função
    result = extract_price_and_currency("http://site-falso.com", selector=".price")
    
    assert result is not None
    
    # O seu verifier.py retorna (currency, price, prefix)
    currency, price, prefix = result 
    
    assert price == 39.95
    assert currency == "EUR"
    assert prefix == "Valor Atual:"

def test_extract_price_and_currency_not_found(mocker):
    mock_playwright = mocker.patch("verifier.sync_playwright")
    mock_page = MagicMock()
    
    # [CORREÇÃO AQUI]: Também precisamos zerar a contagem neste teste
    mock_page.locator.return_value.count.return_value = 0
    
    mock_page.content.return_value = "<html><body>Nenhum produto aqui</body></html>"
    
    # Pula a configuração completa e vai direto ao retorno do launch
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value.new_page.return_value = mock_page

    result = extract_price_and_currency("http://site-falso.com")
    
    assert result is None