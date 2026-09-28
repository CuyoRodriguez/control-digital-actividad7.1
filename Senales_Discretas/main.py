import numpy as np
import matplotlib.pyplot as plt


# La frecuencia de la senal permanece fija para los tres casos.
FRECUENCIA = 6  # Hz

# Se usa el mismo conjunto de indices n para comparar los casos.
N = np.arange(0, 101)


def calcular_muestras(n, periodo_muestreo):
    """Calcula x[nT] = 5 cos(2 pi f n T)."""
    return 5 * np.cos(2 * np.pi * FRECUENCIA * n * periodo_muestreo)


def main():
    periodos_muestreo = [
        ("T1 = pi/200", np.pi / 200),
        ("T2 = pi/100", np.pi / 100),
        ("T3 = pi/50", np.pi / 50),
    ]

    figura, ejes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    figura.suptitle("Muestreo de x(t) = 5 cos(2 pi f t), con f = 6 Hz")

    for eje, (nombre_periodo, periodo_muestreo) in zip(ejes, periodos_muestreo):
        muestras = calcular_muestras(N, periodo_muestreo)

        eje.stem(N, muestras)
        eje.set_title(f"Senal discreta para {nombre_periodo}")
        eje.set_ylabel("x[nT]")
        eje.set_ylim(-5.5, 5.5)
        eje.grid(True, linestyle="--", alpha=0.6)
        eje.axhline(0, color="black", linewidth=0.8)

    ejes[-1].set_xlabel("Indice n")
    figura.tight_layout(rect=(0, 0, 1, 0.96))
    plt.show()


if __name__ == "__main__":
    main()
