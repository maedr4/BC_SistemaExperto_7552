# -*- coding: utf-8 -*-
"""
MOTOR DE INFERENCIA (encadenamiento hacia adelante)
===================================================

El motor implementa explícitamente las tres fases del ciclo de inferencia
de un sistema experto basado en reglas:

  Fase 1 — EQUIPARACIÓN (matching):
      Se comparan las condiciones de cada regla contra la base de hechos
      activa. Las reglas cuyas condiciones se satisfacen (todas, son AND)
      forman el conjunto de reglas activadas (la agenda).

  Fase 2 — RESOLUCIÓN DE CONFLICTOS:
      Cuando varias reglas están activadas a la vez, se decide cuál se
      aplica primero. Estrategia: mayor PRIORIDAD primero; en empate gana
      la regla más ESPECÍFICA (más condiciones); si persiste el empate,
      se respeta el orden por identificador (R01 < R02 < ...).

  Fase 3 — EJECUCIÓN:
      Se ejecuta la regla ganadora: sus conclusiones se agregan a la base
      de hechos. Luego el ciclo vuelve a la Fase 1 (encadenamiento hacia
      adelante) hasta que ninguna regla agrega hechos nuevos (punto fijo).

Cada ciclo deja traza registrada para que la interfaz pueda mostrar el
razonamiento completo del motor.
"""

from base_conocimiento import REGLAS

FASE_EQUIPARACION = "equiparacion"
FASE_CONFLICTOS = "resolucion_conflictos"
FASE_EJECUCION = "ejecucion"


class MotorInferencia:
    def __init__(self, reglas=None):
        self.reglas = REGLAS if reglas is None else reglas
        self.traza = []

    # -- Fase 1: equiparación ------------------------------------------------
    def _condicion_se_cumple(self, condicion, hechos):
        clave, valor = condicion
        if valor == "*":  # cualquier valor no vacío para esa clave
            return any(c == clave and v for c, v in hechos)
        return (clave, valor) in hechos

    def equiparacion(self, hechos):
        """Fase 1: devuelve las reglas cuyas condiciones se cumplen."""
        activadas = [
            regla for regla in self.reglas
            if all(self._condicion_se_cumple(c, hechos) for c in regla["si"])
        ]
        self.traza.append({
            "fase": FASE_EQUIPARACION,
            "detalle": [r["id"] for r in activadas],
            "texto": "Reglas activadas: " + (", ".join(r["id"] for r in activadas) or "ninguna"),
        })
        return activadas

    # -- Fase 2: resolución de conflictos ------------------------------------
    def resolucion_conflictos(self, activadas):
        """Fase 2: ordena la agenda por prioridad, especificidad e id."""
        ordenadas = sorted(
            activadas,
            key=lambda r: (-r["prioridad"], -len(r["si"]), r["id"]),
        )
        self.traza.append({
            "fase": FASE_CONFLICTOS,
            "detalle": [r["id"] for r in ordenadas],
            "texto": "Agenda resuelta (orden de aplicación): "
                     + (", ".join(r["id"] for r in ordenadas) or "vacía"),
        })
        return ordenadas

    # -- Fase 3: ejecución ---------------------------------------------------
    def ejecutar(self, regla, hechos):
        """Fase 3: agrega las conclusiones de la regla a la base de hechos.

        Devuelve los hechos nuevos agregados (vacío si no aporta nada).
        """
        nuevos = []
        for conclusion in regla["entonces"]:
            clave, valor = conclusion
            # Restricción del dominio: un solo género recomendado; si ya hay uno
            # (fijado por una regla de mayor prioridad), esta regla no lo cambia.
            if clave == "genero_recomendado" and any(c == "genero_recomendado" for c, _ in hechos):
                continue
            if conclusion not in hechos:
                hechos.add(conclusion)
                nuevos.append(conclusion)
        self.traza.append({
            "fase": FASE_EJECUCION,
            "detalle": [regla["id"]],
            "texto": f'{regla["id"]} ejecutada -> ' + (", ".join(f"{k}={v}" for k, v in nuevos) or "sin hechos nuevos"),
        })
        return nuevos

    # -- Ciclo completo ------------------------------------------------------
    def inferir(self, hechos_iniciales):
        """Ejecuta el encadenamiento hacia adelante sobre los hechos dados.

        Devuelve un dict con las conclusiones derivadas, las reglas disparadas
        y la traza completa de las tres fases por ciclo.
        """
        self.traza = []
        hechos = set(hechos_iniciales)
        disparadas = []
        while True:
            activadas = self.equiparacion(hechos)
            pendientes = [r for r in activadas if r["id"] not in {d["id"] for d in disparadas}]
            ordenadas = self.resolucion_conflictos(pendientes)
            progreso = False
            for regla in ordenadas:  # se ejecuta la primera que aporte hechos nuevos
                if self.ejecutar(regla, hechos):
                    disparadas.append(regla)
                    progreso = True
                    break
            if not progreso:
                break

        conclusiones = sorted(v for k, v in hechos if k == "genero_recomendado")
        return {
            "conclusiones": conclusiones,
            "formatos": sorted(v for k, v in hechos if k == "formato_recomendado"),
            "reglas_disparadas": disparadas,
            "hechos_finales": hechos,
            "traza": self.traza,
        }


def hechos_desde_respuestas(respuestas):
    """Convierte las respuestas de la interfaz (dict) en hechos (tuplas).

    - radio/texto: {"clave": "valor"}
    - check:       {"clave": ["valor1", "valor2"]}
    - texto vacío se ignora.
    """
    hechos = set()
    for clave, valor in respuestas.items():
        if isinstance(valor, (list, tuple, set)):
            for v in valor:
                hechos.add((clave, v))
        elif valor not in (None, ""):
            hechos.add((clave, valor))
    return hechos
