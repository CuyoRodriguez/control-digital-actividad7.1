import numbers

import numpy as np


def calcular_senal_continua(
	tiempo: np.ndarray,
	valor_inicial: float = 1.0,
	amplitud_pico: float = 2.0,
	tasa_descenso: float = 0.5,
) -> np.ndarray:
	"""Devuelve una curva suave con un único pico y decaimiento progresivo.

	Se utiliza la forma sugerida por el enunciado:
	e(t) = 1.0 + 2.0 * t * exp(-0.5 * t)
	"""
	return valor_inicial + amplitud_pico * tiempo * np.exp(-tasa_descenso * tiempo)


def calcular_instantes_muestreo(
	periodo_muestreo: float,
	tiempo_inicial: float,
	tiempo_final: float,
) -> np.ndarray:
	"""Devuelve los instantes t_k = kT contenidos en un intervalo temporal."""
	valores = (periodo_muestreo, tiempo_inicial, tiempo_final)
	if any(isinstance(valor, bool) or not isinstance(valor, numbers.Real) for valor in valores):
		raise TypeError("T, tiempo_inicial y tiempo_final deben ser números reales")

	periodo_muestreo = float(periodo_muestreo)
	tiempo_inicial = float(tiempo_inicial)
	tiempo_final = float(tiempo_final)

	if not np.isfinite(periodo_muestreo) or periodo_muestreo <= 0:
		raise ValueError("El período de muestreo T debe ser positivo y finito")
	if not np.isfinite(tiempo_inicial) or not np.isfinite(tiempo_final):
		raise ValueError("Los límites de tiempo deben ser finitos")
	if tiempo_inicial > tiempo_final:
		raise ValueError("El tiempo inicial no puede ser mayor que el tiempo final")

	indice_inicial = int(np.ceil(tiempo_inicial / periodo_muestreo))
	indice_final = int(np.floor(tiempo_final / periodo_muestreo))
	if indice_inicial > indice_final:
		return np.array([], dtype=float)

	indices = np.arange(indice_inicial, indice_final + 1)
	return indices * periodo_muestreo


def calcular_senal_discreta(
	periodo_muestreo: float,
	tiempo_inicial: float,
	tiempo_final: float,
	valor_inicial: float = 1.0,
	amplitud_pico: float = 2.0,
	tasa_descenso: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
	"""Evalúa la misma ecuación e(t) en los instantes discretos t_k = kT."""
	instantes = calcular_instantes_muestreo(
		periodo_muestreo,
		tiempo_inicial,
		tiempo_final,
	)
	valores = calcular_senal_continua(
		instantes,
		valor_inicial=valor_inicial,
		amplitud_pico=amplitud_pico,
		tasa_descenso=tasa_descenso,
	)
	return instantes, valores


def calcular_valores_muestreados(
	periodo_muestreo: float,
	tiempo_inicial: float,
	tiempo_final: float,
) -> tuple[np.ndarray, np.ndarray]:
	"""Compatibilidad: devuelve los instantes de muestreo y los valores correspondientes e(kT)."""
	return calcular_senal_discreta(
		periodo_muestreo,
		tiempo_inicial,
		tiempo_final,
	)
