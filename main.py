# main.py
from scraper.core import scrape_products
from scraper.utils import save_to_json, save_to_csv, log_message


def main():
    log_message("🚀 Iniciando scraper de Éxito...")
    results = scrape_products()
    if not results:
        log_message("⚠️ No se encontraron productos.")
        return


    # Guardar JSON
    json_filename = "snacks.json"
    save_to_json(results, filename=json_filename)
    log_message(f"✅ JSON guardado en {json_filename} (total: {len(results)})")

    # Guardar CSV
    csv_filename = "snacks.csv"
    save_to_csv(results, filename=csv_filename, add_timestamp=False)
    log_message(f"✅ CSV guardado en {csv_filename} (total: {len(results)})")


if __name__ == "__main__":
    main()