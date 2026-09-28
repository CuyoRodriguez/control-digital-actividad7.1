import numpy as np
import matplotlib.pyplot as plt

# Datos del problema
n = np.arange(0, 40, dtype=int)
x = (0.5) ** n

y_iter = np.zeros_like(n, dtype=float)
y_prev = 0.0
x_prev = 0.0

for k in range(len(n)):
    y_iter[k] = y_prev + x[k] + 0.5 * x_prev
    y_prev = y_iter[k]
    x_prev = x[k]

# Solución analítica
y_analitica = 3 - 2 * (0.5 ** n)

# Figura principal
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Inciso a) - gráfica iterativa
ax = axes[0, 0]
ax.stem(n, y_iter, basefmt=' ', linefmt='C0-', markerfmt='C0o')
ax.set_title('Inciso a) Gráfica de y[n] Iterativa (Primeros 40 puntos)', fontsize=12)
ax.set_xlabel('n')
ax.set_ylabel('y[n]')
ax.grid(True, linestyle='--', alpha=0.7)

# Inciso b) - función de transferencia
ax = axes[0, 1]
ax.set_axis_off()
texto_b = (
    "Inciso b) Función de Transferencia H(z)\n\n"
    "Y(z) = z⁻¹Y(z) + X(z) + 0.5 z⁻¹X(z)\n"
    "=> Y(z) - z⁻¹Y(z) = X(z) + 0.5 z⁻¹X(z)\n"
    "=> Y(z)(1 - z⁻¹) = X(z)(1 + 0.5 z⁻¹)\n"
    "=> H(z) = Y(z)/X(z) = (1 + 0.5 z⁻¹)/(1 - z⁻¹)\n"
    "=> H(z) = (1 + 0.5 z⁻¹)/(1 - z⁻¹) · (z/z) = (z + 0.5)/(z - 1)"
)
ax.text(
    0.5, 0.5, texto_b,
    ha='center', va='center', fontsize=12.5, linespacing=1.7,
    bbox=dict(boxstyle='round,pad=1.1', facecolor='whitesmoke', edgecolor='gray', alpha=0.95)
)

# Inciso c) - comparación iterativa vs analítica
ax = axes[1, 0]
ax.stem(n, y_iter, basefmt=' ', linefmt='C0-', markerfmt='C0o', label='Iterativa')
ax.plot(n, y_analitica, '--r', linewidth=2, label='Analítica')
ax.set_title('Inciso c) Comparación: Solución Analítica vs Iterativa', fontsize=12)
ax.set_xlabel('n')
ax.set_ylabel('y[n]')
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='upper left')

# Inciso d) - teorema del valor final
ax = axes[1, 1]
ax.set_axis_off()
texto_d = (
    "Inciso d) Teorema del Valor Final\n\n"
    "lim (n -> ∞) y[n] = lim (z -> 1) (z - 1) Y(z)\n"
    "Y(z) = z(z + 0.5) / [(z - 1)(z - 0.5)]\n"
    "lim (z -> 1) [ z(z + 0.5) / (z - 0.5) ] = (1 · 1.5) / 0.5 = 3\n"
    "\n"
    "Conclusión: Sí, la salida se estabiliza en 3."
)
ax.text(
    0.5, 0.5, texto_d,
    ha='center', va='center', fontsize=12.5, linespacing=1.7,
    bbox=dict(boxstyle='round,pad=1.1', facecolor='whitesmoke', edgecolor='gray', alpha=0.95)
)

plt.tight_layout()
plt.savefig('control_discreto_incisos.png', dpi=200, bbox_inches='tight')
plt.show()
