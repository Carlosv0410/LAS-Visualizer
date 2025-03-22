# streamlit_app.py

import streamlit as st
import pandas as pd
import lasio
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import numpy as np
import random

# Configurar la página
st.set_page_config(page_title="Visualización de Registros Eléctricos", layout="wide")

# Mostrar logo en el sidebar
st.sidebar.image("Logo Carlos Carrillo.png", use_container_width=True)

# Estilos personalizados para el Home en HTML + CSS
custom_home = '''
<style>
    .custom-box {
        background: linear-gradient(135deg, #001f3f, #0074D9);
        border-radius: 20px;
        padding: 30px;
        color: white;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        text-align: center;
        margin-top: 40px;
    }
    .custom-box h1 {
        font-size: 32px;
        margin-bottom: 10px;
    }
    .custom-box p {
        font-size: 18px;
        line-height: 1.5;
    }
</style>
<div class="custom-box">
    <h1>Visualizador de Registros Eléctricos</h1>
    <p><strong>Desarrollado por:</strong> Carlos Carrillo Villavicencio</p>
    <p><em>MSc. en TIC | Instructor de Python para Oil & Gas</em></p>
    <p>Esta aplicación permite visualizar y analizar archivos <code>.LAS</code> de registros eléctricos, utilizados en la industria petrolera.</p>
    <p><strong>¿Qué puedes hacer?</strong></p>
    <ul style="text-align: left; max-width: 600px; margin: 0 auto;">
        <li>Cargar archivos LAS</li>
        <li>Seleccionar curvas de interés</li>
        <li>Filtrar por profundidad</li>
        <li>Visualizar con Matplotlib o Plotly</li>
    </ul>
    <p style="margin-top: 30px;">Usa el menú lateral para comenzar 🔍</p>
</div>
'''

# Sidebar - Navegación y carga
st.sidebar.title("Menú de Navegación")
seccion = st.sidebar.selectbox("Ir a sección:", ["Home", "Visualización"])

# Sidebar - Carga de archivo
archivo = st.sidebar.file_uploader("Cargar archivo LAS", type=[".las"])

# Diccionario de colores
colores = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'cyan']

if seccion == "Home":
    st.markdown(custom_home, unsafe_allow_html=True)

elif seccion == "Visualización":
    st.title("Visualización de Registros Eléctricos en la Industria del Petróleo")

    if archivo is not None:
        with st.spinner("Leyendo archivo LAS..."):
            las = lasio.read(io.StringIO(archivo.getvalue().decode("utf-8")))
            df = las.df()
            columnas = df.columns.tolist()
            profundidad = df.index

        tabs = st.tabs(["Versión LAS", "WELL Info", "Curvas y Unidades"])

        with tabs[0]:
            st.subheader("Versión del archivo LAS")
            st.text(f"{las.version}")

        with tabs[1]:
            st.subheader("Encabezado del Archivo (WELL)")
            st.text(str(las.well))

        with tabs[2]:
            st.subheader("Curvas detectadas y sus unidades")
            st.text(str(las.curves))

        # Layout en dos columnas
        col1, col2 = st.columns([1, 2])

        with col1:
            min_depth = float(profundidad.min())
            max_depth = float(profundidad.max())
            depth_range = st.slider("Selecciona el rango de profundidad", min_value=min_depth, max_value=max_depth,
                                     value=(min_depth, max_depth), step=0.5)

            st.markdown("#### Selecciona las curvas a visualizar")
            curvas_seleccionadas = st.pills("Curvas", columnas, selection_mode="multi")
            tipo_grafico = st.radio("Selecciona el tipo de gráfico", ["Matplotlib", "Plotly"])

            df_filtrado = df.loc[(df.index >= depth_range[0]) & (df.index <= depth_range[1])]

            if curvas_seleccionadas:
                df_filtrado = df_filtrado[curvas_seleccionadas]

                st.subheader("Vista interactiva del DataFrame")
                st.dataframe(
                    df_filtrado,
                    column_config={
                        col: st.column_config.NumberColumn(
                            label=col,
                            help=f"Valores de {col} en el rango seleccionado",
                            format="%.2f"
                        ) for col in curvas_seleccionadas
                    },
                    use_container_width=True,
                )

        with col2:
            if curvas_seleccionadas:
                st.markdown("### Visualización")
                if tipo_grafico == "Matplotlib":
                    n = len(curvas_seleccionadas)
                    fig, axes = plt.subplots(1, n, figsize=(2.5 * n, 6), sharey=True)
                    axes = axes if isinstance(axes, (list, np.ndarray)) else [axes]

                    for i, curva in enumerate(curvas_seleccionadas):
                        color = colores[i % len(colores)]
                        ax = axes[i]
                        ax.plot(df_filtrado[curva], df_filtrado.index, lw=0.7, color=color)
                        ax.set_xlabel(curva)
                        ax.invert_yaxis()
                        ax.grid(True, linestyle='--', linewidth=0.5)
                        ax.set_title(f'Curva: {curva}')

                        ax.tick_params(axis='x', labelbottom=False)
                        if i == 0:
                            ax.set_ylabel('Profundidad (DEPT)', fontsize=10)
                        else:
                            ax.tick_params(labelleft=False)

                        ax_top = ax.twiny()
                        ax_top.set_xlim(ax.get_xlim())
                        ax_top.spines['top'].set_position(('outward', 40))
                        ax_top.set_xlabel(f'{curva} [escala]', fontsize=10, color=color)
                        ax_top.tick_params(axis='x', colors=color, labelsize=9)

                    st.pyplot(fig)
                else:
                    n = len(curvas_seleccionadas)
                    fig = make_subplots(rows=1, cols=n, shared_yaxes=True, horizontal_spacing=0.02)
                    for i, curva in enumerate(curvas_seleccionadas):
                        color = colores[i % len(colores)]
                        fig.add_trace(
                            go.Scatter(x=df_filtrado[curva], y=df_filtrado.index, mode='lines', line=dict(color=color),
                                       name=curva, showlegend=False),
                            row=1, col=i+1
                        )
                        fig.update_xaxes(title_text=curva, showgrid=True, zeroline=False, row=1, col=i+1)

                    fig.update_yaxes(autorange="reversed", title="Profundidad (DEPT)", showgrid=True, zeroline=False, row=1, col=1)
                    fig.update_layout(
                        height=600,
                        title_text="Curvas en paralelo (tracks)",
                        margin=dict(t=50, b=40, l=40, r=40),
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                    )
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Por favor, carga un archivo LAS para comenzar.")
