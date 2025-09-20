# scraper/utils.py
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional, Any


def save_to_json(data: List[Dict[str, Any]], filename: str = "output.json") -> None:
    """Guarda los resultados en un archivo JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_csv(
    data: List[Dict[str, Any]],
    filename: str = "output.csv",
    fieldnames: Optional[List[str]] = None,
    add_timestamp: bool = False,
    append: bool = False
) -> None:
    """
    Guarda los resultados en CSV.
    - data: lista de diccionarios homogéneos (cada dict = un producto)
    - filename: nombre del archivo (extensión .csv será respetada/añadida)
    - fieldnames: orden de columnas; si None se deducen de los keys (prioriza orden por defecto)
    - add_timestamp: añade timestamp al nombre del archivo antes de la extensión
    - append: si True escribe en modo append (no reescribe header si el archivo ya existe)
    """
    if not data:
        print("[save_to_csv] No hay datos para guardar.")
        return

    # Orden preferente de columnas
    default_order = ["item", "marca", "descripcion", "precio_x_gramo", "descuento", "precio", "link"]

    # Deducir fieldnames a partir de keys en data si no fueron provistos
    if fieldnames is None:
        keys = []
        for row in data:
            for k in row.keys():
                if k not in keys:
                    keys.append(k)
        # Priorizar el default_order
        fieldnames = [k for k in default_order if k in keys] + [k for k in keys if k not in default_order]

    # Añadir timestamp si se solicita
    if add_timestamp:
        base, dot, ext = filename.rpartition('.')
        if dot == '':
            base = filename
            ext = 'csv'
        filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

    mode = 'a' if append else 'w'
    # utf-8-sig para compatibilidad con Excel (agrega BOM)
    with open(filename, mode, newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        # escribir header si vamos a reescribir o el archivo está vacío (modo append + tamaño 0)
        if mode == 'w' or (mode == 'a' and f.tell() == 0):
            writer.writeheader()

        for row in data:
            clean_row = {}
            for key in fieldnames:
                val = row.get(key, "")
                # normalizamos listas y dicts a cadenas para CSV
                if isinstance(val, (list, tuple)):
                    val = "; ".join(str(x) for x in val)
                elif isinstance(val, dict):
                    val = json.dumps(val, ensure_ascii=False)
                # None -> ""
                if val is None:
                    val = ""
                clean_row[key] = val
            writer.writerow(clean_row)

    print(f"[save_to_csv] {len(data)} filas guardadas en {filename}")


def log_message(message: str) -> None:
    """Agrega timestamp a los mensajes de log."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
