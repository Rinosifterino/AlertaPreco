from verifier import extract_price_and_currency

url = input("url:")
selector = input("selector:")

print(extract_price_and_currency(url, selector))