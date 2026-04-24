
# 🚀 Auction Price Monitor (AlertaPreço)

Sistema automatizado em Python projetado para monitorar lances e variações de preços em sites de leilões ou e-commerce. O software utiliza web scraping para detectar aumentos de valores em tempo real e notifica o usuário via e-mail.

## 📋 Funcionalidades

* **Monitoramento Inteligente**: Realiza checagens periódicas em URLs para detectar mudanças de preço.
* **Lógica de Leilão**: O sistema foca em detectar especificamente **aumentos** de preço e ignora anomalias (como picos superiores a 10x o valor atual).
* **Notificações por E-mail**: Dispara alertas automáticos via SMTP sempre que um novo lance é detectado ou quando o monitoramento é iniciado.
* **Registro de Logs**: Mantém um registro detalhado de todas as ações com carimbo de data/hora (timestamp) no arquivo `log.txt`.
* **Persistência de Dados**:
    * `monitor.csv`: Armazena o estado atual do item (preço original, atual e moeda).
    * `historico.csv`: Registra o histórico de todos os saltos de preço detectados para análise futura.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**: Linguagem base do projeto.
* **Playwright**: Motor de automação para extração de dados do DOM.
* **python-dotenv**: Gestão de credenciais sensíveis via variáveis de ambiente.
* **CustomTkinter**: Interface visual para interação com o usuário.
=======
pip install -r requirements.txt  
playwright install  
python -m pytest -v

