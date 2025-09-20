# scraper/core.py
import time
import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS, TIMEOUT, SCRAPER_MODE
from scraper.parser import parse_products_html, parse_products_api
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def fetch_page_selenium(url: str) -> str:
    options = Options()
    options.add_argument("--headless")  # Opcional, para no abrir ventana
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def old_fetch_page_selenium(url: str) -> str:
    """Descarga la página renderizada con JS usando Selenium."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # espera carga de productos
    html = driver.page_source
    driver.quit()
    return html


# ========== MÉTODO API JSON ==========
def fetch_products_api():
    """Usa la API interna de VTEX para obtener los productos en JSON."""
    url = "https://www.exito.com/api/catalog_system/pub/products/search/mercado/pasabocas-y-snacks"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error API: {e}")
        return []


# ========== CONTROLADOR PRINCIPAL ==========
def scrape_products():
    """Selecciona el modo de scraping según config.py"""
    if SCRAPER_MODE == "selenium":
        html = fetch_page_selenium(BASE_URL)
        return parse_products_html(html)
    elif SCRAPER_MODE == "api":
        data = fetch_products_api()
        return parse_products_api(data)
    else:
        raise ValueError("⚠️ Modo de scraping inválido. Usa 'selenium' o 'api'.")
