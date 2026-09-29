# -*- coding: utf-8 -*-
"""
BASE DE CONOCIMIENTO del Sistema Experto de Recomendación de Películas
=====================================================================

Contiene los dos componentes clásicos de un sistema experto basado en reglas:

1. HECHOS (base de hechos): 11 hechos que el usuario introduce por la interfaz
   gráfica. Cada hecho se describe con su identificador, enunciado, tipo de
   control gráfico y valores posibles.

2. REGLAS (base de reglas): 14 reglas "SI <condiciones> ENTONCES <conclusiones>"
   con prioridad y explicación en lenguaje natural. Las condiciones se evalúan
   por AND (todas deben cumplirse). Los hechos de tipo checkbox generan varios
   hechos (uno por casilla marcada), por lo que una condición puede apuntar a
   un valor concreto dentro de un hecho multivaluado.

Los hechos se representan como tuplas (clave, valor) y la base de hechos
activa es un conjunto de esas tuplas.
"""

# ---------------------------------------------------------------------------
# 1. HECHOS (mínimo requerido: 8) — se muestran como controles en la interfaz
# ---------------------------------------------------------------------------
# tipo: "radio" (selección única), "check" (selección múltiple), "texto"
HECHOS = [
    {
        "clave": "estado_animo",
        "enunciado": "¿Cuál es tu estado de ánimo hoy?",
        "tipo": "radio",
        "opciones": [
            ("triste", "Triste / melancólico"),
            ("estresado", "Estresado"),
            ("alegre", "Alegre / animado"),
            ("aburrido", "Aburrido"),
            ("nostalgico", "Nostálgico"),
            ("reflexivo", "Reflexivo"),
        ],
    },
    {
        "clave": "tiempo_disponible",
        "enunciado": "¿Cuánto tiempo dispones?",
        "tipo": "radio",
        "opciones": [
            ("corto", "Menos de 90 minutos"),
            ("medio", "Entre 90 y 120 minutos"),
            ("largo", "Más de 2 horas (o maratón)"),
        ],
    },
    {
        "clave": "compania",
        "enunciado": "¿Con quién verás la película?",
        "tipo": "radio",
        "opciones": [
            ("solo", "A solas"),
            ("pareja", "Con mi pareja"),
            ("familia", "En familia"),
            ("amigos", "Con amigos"),
        ],
    },
    {
        "clave": "hay_ninos",
        "enunciado": "¿Hay niños presentes?",
        "tipo": "radio",
        "opciones": [("si", "Sí"), ("no", "No")],
    },
    {
        "clave": "tolerancia_violencia",
        "enunciado": "¿Cuál es tu tolerancia a la violencia en pantalla?",
        "tipo": "radio",
        "opciones": [("baja", "Baja"), ("media", "Media"), ("alta", "Alta")],
    },
    {
        "clave": "terror_gusto",
        "enunciado": "¿Te gusta el terror?",
        "tipo": "radio",
        "opciones": [("si", "Sí"), ("no", "No")],
    },
    {
        "clave": "humor_gusto",
        "enunciado": "¿Te gusta el humor?",
        "tipo": "radio",
        "opciones": [("si", "Sí"), ("no", "No")],
    },
    {
        "clave": "ritmo_preferido",
        "enunciado": "¿Qué ritmo prefieres?",
        "tipo": "radio",
        "opciones": [
            ("rapido", "Rápido / trepidante"),
            ("lento", "Lento / contemplativo"),
            ("indiferente", "Me es indiferente"),
        ],
    },
    {
        "clave": "epoca_preferida",
        "enunciado": "¿De qué época prefieres la película?",
        "tipo": "radio",
        "opciones": [
            ("clasico", "Clásica (antes del 2000)"),
            ("reciente", "Reciente (2000 en adelante)"),
            ("indiferente", "Me es indiferente"),
        ],
    },
    {
        "clave": "contenido_a_evitar",
        "enunciado": "Marca el contenido que quieres evitar",
        "tipo": "check",
        "opciones": [
            ("sangre", "Sangre / gore"),
            ("lenguaje_soez", "Lenguaje soez"),
            ("sustos", "Sustos / terror psicológico"),
        ],
    },
    {
        "clave": "pelicula_favorita",
        "enunciado": "Menciona una película que te haya gustado (opcional)",
        "tipo": "texto",
    },
]

