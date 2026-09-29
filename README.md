# Sistema Experto de Recomendación de Películas

Sistema experto basado en reglas (encadenamiento hacia adelante) con interfaz
gráfica de escritorio en Tkinter. El usuario responde sobre su estado de ánimo,
tiempo, compañía y preferencias; el motor activa reglas y recomienda géneros de
cine con sugerencias concretas y explicación del razonamiento.

## Cómo ejecutar

```powershell
py main.py
```

Requisitos: Python 3.x con Tkinter (incluido en la instalación estándar de Windows).
No usa librerías externas.

Verificación del motor (sin interfaz):

```powershell
py test_motor.py
```

## Estructura

| Archivo | Contenido |
|---|---|
| `base_conocimiento.py` | Base de conocimiento: 11 hechos y 14 reglas documentadas |
| `motor.py` | Motor de inferencia con las tres fases del ciclo de inferencia |
| `interfaz.py` | Interfaz gráfica Tkinter (paleta estilo OpenCode/Claude) |
| `main.py` | Punto de entrada |
| `test_motor.py` | Auto-verificación del motor (asserts) |
| `GUION_VIDEO.md` | Guion para el video explicativo |

## Base de conocimiento

### Hechos (11) — se ingresan por controles gráficos

| # | Hecho (clave) | Control | Valores |
|---|---|---|---|
| 1 | `estado_animo` | radio buttons | triste, estresado, alegre, aburrido, nostalgico, reflexivo |
| 2 | `tiempo_disponible` | radio buttons | corto, medio, largo |
| 3 | `compania` | radio buttons | solo, pareja, familia, amigos |
| 4 | `hay_ninos` | radio buttons | si, no |
| 5 | `tolerancia_violencia` | radio buttons | baja, media, alta |
| 6 | `terror_gusto` | radio buttons | si, no |
| 7 | `humor_gusto` | radio buttons | si, no |
| 8 | `ritmo_preferido` | radio buttons | rapido, lento, indiferente |
| 9 | `epoca_preferida` | radio buttons | clasico, reciente, indiferente |
| 10 | `contenido_a_evitar` | checkboxes | sangre, lenguaje_soez, sustos |
| 11 | `pelicula_favorita` | campo de texto | texto libre (opcional) |

### Reglas (14) — SI condiciones (AND) ENTONCES conclusiones

| Regla | Si | Entonces | Prioridad |
|---|---|---|---|
| R01 | hay_ninos = si | genero = animada | 5 |
| R02 | estado_animo = triste ∧ humor_gusto = si | genero = comedia | 3 |
| R03 | estado_animo = estresado ∧ tolerancia_violencia = baja | genero = animada | 2 |
| R04 | estado_animo = aburrido ∧ ritmo_preferido = rapido | genero = accion | 2 |
| R05 | estado_animo = aburrido ∧ ritmo_preferido = lento | genero = thriller | 2 |
| R06 | terror_gusto = si ∧ tolerancia_violencia = alta ∧ hay_ninos = no | genero = terror | 4 |
| R07 | terror_gusto = si ∧ contenido_a_evitar ∋ sustos | genero = thriller | 6 |
| R08 | compania = pareja ∧ estado_animo = alegre | genero = romance | 3 |
| R09 | estado_animo = reflexivo ∧ ritmo_preferido = lento | genero = documental | 3 |
| R10 | estado_animo = nostalgico ∧ epoca_preferida = clasico | genero = drama | 3 |
| R11 | compania = amigos ∧ humor_gusto = si | genero = comedia | 2 |
| R12 | estado_animo = alegre ∧ ritmo_preferido = rapido | genero = accion | 2 |
| R13 | tiempo_disponible = corto | formato = cortometraje | 1 |
| R14 | pelicula_favorita ≠ vacío | perfil_gusto = con_gustos_definidos | 1 |

La base completa con la explicación en lenguaje natural de cada regla está en
`base_conocimiento.py`.

## Motor de inferencia — las tres fases (`motor.py`)

1. **Equiparación**: compara las condiciones de cada regla con la base de hechos
   activa y produce la agenda de reglas activadas (`equiparacion`).
2. **Resolución de conflictos**: ordena la agenda por prioridad (mayor primero),
   desempatando por especificidad (número de condiciones) y luego por id
   (`resolucion_conflictos`).
3. **Ejecución**: aplica la regla ganadora agregando sus conclusiones a la base
   de hechos (`ejecutar`) y repite el ciclo (encadenamiento hacia adelante) hasta
   que ninguna regla aporta hechos nuevos. El género recomendado es exclusivo:
   la primera regla que lo fija (la de mayor prioridad) gana el conflicto y las
   reglas restantes quedan descartadas para esa conclusión.

Cada ciclo queda registrado en una traza que la interfaz muestra al usuario.

## Interfaz gráfica

Escritorio con Tkinter. Controles: radio buttons, checkboxes, campo de texto,
botones «Obtener recomendación» y «Limpiar». El panel derecho muestra la
conclusión (género y sugerencias), las reglas aplicadas con su explicación y la
traza completa de las tres fases. Paleta estilo OpenCode/Claude: fondo `#1F1E1D`,
paneles `#262524`, texto `#F5F4EF`, acento coral `#D97757`.
