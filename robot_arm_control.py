import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import control as ct

# Sistema discreto:
# y[k] - 1.2 y[k-1] + 0.32 y[k-2] = 0.12 x[k-1]
# H(z) = 0.12 z^-1 / (1 - 1.2 z^-1 + 0.32 z^-2)
num = [0.12]
den = [1, -1.2, 0.32]

sys = ct.TransferFunction(num, den, dt=1)
zeros = sys.zeros()
poles = sys.poles()
stable = np.all(np.abs(poles) < 1)

print('Ceros del sistema:')
print(zeros)
print('\nPolos del sistema:')
print(poles)

if stable:
    print('\nSistema estable: los polos estan dentro del circulo unitario.')
else:
    print('\nSistema inestable: al menos un polo esta fuera del circulo unitario.')

k = np.arange(0, 21, 1)
t, y = ct.step_response(sys, T=k)

print('\nValores numericos de la salida y[k]:')
for i, yi in enumerate(y):
    print(f'k = {i:2d}  ->  y[{i}] = {yi:.6f}')

plt.figure(figsize=(10, 6))
plt.stem(t, y, basefmt=' ', linefmt='C0-', markerfmt='C0o', label='Respuesta al escalon')
plt.plot(t, y, '--', color='gray', linewidth=1.5, alpha=0.7, label='Interpolacion')
plt.title('Respuesta al escalon unitario del brazo robotico', fontsize=14, fontweight='bold')
plt.xlabel('Instante de muestreo k', fontsize=12)
plt.ylabel('Salida y[k]', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('robot_arm_response.png', dpi=150)
print('\nGrafica guardada en robot_arm_response.png')
