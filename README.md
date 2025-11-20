# SmartEcoHome

Proyecto final: **SmartEcoHome** — Interfaz multimodal para controlar una habitación simulada.

## Estructura
- `Inicio.py` - página principal (Streamlit).
- `pages/control.py` - controles por botones y lectura de sensores.
- `pages/voz_ctr.py` - enviar comandos por audio (subida de archivo).
- `pages/imagen.py` - detectar personas desde imagen y accionar la luz.
- `requirements.txt` - dependencias.

## Cómo ejecutar (local)
1. Crear un entorno virtual (recomendado).
2. `pip install -r requirements.txt`
3. Ejecutar:
   ```bash
   streamlit run Inicio.py
