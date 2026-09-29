# -*- coding: utf-8 -*-
"""Auto-verificación del motor de inferencia (sin frameworks).

Ejecutar:  py test_motor.py
Falla con AssertionError si la lógica de reglas o de las tres fases se rompe.
"""

from motor import MotorInferencia, hechos_desde_respuestas


def escenario(**respuestas):
    motor = MotorInferencia()
    return motor.inferir(hechos_desde_respuestas(respuestas))


# 1) R01 (prioridad 5) debe ganar sobre R03 (prioridad 2): hay niños -> animada
r = escenario(hay_ninos="si", estado_animo="estresado", tolerancia_violencia="baja")
assert "animada" in r["conclusiones"], r["conclusiones"]
assert r["reglas_disparadas"][0]["id"] == "R01", "la resolución de conflictos no respetó la prioridad"

# 2) Triste + humor -> comedia (R02)
r = escenario(estado_animo="triste", humor_gusto="si")
assert "comedia" in r["conclusiones"]

# 3) Terror + violencia alta + sin niños -> terror (R06)
r = escenario(terror_gusto="si", tolerancia_violencia="alta", hay_ninos="no")
assert "terror" in r["conclusiones"]

# 4) R07 (prioridad 6) supera a R06 (prioridad 4): evita sustos -> thriller
r = escenario(terror_gusto="si", tolerancia_violencia="alta", hay_ninos="no",
              contenido_a_evitar=["sustos"])
assert "thriller" in r["conclusiones"] and "terror" not in r["conclusiones"]

# 5) Tiempo corto agrega formato; texto vacío no dispara R14
r = escenario(tiempo_disponible="corto", pelicula_favorita="")
assert r["formatos"] == ["cortometraje"]
assert not any(regla["id"] == "R14" for regla in r["reglas_disparadas"])

# 6) El ciclo de inferencia deja las tres fases en la traza
fases = {paso["fase"] for paso in r["traza"]}
assert fases == {"equiparacion", "resolucion_conflictos", "ejecucion"}, fases

print("OK: 6 verificaciones del motor pasaron.")
