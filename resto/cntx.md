Segue todo o contexto estruturado em **Markdown (.md)** para você reutilizar em outro chat:

---

```md
# 📊 Price Monitor System (Playwright + Email + CSV)

## 1. Project Overview

**Goal:**  
Develop a system to monitor prices on any web page and trigger an action (send email) when a change is detected.

**Architecture:**
- Python modular system
- Playwright (web scraping dinâmico)
- SMTP (Gmail) para envio de email
- CSV para persistência de dados

**Files:**
- `main.py` → Entry point
- `verifier.py` → Extrai preço
- `notifier.py` → Envia email
- `monitor.py` → Loop de monitoramento
- `debug.py` → Ferramenta de testes
- `.env` → Variáveis sensíveis

---

## 2. Coding Standards

- **PEP 8**
- **PEP 257**
- Docstrings e comentários → **Português**
- Código (variáveis/funções/classes) → **Inglês**

### Naming:
- Classes → PascalCase
- Functions/variables → snake_case
- Constants → SCREAMING_SNAKE_CASE

---

## 3. Core Features

### ✔ Web Scraping (Playwright)
- Renderiza páginas com JavaScript
- Funciona com sites dinâmicos (eBay, Amazon)

### ✔ Price Detection Strategy
1. CSS Selector (usuário)
2. Site específico (Amazon)
3. Genérico (class/id com "price")
4. Regex fallback

---

## 4. Problem Found

Problema real identificado:

- Sistema capturando valores errados:
  - Frete
  - Produtos similares
  - Preços secundários

Exemplo de erro:
```

8.00  ✅ (correto)
28.99 ❌
46.48 ❌
145.18 ❌

```

---

## 5. Solution Implemented

### ✔ 1. Price History (CSV)

Arquivo:
```

price_history.csv

````

Salva TODOS os valores capturados:

```csv
price
8.00
28.99
46.48
145.18
````

---

### ✔ 2. Smart Filter

```python
def _is_valid_price(new_price, last_price):
    if new_price > last_price * 3:
        return False
    if new_price < last_price * 0.3:
        return False
    return True
```

Evita:

* preços absurdos
* ruído da página

---

### ✔ 3. CSV Principal

```
monitor.csv
```

Estrutura:

```csv
email,url,original_price,current_price
user@email.com,https://...,8.00,9.50
```

---

## 6. Monitoring Logic

### Primeiro Scan:

* pega preço inicial
* salva CSV
* envia email inicial ("monitorando")

### Loop:

* espera `delay_time`
* pega novo preço
* compara com anterior
* se subir:

  * envia email
  * atualiza CSV

---

## 7. Environment Variables (.env)

```env
email=seu_email@gmail.com
app_password=senha_app
delay_time=30
```

---

## 8. Debug System (`debug.py`)

Ferramenta interativa:

```bash
python debug.py
```

Menu:

```
1 - Get price from URL
2 - Exit
```

Função:

* testa scraping isoladamente
* útil para testes unitários futuros

---

## 9. Selectors Guide

### Amazon

```
.a-price .a-offscreen
```

### eBay

```
.x-price-primary span
```

ou

```
span[itemprop="price"]
```

---

## 10. Test Site Recommendation

Use eBay auctions:

```
https://www.ebay.com/sch/i.html?_nkw=auction&_sop=1
```

Motivos:

* preço muda frequentemente
* ideal para testes reais

---

## 11. Big O Analysis

* Scraping → O(1) (externo)
* Parsing → O(n)

Dominante:

```
O(n)
```

---

## 12. System Guarantees

✔ Não quebra com input inválido
✔ Logging completo no console
✔ Persistência em CSV
✔ Monitoramento contínuo
✔ Notificação por email

---

## 13. Future Improvements

* 📊 gráfico de histórico
* 🔁 múltiplas URLs simultâneas
* 🧠 detecção automática de preço correto
* 🌐 interface web
* 🧪 testes automatizados com pytest

---

## 14. Final Architecture

```
main.py
   ↓
monitor.py (loop + lógica)
   ↓
verifier.py (scraping)
   ↓
notifier.py (email)
   ↓
CSV (persistência)
```

---

## 🚀 Resultado

Sistema completo de monitoramento de preços com:

* scraping robusto
* filtro inteligente
* histórico de dados
* debug interativo
* notificações automáticas

Pronto para avaliação acadêmica e uso real.

```

---

Se quiser, posso na próxima te gerar:
- 📄 :contentReference[oaicite:0]{index=0}
- 📊 :contentReference[oaicite:1]{index=1}
- 🧪 :contentReference[oaicite:2]{index=2}

Só falar 👍
```
