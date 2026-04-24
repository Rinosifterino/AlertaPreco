import os
import pytest
from monitor import _is_valid_variation, _update_monitor_csv

def test_is_valid_variation():
    # Deve aceitar aumentos normais
    assert _is_valid_variation(old_price=100.0, new_price=150.0) is True
    assert _is_valid_variation(old_price=50.0, new_price=450.0) is True
    
    # Deve rejeitar aumentos maiores que 10x (filtro de bug do HTML)
    assert _is_valid_variation(old_price=100.0, new_price=1100.0) is False

def test_update_monitor_csv(tmp_path, mocker):
    # Redireciona o arquivo CSV para uma pasta temporária de testes
    fake_csv_path = tmp_path / "fake_monitor.csv"
    mocker.patch("monitor.MONITOR_CSV", str(fake_csv_path))
    
    # Executa a função
    _update_monitor_csv("user@mail.com", "http://leilao", 50.0, 75.0, "USD")
    
    # Lê o arquivo temporário para verificar os dados
    assert os.path.exists(fake_csv_path)
    with open(fake_csv_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "email,url,original_price,current_price,currency" in content
        assert "user@mail.com,http://leilao,50.0,75.0,USD" in content