# ---------------------------------------------------------------------------
# 2. REGLAS (mínimo requerido: 6) — SI condiciones ENTONCES conclusiones
#    prioridad: número entero; en empate de activación gana el mayor.
#    especificidad (nº de condiciones) desempata después de la prioridad.
# ---------------------------------------------------------------------------
REGLAS = [
    {
        "id": "R01",
        "si": [("hay_ninos", "si")],
        "entonces": [("genero_recomendado", "animada")],
        "prioridad": 5,
        "explicacion": "Si hay niños presentes, una película animada es la opción apta para todo el público.",
    },
    {
        "id": "R02",
        "si": [("estado_animo", "triste"), ("humor_gusto", "si")],
        "entonces": [("genero_recomendado", "comedia")],
        "prioridad": 3,
        "explicacion": "El humor es un excelente ánimo elevador: una comedia ayuda a mejorar el ánimo.",
    },
    {
        "id": "R03",
        "si": [("estado_animo", "estresado"), ("tolerancia_violencia", "baja")],
        "entonces": [("genero_recomendado", "animada")],
        "prioridad": 2,
        "explicacion": "Con estrés y baja tolerancia a la violencia, una película animada relaja sin sobrecargar.",
    },
    {
        "id": "R04",
        "si": [("estado_animo", "aburrido"), ("ritmo_preferido", "rapido")],
        "entonces": [("genero_recomendado", "accion")],
        "prioridad": 2,
        "explicacion": "Ante el aburrimiento y ganas de ritmo rápido, una película de acción mantiene la atención.",
    },
    {
        "id": "R05",
        "si": [("estado_animo", "aburrido"), ("ritmo_preferido", "lento")],
        "entonces": [("genero_recomendado", "thriller")],
        "prioridad": 2,
        "explicacion": "Un thriller de ritmo pausado engancha sin exigir acción constante.",
    },
    {
        "id": "R06",
        "si": [("terror_gusto", "si"), ("tolerancia_violencia", "alta"), ("hay_ninos", "no")],
        "entonces": [("genero_recomendado", "terror")],
        "prioridad": 4,
        "explicacion": "Con gusto por el terror, alta tolerancia a la violencia y sin niños, el terror es apto.",
    },
    {
        "id": "R07",
        "si": [("terror_gusto", "si"), ("contenido_a_evitar", "sustos")],
        "entonces": [("genero_recomendado", "thriller")],
        "prioridad": 6,
        "explicacion": "Si te gusta el terror pero evitas los sustos, el thriller psicológico conserva la intriga sin sobresaltos.",
    },
    {
        "id": "R08",
        "si": [("compania", "pareja"), ("estado_animo", "alegre")],
        "entonces": [("genero_recomendado", "romance")],
        "prioridad": 3,
        "explicacion": "Una velada alegre en pareja se disfruta bien con una comedia romántica o romance.",
    },
    {
        "id": "R09",
        "si": [("estado_animo", "reflexivo"), ("ritmo_preferido", "lento")],
        "entonces": [("genero_recomendado", "documental")],
        "prioridad": 3,
        "explicacion": "El ánimo reflexivo y el ritmo lento encajan con un documental que invite a pensar.",
    },
    {
        "id": "R10",
        "si": [("estado_animo", "nostalgico"), ("epoca_preferida", "clasico")],
        "entonces": [("genero_recomendado", "drama")],
        "prioridad": 3,
        "explicacion": "La nostalgia y el gusto por lo clásico se combinan bien con un drama de época.",
    },
    {
        "id": "R11",
        "si": [("compania", "amigos"), ("humor_gusto", "si")],
        "entonces": [("genero_recomendado", "comedia")],
        "prioridad": 2,
        "explicacion": "Entre amigos y con gusto por el humor, una comedia garantiza una buena velada.",
    },
    {
        "id": "R12",
        "si": [("estado_animo", "alegre"), ("ritmo_preferido", "rapido")],
        "entonces": [("genero_recomendado", "accion")],
        "prioridad": 2,
        "explicacion": "Un ánimo alegre con ganas de ritmo rápido pide una película de acción trepidante.",
    },
    {
        "id": "R13",
        "si": [("tiempo_disponible", "corto")],
        "entonces": [("formato_recomendado", "cortometraje")],
        "prioridad": 1,
        "explicacion": "Con menos de 90 minutos, un cortometraje o película corta evita dejar la historia a medias.",
    },
    {
        "id": "R14",
        "si": [("pelicula_favorita", "*")],
        "entonces": [("perfil_gusto", "con_gustos_definidos")],
        "prioridad": 1,
        "explicacion": "Se registró una película favorita: el perfil del usuario ya tiene gustos definidos.",
    },
]

# Catálogo de apoyo para mostrar sugerencias concretas por género
PELICULAS_SUGERIDAS = {
    "animada": "Up (2009), Ratatouille (2007), El viaje de Chihiro (2001)",
    "comedia": "La gran aventura de LEGO (2014), Superbad (2007), El Gran Hotel Budapest (2014)",
    "accion": "Mad Max: Furia en el camino (2015), John Wick (2014), Los Vengadores (2012)",
    "thriller": "El origen (2010), La isla siniestra (2010), Zodiac (2007)",
    "terror": "El Conjuro (2013), Hereditary (2018), Un lugar en silencio (2018)",
    "romance": "Antes del amanecer (1995), La La Land (2016), Orgullo y prejuicio (2005)",
    "documental": "Free Solo (2018), El dilema de las redes (2020), Cosmos (1980)",
    "drama": "El club de la lucha (1999), Forrest Gump (1994), El pianista (2002)",
}

# Nombres legibles de los géneros para la interfaz
NOMBRES_GENERO = {
    "animada": "Animada",
    "comedia": "Comedia",
    "accion": "Acción",
    "thriller": "Thriller / suspenso",
    "terror": "Terror",
    "romance": "Romance",
    "documental": "Documental",
    "drama": "Drama",
}
