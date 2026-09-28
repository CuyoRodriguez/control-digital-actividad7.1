import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.signals import calcular_senal_continua, calcular_senal_discreta


def cargar_css() -> None:
    css_path = Path(__file__).resolve().parent / "assets" / "styles" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            html, body, [data-testid="stAppViewContainer"] {
                font-size: 18px;
            }

            h1 {
                font-size: 2.2rem !important;
                color: #0F172A !important;
                font-weight: 700 !important;
                margin-bottom: 0.4rem !important;
            }

            h2, h3 {
                font-size: 1.4rem !important;
                color: #1E293B !important;
                font-weight: 700 !important;
                margin-top: 20px !important;
                margin-bottom: 0.35rem !important;
            }

            .stCaption {
                font-size: 1.05rem !important;
                color: #475569 !important;
            }

            p, span, label, div, .stMarkdown {
                font-size: 1.15rem;
                line-height: 1.5;
                color: #1E1E1E;
            }

            [data-testid="stMetricLabel"] {
                font-size: 1.05rem !important;
                font-weight: 700 !important;
                color: #1E1E1E !important;
            }

            [data-testid="stMetricValue"] {
                font-size: 1.65rem !important;
                font-weight: 800 !important;
                color: #1E1E1E !important;
            }

            .stMarkdown p {
                font-size: 1.08rem;
            }

            .stSlider label, .stNumberInput label {
                color: #1E1E1E !important;
                font-weight: 600;
            }

            .section-description {
                font-size: 1.05rem !important;
                line-height: 1.6;
                color: #475569 !important;
                margin-top: 0.35rem;
            }

            .card p,
            .card div,
            .card h3,
            .card span {
                font-size: 1.1rem !important;
                color: #334155 !important;
            }

            details {
                border: 1px solid #94A3B8 !important;
                border-radius: 10px !important;
                background: #E2E8F0 !important;
                margin-top: 1rem !important;
            }

            summary {
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                color: #0F172A !important;
                padding: 0.75rem 1rem !important;
                cursor: pointer !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


cargar_css()

st.set_page_config(
    page_title="Muestreo de señales",
    page_icon="📘",
    layout="wide",
)

st.title("Muestreo de señales en sistemas de control")
st.caption("Aplicación educativa para visualizar la señal continua, la señal discreta y el tren de muestreo.")

with st.container():
    st.markdown(
        """
        <div class="card">
            <h3>Parámetros del muestreo</h3>
            <p>Selecciona el período de muestreo para observar cómo cambia la representación discreta de la señal.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    periodo_muestreo = st.slider(
        "Período de muestreo T (s)",
        min_value=0.1,
        max_value=3.0,
        value=1.0,
        step=0.1,
        format="%.1f",
    )

    tiempo = np.linspace(0, 12, 400)
    senal = calcular_senal_continua(tiempo)

    instantes_muestreo, valores_muestreados = calcular_senal_discreta(
        periodo_muestreo,
        0,
        12,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Señal", "e(t)")
    col2.metric("Muestreo", "e(kT)")
    col3.metric("Período", f"{periodo_muestreo:.1f} s")

    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
    })

    with st.container():
        st.markdown("### 1. Señal continua e(t)")
        fig1, ax1 = plt.subplots(figsize=(8, 3), dpi=100)
        ax1.plot(tiempo, senal, color="#2f6fed", linewidth=2.2)
        ax1.set_xlabel("Tiempo, t")
        ax1.set_ylabel("Amplitud")
        ax1.tick_params(axis="both", which="major", labelsize=10)
        ax1.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)
        st.markdown(
            "<div class='section-description'>La señal continua está definida para cualquier instante de tiempo y representa la evolución de la variable en el tiempo.</div>",
            unsafe_allow_html=True,
        )

    with st.container():
        st.markdown("### 2. Señal discreta e(kT)")
        fig2, ax2 = plt.subplots(figsize=(8, 3), dpi=100)
        ax2.stem(instantes_muestreo, valores_muestreados, linefmt="#f39c12", markerfmt="o", basefmt="k-")
        ax2.set_xlabel("Instantes de muestreo, kT")
        ax2.set_ylabel("Valor")
        ax2.tick_params(axis="both", which="major", labelsize=10)
        ax2.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        st.markdown(
            "<div class='section-description'>La señal discreta toma los valores de la señal continua solo en los instantes t = kT, donde k es un entero.</div>",
            unsafe_allow_html=True,
        )

    with st.container():
        st.markdown("### 3. Señal de muestreo h(t)")
        fig3, ax3 = plt.subplots(figsize=(8, 3), dpi=100)
        ax3.stem(instantes_muestreo, np.ones_like(instantes_muestreo), linefmt="#28a745", markerfmt="^", basefmt="k-")
        ax3.set_xlabel("Tiempo, t = kT")
        ax3.set_ylabel("h(t)")
        ax3.tick_params(axis="both", which="major", labelsize=10)
        ax3.set_ylim(0, 1.2)
        ax3.grid(True, axis="x", linestyle="--", alpha=0.4)
        plt.tight_layout()
        st.pyplot(fig3, use_container_width=True)
        st.markdown(
            "<div class='section-description'>El tren de muestreo representa los instantes en los que la señal continua es capturada para producir la versión discreta.</div>",
            unsafe_allow_html=True,
        )

    with st.expander("🎬 Ver animación de apoyo", expanded=False):
        gif_path = os.path.join(os.path.dirname(__file__), "assets", "problema.gif")

        if os.path.exists(gif_path):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(gif_path, caption="Demostración visual", width=400)
        else:
            st.warning("No se encontró el archivo del GIF en la ruta especificada.")
