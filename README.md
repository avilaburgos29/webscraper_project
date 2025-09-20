# 🛒 WebScraper - Python - Selenium

Este proyecto es un **scraper en Python** diseñado para extraer información de productos desde la configuración de una ruta (url).

Ofrece **dos modos de funcionamiento**:  
1. **API JSON** → Más rápido y confiable.  
2. **Selenium** → Scraping directo del HTML, útil como respaldo.  

Los resultados se pueden exportar en **CSV** y **JSON** para análisis posterior.  

---



## 📂 Estructura del proyecto

webscraper_project/
│── scraper/
│   ├── core.py         # Lógica principal (API y Selenium)
│   ├── parser.py       # Procesamiento de productos
│   ├── utils.py        # Guardado en JSON/CSV + logs
│── main.py             # Script principal para ejecutar scraping
│── requirements.txt    # Dependencias del proyecto
│── README.md           # Documentación del proyecto

---

## ⚙️ Instalación

## 1️⃣ Clonar repositorio

git clone https://github.com/tu-usuario/webscraper_project.git

cd webscraper_project

### 2️⃣ Crear y activar un entorno virtual (opcional pero recomendado).


python -m venv venv

source venv/bin/activate   # En Linux / Mac

venv\Scripts\activate      # En Windows

### 3️⃣ Instalar dependencias


pip install -r requirements.txt

💡 Si usas Selenium, instala también:

pip install webdriver-manager

---

## 🚀 Uso

Ejecuta el scraper desde la terminal:

### Usar API de Éxito

python main.py --mode api --export both --output snacks_api

### Usar Selenium

python main.py --mode selenium --export csv --output snacks_html


---

## 📑 Parámetros disponibles

--mode → Modo de scraping (api o selenium).

--export → Tipo de exportación (csv, json, both).

--output → Nombre base de los archivos generados.

### Ejemplo:

python main.py --mode api --export both --output snacks_resultados

Generará:

snacks_resultados.json

snacks_resultados.csv


---

## 📊 Campos extraídos

Item → contador incremental

Marca → marca del producto

Descripción → nombre del producto

Precio x gramo → calculado si se encuentra peso en la descripción

Descuento → precio anterior o de lista

Precio → precio actual del producto


---

## ⚠️ Notas importantes

El scraping con Selenium requiere tener Google Chrome instalado.

Si Selenium falla en Windows, puedes instalar el driver con:


pip install webdriver-manager


Se recomienda usar el modo API, más rápido y estable.

---

## 🛠️ Requisitos

Python 3.9+

### Librerías:

requests

beautifulsoup4

selenium

pandas


Instalar con:

pip install -r requirements.txt

---

## 👨‍💻 Autor

Desarrollado por Marvin Ávila Burgos

Data Engineer


