# scraper/parser.py
from bs4 import BeautifulSoup
import re


# ========= PARSER SELENIUM/HTML =========
def parse_products_html(html: str):
    """Parsea productos desde HTML renderizado por Selenium."""
    soup = BeautifulSoup(html, "lxml")
    products_data = []

    product_cards = soup.select("[data-fs-product-card]")

    # for card in product_cards:
    for idx, card in enumerate(product_cards, start=1):

        name_tag = card.select_one("span.vtex-product-summary-2-x-productBrand")
        price_tag = card.select_one("span.exito-vtex-components-4-x-currencyInteger")
        discount_tag = card.select_one("span.exito-vtex-components-4-x-currencyDiscount")
        desc_tag = card.select_one("span.vtex-product-summary-2-x-productNameContainer")
        link_tag = card.select_one("a.vtex-product-summary-2-x-clearLink")

        name = name_tag.get_text(strip=True) if name_tag else "N/A"
        description = desc_tag.get_text(strip=True) if desc_tag else "N/A"
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        discount = discount_tag.get_text(strip=True) if discount_tag else "N/A"
        link = f"https://www.exito.com{link_tag['href']}" if link_tag else "N/A"

        # Intentar extraer marca (usamos la primera palabra del nombre como fallback)
        marca = name.split()[0] if name != "N/A" else "N/A"

        # Calcular precio por gramo si hay peso en el texto
        price_per_gram = "N/A"
        import re
        match = re.search(r"(\d+)\s*(g|gr|gramos)", f"{name} {description}", re.IGNORECASE)
        try:
            numeric_price = float(price.replace(".", "").replace(",", "."))
            if match:
                grams = int(match.group(1))
                if grams > 0:
                    price_per_gram = round(numeric_price / grams, 2)
        except:
            pass

        products_data.append({
            #"item": name,
            "item": idx,
            "marca": marca,
            #"descripcion": description,
            "descripcion": name,
            "precio": price,
            "descuento": discount,
            "precio_x_gramo": price_per_gram,
            "link": link
        })

    return products_data


# ========= PARSER API JSON =========
def parse_products_api(data: list):
    """Parsea productos desde la API de Éxito."""
    products_data = []

    #for product in data:
    for idx, product in enumerate(data, start=1):

        name = product.get("productName", "N/A")
        brand = product.get("brand", "N/A")
        description = product.get("description", "N/A")
        link = f"https://www.exito.com/{product.get('linkText', '')}"

        try:
            offer = product["items"][0]["sellers"][0]["commertialOffer"]
            price = offer.get("Price", "N/A")
            list_price = offer.get("ListPrice", price)
        except (IndexError, KeyError, TypeError):
            price = "N/A"
            list_price = "N/A"

        # Calcular descuento
        discount = "N/A"
        if isinstance(price, (int, float)) and isinstance(list_price, (int, float)) and list_price > price:
            discount = round((list_price - price) / list_price * 100, 2)

        # Calcular precio por gramo
        price_per_gram = "N/A"
        match = re.search(r"(\d+)\s*(g|gr|gramos)", f"{name} {description}", re.IGNORECASE)
        if match and isinstance(price, (int, float)):
            grams = int(match.group(1))
            if grams > 0:
                price_per_gram = round(price / grams, 2)

        products_data.append({
            "item": idx,
            "marca": brand,
            "descripcion": name,
            "precio": price,
            "descuento": discount,
            "precio_x_gramo": price_per_gram,
            "link": link
        })
    return products_data
