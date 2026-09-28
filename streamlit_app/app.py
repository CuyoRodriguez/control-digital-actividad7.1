import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

st.set_page_config(page_title="Control Digital con Streamlit", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { background-color: #1E293B; color: #F8FAFC; }
    .stApp {
        font-family: 'Segoe UI', sans-serif;
        background: #F8FAFC;
        color: #334155;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #111827 100%);
        color: #E2E8F0;
    }
    div[data-testid="stSidebar"] .stContainer,
    div[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        margin-bottom: 0.75rem;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
    }
    div[data-testid="stSidebar"] .stMarkdown,
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] li,
    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        color: #F8FAFC !important;
    }
    [data-testid="stSuccess"] {
        background: rgba(37, 99, 235, 0.08);
        border: 1px solid rgba(37, 99, 235, 0.35);
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        color: #1E3A8A;
        padding: 0.8rem 1rem;
    }
    [data-testid="stError"] {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-left: 5px solid #dc2626;
        border-radius: 10px;
        color: #7f1d1d;
        padding: 0.8rem 1rem;
    }
    .stTabs [role="tablist"] {
        gap: 0.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [role="tablist"] button[role="tab"] {
        background: rgba(255,255,255,0.8);
        border: 1px solid #E2E8F0;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.04);
        color: #475569;
    }
    .stTabs [role="tablist"] button[role="tab"][aria-selected="true"] {
        background: #ffffff;
        border-bottom: 3px solid #2563EB;
        color: #0F172A;
    }
    [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    .stTabs [role="tabpanel"] > div {
        background: rgba(255,255,255,0.94);
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 {
        color: #0F172A;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Variables simbólicas
z, K, s, b = sp.symbols('z K s b', real=True)

# Funciones de transferencia
G = 1 / (z - sp.Rational(1, 2))
Gc = (K * z) / (z - 1)

# Polinomios para la segunda parte de la actividad (Routh-Hurwitz)
P3_actividad = z**2 - 3*z + b
P4_actividad = z**2 + (K - sp.Rational(1, 5))*z + K

# Polinomios de la primera parte de la actividad
P1_actividad = z**2 + 2*K*z + 1
P2_actividad = z**3 + 2*z**2 - 3*z + 1

# Ecuación característica del lazo cerrado: 1 + Gc(z) * G(z) = 0
char_expr = sp.simplify(1 + Gc * G)
num, den = sp.fraction(sp.together(char_expr))
P = sp.expand(num)
poly = sp.Poly(P, z)

# Criterio de Jury para el polinomio de segundo orden: P(z) = z^2 + a1*z + a0
coeffs = poly.all_coeffs()
a2 = coeffs[0]
a1 = coeffs[1]
a0 = coeffs[2]

P1 = sp.simplify(P.subs(z, 1))
Pm1 = sp.simplify(P.subs(z, -1))

# Despeje de K para las condiciones del criterio de Jury
cond1_ineq = sp.solve_univariate_inequality(P1 > 0, K)
cond2_ineq = sp.solve_univariate_inequality(Pm1 > 0, K)
cond3_check = abs(a0) < a2
combined_limits = sp.reduce_inequalities([P1 > 0, Pm1 > 0], K)

st.title("Control Digital con Streamlit")
st.caption("Análisis de estabilidad y respuesta al escalón del sistema en lazo cerrado.")

st.sidebar.markdown("### Control digital y estabilidad")
with st.sidebar.container(border=True):
    st.markdown(
        """
        En sistemas discretos, la estabilidad ya no se interpreta con el eje real del plano s, sino con el plano z.
        Un sistema es estable cuando sus polos quedan dentro del círculo unitario, es decir, cuando $|z_i| < 1$.
        """
    )

with st.sidebar.container(border=True):
    st.markdown(
        """
        El Criterio de Jury permite determinar, a partir del polinomio característico, si todas las raíces del sistema discreto pertenecen a ese círculo unitario sin resolverlas explícitamente.
        """
    )

with st.sidebar.container(border=True):
    st.markdown(
        r"""
        Por otro lado, el mapeo bilineal transforma el plano z al plano s mediante $z = \frac{1+s}{1-s}$, lo cual facilita el análisis de estabilidad usando herramientas continuas como el criterio de Routh-Hurwitz.
        """
    )

analysis_tab, additional_tab, simulation_tab, tab4 = st.tabs([
    "Análisis Matemático",
    "Criterios Adicionales",
    "Simulación de Respuesta",
    "Ejemplo Práctico",
])

with analysis_tab:
    with st.container(border=True):
        st.subheader("Funciones de transferencia")
        st.latex(r"G(z) = \frac{1}{z - 0.5}")
        st.latex(r"G_c(z) = \frac{K z}{z - 1}")
        st.latex(f"G(z) = {sp.latex(G)}")
        st.latex(f"G_c(z) = {sp.latex(Gc)}")

        st.subheader("Ecuación característica del lazo cerrado")
        st.latex(r"1 + G_c(z)G(z) = 0")
        st.latex(r"1 + \frac{Kz}{z-1}\cdot\frac{1}{z-0.5} = 0")
        st.latex(f"{sp.latex(sp.together(1 + Gc * G))} = 0")

        st.latex(r"\Rightarrow \frac{P(z)}{(z-1)(z-0.5)} = 0")
        st.latex(f"P(z) = {sp.latex(P)}")
        st.latex(f"P(z) = {sp.latex(poly.as_expr())}")
        st.latex(r"P(z) = z^2 + \left(K - \frac{3}{2}\right)z + \frac{1}{2}")

        st.write("Polinomio agrupado por potencias de z:")
        st.latex(f"P(z) = {sp.latex(sp.expand(P))}")

        st.subheader("Criterio de Jury")
        with st.container():
            st.latex(r"P(z) = z^2 + a_1 z + a_0, \quad a_0 = \frac{1}{2}, \quad a_2 = 1")
            st.latex(f"a_0 = {sp.latex(a0)}")
            st.latex(f"a_2 = {sp.latex(a2)}")

            st.latex(r"1)\; P(1) > 0")
            st.latex(f"P(1) = {sp.latex(P1)}")
            st.latex(rf"P(1) > 0 \Rightarrow {sp.latex(cond1_ineq)}")

            st.latex(r"2)\; P(-1) > 0")
            st.latex(f"P(-1) = {sp.latex(Pm1)}")
            st.latex(rf"P(-1) > 0 \Rightarrow {sp.latex(cond2_ineq)}")

            st.latex(r"3)\; |a_0| < a_2")
            st.latex(rf"|a_0| < a_2 \Rightarrow {sp.latex(abs(a0))} < {sp.latex(a2)}")
            st.latex(r"\left|\frac{1}{2}\right| < 1 \Rightarrow \text{se cumple para todo } K")

            st.latex(r"\text{Conjunto final: } 0 < K < 3")
            st.latex(rf"\text{{Reduciendo ambas condiciones: }} {sp.latex(combined_limits)}")

            if cond3_check:
                st.success("Sistema estable según el Criterio de Jury: 0 < K < 3")
            else:
                st.error("No se cumple la condición 3 del Criterio de Jury.")

with additional_tab:
    with st.container(border=True):
        st.subheader("Primera parte de la actividad: análisis de Jury")

        with st.container():
            coeffs_p1 = sp.Poly(P1_actividad, z).all_coeffs()
            a2_p1 = coeffs_p1[0]
            a0_p1 = coeffs_p1[2]
            P1_val_1 = sp.expand(P1_actividad.subs(z, 1))
            P1_val_m1 = sp.expand(P1_actividad.subs(z, -1))
            final_p1 = sp.reduce_inequalities([P1_val_1 > 0, P1_val_m1 > 0, sp.Abs(a0_p1) < a2_p1], K)

            st.latex(r"P_1(z) = z^2 + 2Kz + 1")
            st.latex(f"P_1(z) = {sp.latex(P1_actividad)}")
            st.latex(r"\text{Para } P_1(z), \; a_2 = 1, \; a_1 = 2K, \; a_0 = 1")
            st.latex(r"1)\; P_1(1) > 0")
            st.latex(f"P_1(1) = {sp.latex(P1_val_1)}")
            st.latex(r"P_1(1) = 1 + 2K + 1 = 2 + 2K > 0")
            st.latex(rf"\Rightarrow {sp.latex(sp.reduce_inequalities([P1_val_1 > 0], K))}")

            st.latex(r"2)\; P_1(-1) > 0")
            st.latex(f"P_1(-1) = {sp.latex(P1_val_m1)}")
            st.latex(r"P_1(-1) = 1 - 2K + 1 = 2 - 2K > 0")
            st.latex(rf"\Rightarrow {sp.latex(sp.reduce_inequalities([P1_val_m1 > 0], K))}")

            st.latex(r"3)\; |a_0| < a_2")
            st.latex(rf"|a_0| < a_2 \Rightarrow {sp.latex(sp.Abs(a0_p1))} < {sp.latex(a2_p1)}")
            st.latex(r"1 < 1 \Rightarrow \text{falla, por lo que no se cumple}")
            st.latex(rf"\text{{Resultado combinado: }} {sp.latex(final_p1)}")

            if final_p1 == False or str(final_p1) == 'False':
                st.error("P1(z) es inestable para todo K porque la condición |a0| < a2 no se cumple.")
            else:
                st.success(f"P1(z) cumple el criterio de Jury para: {sp.latex(final_p1)}")

        with st.container():
            st.markdown("### P2(z) = z^3 + 2z^2 - 3z + 1")
            coeffs_p2 = sp.Poly(P2_actividad, z).all_coeffs()
            a3_p2 = coeffs_p2[0]
            a0_p2 = coeffs_p2[3]
            P2_val_1 = sp.expand(P2_actividad.subs(z, 1))
            P2_val_m1 = sp.expand(P2_actividad.subs(z, -1))
            final_p2 = sp.reduce_inequalities([P2_val_1 > 0, P2_val_m1 > 0, sp.Abs(a0_p2) < a3_p2])

            st.latex(r"P_2(z) = z^3 + 2z^2 - 3z + 1")
            st.latex(f"P_2(z) = {sp.latex(P2_actividad)}")
            st.latex(r"\text{Para } P_2(z), \; a_3 = 1, \; a_2 = 2, \; a_1 = -3, \; a_0 = 1")

            st.latex(r"1)\; P_2(1) > 0")
            st.latex(f"P_2(1) = {sp.latex(P2_val_1)}")
            st.latex(r"P_2(1) = 1 + 2 - 3 + 1 = 1 > 0")
            st.latex(rf"\Rightarrow {sp.latex(sp.reduce_inequalities([P2_val_1 > 0]))}")

            st.latex(r"2)\; P_2(-1) > 0 \; (grado impar: alternancia de signos)")
            st.latex(f"P_2(-1) = {sp.latex(P2_val_m1)}")
            st.latex(r"P_2(-1) = -1 + 2 - (-3) + 1 = 5 > 0")
            st.latex(rf"\Rightarrow {sp.latex(sp.reduce_inequalities([P2_val_m1 > 0]))}")

            st.latex(r"3)\; |a_0| < a_3")
            st.latex(rf"|a_0| < a_3 \Rightarrow {sp.latex(sp.Abs(a0_p2))} < {sp.latex(a3_p2)}")
            st.latex(r"1 < 1 \Rightarrow \text{falla, por lo que no se cumple}")
            st.latex(rf"\text{{Resultado combinado: }} {sp.latex(final_p2)}")

            if final_p2 == False or str(final_p2) == 'False':
                st.error("P2(z) es inestable porque la condición |a0| < an no se cumple.")
            else:
                st.success(f"P2(z) cumple el criterio de Jury: {sp.latex(final_p2)}")

        st.subheader("Segunda parte de la actividad: Criterio de Routh-Hurwitz")

        with st.container():
            st.markdown("### P3(z) = z^2 - 3z + b")
            transformation = (s + 1) / (s - 1)
            P3_sub = sp.expand(sp.simplify(P3_actividad.subs(z, transformation)))
            Q3 = sp.expand(sp.simplify(P3_sub * (s - 1)**2))
            Q3_coeffs = sp.Poly(Q3, s).all_coeffs()
            Q3_a2, Q3_a1, Q3_a0 = Q3_coeffs
            cond_b = sp.reduce_inequalities([Q3_a2 > 0, Q3_a1 > 0, Q3_a0 > 0], b)

            st.latex(r"z = \frac{s+1}{s-1}")
            st.latex(r"Q_3(s) = (s-1)^2 P_3\left(\frac{s+1}{s-1}\right)")
            st.latex(rf"P_3\left(\frac{s+1}{s-1}\right) = {sp.latex(P3_sub)}")
            st.latex(rf"Q_3(s) = {sp.latex(Q3)}")
            st.latex(r"Q_3(s) = (b-2)s^2 + (2-2b)s + (b+4)")
            st.latex(r"\text{Condición de Routh-Hurwitz: } a_2>0,\ a_1>0,\ a_0>0")
            st.latex(f"a_2 = {sp.latex(Q3_a2)}")
            st.latex(f"a_1 = {sp.latex(Q3_a1)}")
            st.latex(f"a_0 = {sp.latex(Q3_a0)}")
            st.latex(rf"\Rightarrow {sp.latex(cond_b)}")

            if cond_b == False or str(cond_b) == 'False':
                st.error("P3(z) es inestable: no existe un rango real de b que haga positivos todos los coeficientes.")
            else:
                st.success(f"P3(z) cumple la condición de Routh-Hurwitz para: {sp.latex(cond_b)}")

        with st.container():
            st.markdown("### P4(z) = z^2 + (K - 0.2)z + K")
            transformation = (s + 1) / (s - 1)
            P4_sub = sp.expand(sp.simplify(P4_actividad.subs(z, transformation)))
            Q4 = sp.expand(sp.simplify(P4_sub * (s - 1)**2))
            Q4_coeffs = sp.Poly(Q4, s).all_coeffs()
            Q4_a2, Q4_a1, Q4_a0 = Q4_coeffs
            cond_K = sp.reduce_inequalities([Q4_a2 > 0, Q4_a1 > 0, Q4_a0 > 0], K)

            st.latex(r"Q_4(s) = (s-1)^2 P_4\left(\frac{s+1}{s-1}\right)")
            st.latex(rf"P_4\left(\frac{s+1}{s-1}\right) = {sp.latex(P4_sub)}")
            st.latex(rf"Q_4(s) = {sp.latex(Q4)}")
            st.latex(r"Q_4(s) = \left(2K + \frac{4}{5}\right)s^2 + (2 - 2K)s + \frac{6}{5}")
            st.latex(r"\text{Condición de Routh-Hurwitz: } a_2>0,\ a_1>0,\ a_0>0")
            st.latex(f"a_2 = {sp.latex(Q4_a2)}")
            st.latex(f"a_1 = {sp.latex(Q4_a1)}")
            st.latex(f"a_0 = {sp.latex(Q4_a0)}")
            st.latex(rf"\Rightarrow {sp.latex(cond_K)}")

            if cond_K == False or str(cond_K) == 'False':
                st.error("P4(z) es inestable: no existe rango real de K que cumpla Routh-Hurwitz.")
            else:
                st.markdown("### Rango estable de K")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.latex(r"-\frac{2}{5} < K < 1")
                st.caption("Rango final: -2/5 < K < 1")

with simulation_tab:
    with st.container(border=True):
        st.subheader("Simulación de Respuesta")

        K_slider = st.slider(
            "Ganancia K",
            min_value=-1.0,
            max_value=4.0,
            value=1.5,
            step=0.1,
            help="Ajusta la ganancia del lazo para observar cómo cambia la estabilidad y la respuesta al escalón.",
        )
        st.caption("Este ajuste solo afecta la simulación de esta sección y permite relacionar la ganancia con la localización de los polos.")

        st.latex(r"T(z) = \frac{Kz}{z^2 + (K - 1.5)z + 0.5}")

        num_T = [K_slider, 0]
        den_T = [1.0, K_slider - 1.5, 0.5]
        system = signal.dlti(num_T, den_T)
        t, y = signal.dstep(system, n=40)
        t = np.asarray(t).ravel()
        y = np.asarray(y).squeeze()

        if 0 < K_slider < 3:
            st.success("Sistema estable: 0 < K < 3")
        else:
            st.error("Sistema inestable para esta ganancia K.")

        poles = np.roots(den_T)
        max_abs_pole = np.max(np.abs(poles))

        def format_pole(pole: complex) -> str:
            real_part = pole.real
            imag_part = pole.imag

            if abs(imag_part) < 1e-9:
                return f"{real_part:.4f}"
            if abs(real_part) < 1e-9:
                return f"{abs(imag_part):.4f}j" if imag_part > 0 else f"-{abs(imag_part):.4f}j"
            return f"{real_part:.4f}{imag_part:+.4f}j"

        left_col, right_col = st.columns([3, 1])

        with left_col:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.step(t, y, where='post', color='tab:blue', linewidth=2)
            ax.set_title('Respuesta al escalón del sistema en lazo cerrado')
            ax.set_xlabel('Muestra n')
            ax.set_ylabel('Salida y[n]')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        with right_col:
            st.markdown("### Parámetros Objetivos")
            st.metric("Ganancia K", f"{K_slider:.2f}")
            st.markdown("**Polos del sistema:**")
            for idx, pole in enumerate(poles, start=1):
                st.write(f"p{idx} = {format_pole(pole)}")
            st.metric("max |z|", f"{max_abs_pole:.4f}")

with tab4:
    with st.container(border=True):
        st.markdown("### Ejemplo práctico: control de altura de un dron")
        st.markdown(
            """
            En este caso, la planta $G(z)$ representa la física del dron: masa, aerodinámica, retrasos y respuesta del sistema al impulsar los rotores.
            El controlador $G_c(z)$ es el algoritmo que observa el error entre la altura deseada y la altura real, y acumula esa diferencia para corregirla.
            La ganancia $K$ representa la agresividad del control: cuánto se fuerza la acción de corrección sobre los motores.
            """
        )

        drone_k = st.slider("Ganancia K del dron", min_value=0.1, max_value=4.0, value=1.5, step=0.1)

        num_dron = [drone_k, 0]
        den_dron = [1.0, drone_k - 1.5, 0.5]
        drone_system = signal.dlti(num_dron, den_dron)
        t_dron, y_dron = signal.dstep(drone_system, n=60)
        t_dron = np.asarray(t_dron).ravel()
        y_dron = np.asarray(y_dron).squeeze() * 10

        col1, col2 = st.columns([3, 1])

        with col1:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(t_dron, y_dron, color='tab:blue', linewidth=2, label='Altura real')
            ax.axhline(10, color='green', linestyle='--', linewidth=1.5, label='Altura objetivo = 10 m')
            ax.set_title('Respuesta de altura del dron')
            ax.set_xlabel('Tiempo')
            ax.set_ylabel('Altura (metros)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

        with col2:
            if drone_k < 1.0:
                st.warning("El dron sube muy lento: la compensación es débil y la altura tarda demasiado en alcanzar la referencia.")
            elif 1.0 <= drone_k < 3.0:
                st.success("El dron alcanzó la altura de forma eficiente: la respuesta es rápida y estable, con un seguimiento apropiado de la referencia.")
            else:
                st.error("¡Peligro! El dron entró en oscilación incontrolable: la ganancia es demasiado alta y la respuesta se vuelve inestable.")

            st.markdown(
                "**Interpretación física resumida:**\n"
                "- $G(z)$ = la física del dron\n"
                "- $G_c(z)$ = el algoritmo de corrección\n"
                "- $K$ = la agresividad de los motores"
            )

