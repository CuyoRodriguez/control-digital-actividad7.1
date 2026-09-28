import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

texto = (
    r"$T(z) = \frac{\frac{0.2z + 1}{z^2 + 0.3z + 0.5}}{1 + \frac{0.2z + 1}{z^2 + 0.3z + 0.5}}$"
    r"$\;$" "\n"
    r"$\Rightarrow T(z) = \frac{0.2z + 1}{(z^2 + 0.3z + 0.5) + (0.2z + 1)} = \frac{0.2z + 1}{z^2 + 0.5z + 1.5}$"
    r"$\;$" "\n"
    r"$\Rightarrow \frac{Y(z)}{X(z)} = \frac{0.2 z^{-1} + z^{-2}}{1 + 0.5 z^{-1} + 1.5 z^{-2}}$"
    r"$\;$" "\n"
    r"$Y(z)(1 + 0.5 z^{-1} + 1.5 z^{-2}) = X(z)(0.2 z^{-1} + z^{-2})$"
    r"$\;$" "\n"
    r"$\Rightarrow y[n] + 0.5 y[n-1] + 1.5 y[n-2] = 0.2 x[n-1] + x[n-2]$"
    r"$\;$" "\n"
    r"$\Rightarrow y[n] = -0.5 y[n-1] - 1.5 y[n-2] + 0.2 x[n-1] + x[n-2]$"
)

ax.text(
    0.5,
    0.5,
    texto,
    ha='center',
    va='center',
    fontsize=13,
    bbox=dict(boxstyle='round,pad=1.2', facecolor='white', edgecolor='0.75', linewidth=1.2),
    color='black',
)

plt.show()
