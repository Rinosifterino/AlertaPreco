import pytest
from unittest.mock import MagicMock
from verifier import extract_price_and_currency

def test_extract_price_and_currency_success(mocker):
    # Simula o contexto do Playwright
    mock_playwright = mocker.patch("verifier.sync_playwright")
    
    # MOCK DO LOGGER: Evita que o teste escreva no arquivo log.txt real
    mocker.patch("verifier.log_action")
    
    mock_page = MagicMock()
    
    # Ensina o mock a encontrar o elemento (count = 1)
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
    
    # Retorno atualizado do seu código: currency, price, prefix
    currency, price, prefix = result 
    
    assert price == 39.95
    assert currency == "EUR"
    assert prefix == "Valor Atual:"

def test_extract_price_and_currency_not_found(mocker):
    mock_playwright = mocker.patch("verifier.sync_playwright")
    mocker.patch("verifier.log_action") # Impede escrita no log
    
    mock_page = MagicMock()
    mock_page.locator.return_value.count.return_value = 0
    mock_page.content.return_value = "<html><body>Nenhum produto aqui</body></html>"
    
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value.new_page.return_value = mock_page

    result = extract_price_and_currency("http://site-falso.com")
    assert result is None

# NOVO TESTE: Valida a sua "Limpeza Inteligente" de números
@pytest.mark.parametrize("raw_html, expected_price", [
    ("<html><body>US$ 77,730.59</body></html>", 77730.59),  # Formato US (Vírgula milhar, ponto decimal)
    ("<html><body>R$ 77.730,59</body></html>", 77730.59),   # Formato BR (Ponto milhar, vírgula decimal)
    ("<html><body>€ 1.500</body></html>", 1500.0),           # Ponto isolado como milhar
    ("<html><body>R$ 500,00</body></html>", 500.0),          # Apenas decimal BR
])
def test_number_cleaning_logic(mocker, raw_html, expected_price):
    mock_playwright = mocker.patch("verifier.sync_playwright")
    mocker.patch("verifier.log_action")
    
    mock_page = MagicMock()
    mock_page.locator.return_value.count.return_value = 0 # Força a falha do seletor para usar o HTML inteiro
    mock_page.content.return_value = raw_html
    
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value.new_page.return_value = mock_page

    result = extract_price_and_currency("http://site-falso.com")
    
    assert result is not None
    _, price, _ = result # Ignoramos moeda e prefixo, focamos só no preço extraído
    
    assert price == expected_price