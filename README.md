# LAS-Visualizer

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![PRs](https://img.shields.io/badge/PRs-Welcome-orange)

🚀 Aplicación interactiva para la **visualización de archivos LAS** usados en registros eléctricos de pozos petroleros. Desarrollado con **Streamlit**, **Matplotlib** y **Plotly**, este visualizador permite cargar, explorar y graficar curvas de manera intuitiva.



---

## 📌 Características

- 📂 Carga de archivos `.LAS` desde la interfaz.
- 📋 Visualización de metadatos: versión, información del pozo y unidades.
- 📊 Gráficas tipo tracks (curvas paralelas) con Matplotlib o Plotly.
- 🧮 Filtro por rango de profundidad.
- 🎯 Selección dinámica de curvas usando controles interactivos (pills).
- 📈 Vista previa del DataFrame filtrado con estilo mejorado.
- 🎨 Página de inicio personalizada con HTML/CSS.

---

## 🛠️ Tecnologías utilizadas

- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)
- [Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)
- [Lasio](https://lasio.readthedocs.io/)

---

## 📷 Captura de pantalla

![Captura](Captura.jpg)

---

## 📁 Estructura del repositorio

```bash
# Carpeta raíz del proyecto
LAS-Visualizer/
├── Archivo principal de la aplicación Streamlit
├── app.py                     
├── Documentación del proyecto
├── README.md                 
├── Logo de la marca personal (usado en el sidebar)
├── Logo Carlos Carrillo.png  
├── Carpeta para almacenar archivos LAS de ejemplo
├── Data/
     └── Aquí puedes colocar archivos .las para pruebas
```

---

## 🧑‍💻 Autor

**Carlos Carrillo Villavicencio**  
MSc. en TIC | Instructor de Python para la industria Oil & Gas  
🔗 [LinkedIn](https://www.linkedin.com/in/carlos-carrillo-villavicencio) *(agrega tu enlace real)*  

---

## ✅ Estado del proyecto

> En desarrollo activo. Próximas funciones:
> - Descarga de reportes en CSV.
> - Estadísticas por curva.
> - Modo oscuro.
