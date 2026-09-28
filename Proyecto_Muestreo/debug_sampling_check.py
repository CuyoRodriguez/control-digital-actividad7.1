import numpy as np
from src.signals import calcular_senal_continua, calcular_senal_discreta

t = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
print('continuos', np.round(calcular_senal_continua(t), 6))
inst, vals = calcular_senal_discreta(1.0, 0, 5)
print('instantes', inst)
print('muestreo', np.round(vals, 6))
