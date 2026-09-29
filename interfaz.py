# -*- coding: utf-8 -*-
"""
INTERFAZ GRÁFICA (Tkinter) — estilo visual OpenCode / Claude.

Toda la interacción con el usuario ocurre por controles gráficos:
radio buttons, checkboxes, campo de texto y botones. El resultado y la
traza del motor de inferencia se muestran en pantalla, sin terminal.
"""

import tkinter as tk
from tkinter import ttk

from base_conocimiento import HECHOS, NOMBRES_GENERO, PELICULAS_SUGERIDAS
from motor import MotorInferencia, hechos_desde_respuestas

# Paleta estilo OpenCode / Claude (tema oscuro, acento coral)
FONDO = "#1F1E1D"
PANEL = "#262524"
TEXTO = "#F5F4EF"
TEXTO_SEC = "#B8B5AE"
ACENTO = "#D97757"
ACENTO_OSC = "#B85C42"
BORDE = "#3E3D3B"


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Experto · Recomendación de Películas")
        self.geometry("1100x720")
        self.configure(bg=FONDO)
        self._configurar_estilo()

        # ---- Encabezado ----
        encabezado = tk.Frame(self, bg=PANEL, pady=14, padx=20)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado, text="🎬  Sistema Experto de Recomendación de Películas",
            bg=PANEL, fg=TEXTO, font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text="Base de conocimiento basada en reglas · Motor de inferencia con "
                 "equiparación, resolución de conflictos y ejecución",
            bg=PANEL, fg=TEXTO_SEC, font=("Segoe UI", 9),
        ).pack(anchor="w")

        # ---- Cuerpo: formulario (izq) | resultados (der) ----
        cuerpo = tk.Frame(self, bg=FONDO)
        cuerpo.pack(fill="both", expand=True, padx=16, pady=12)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=2)
        cuerpo.rowconfigure(0, weight=1)

        self._construir_formulario(cuerpo)
        self._construir_panel_resultado(cuerpo)

        # ---- Botonera inferior ----
        barra = tk.Frame(self, bg=FONDO, pady=10)
        barra.pack(fill="x", padx=16)
        tk.Button(
            barra, text="Obtener recomendación", command=self.recomendar,
            bg=ACENTO, fg="#FFFFFF", activebackground=ACENTO_OSC,
            activeforeground="#FFFFFF", relief="flat", font=("Segoe UI", 11, "bold"),
            padx=18, pady=8, cursor="hand2",
        ).pack(side="left")
        tk.Button(
            barra, text="Limpiar", command=self.limpiar,
            bg=PANEL, fg=TEXTO, activebackground=BORDE, activeforeground=TEXTO,
            relief="flat", font=("Segoe UI", 11), padx=18, pady=8, cursor="hand2",
        ).pack(side="left", padx=10)

    # ------------------------------------------------------------------ UI
    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TCombobox", fieldbackground=PANEL, background=PANEL, foreground=TEXTO)

    def _construir_formulario(self, padre):
        contenedor = tk.Frame(padre, bg=FONDO)
        contenedor.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        lienzo = tk.Canvas(contenedor, bg=FONDO, highlightthickness=0)
        barra = ttk.Scrollbar(contenedor, orient="vertical", command=lienzo.yview)
        marco = tk.Frame(lienzo, bg=FONDO)
        marco.bind("<Configure>", lambda e: lienzo.configure(scrollregion=lienzo.bbox("all")))
        lienzo.create_window((0, 0), window=marco, anchor="nw")
        lienzo.configure(yscrollcommand=barra.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        lienzo.bind_all("<MouseWheel>", lambda e: lienzo.yview_scroll(-1 * (e.delta // 120), "units"))

        self.variables = {}
        for hecho in HECHOS:
            caja = tk.LabelFrame(
                marco, text=f"  {hecho['enunciado']}  ", bg=FONDO, fg=ACENTO,
                font=("Segoe UI", 10, "bold"), padx=10, pady=8,
                highlightbackground=BORDE, highlightthickness=1,
            )
            caja.pack(fill="x", pady=6, anchor="n")

            if hecho["tipo"] == "radio":
                var = tk.StringVar(value="")
                self.variables[hecho["clave"]] = var
                for valor, etiqueta in hecho["opciones"]:
                    tk.Radiobutton(
                        caja, text=etiqueta, variable=var, value=valor,
                        bg=FONDO, fg=TEXTO, selectcolor=PANEL, activebackground=FONDO,
                        activeforeground=TEXTO, anchor="w", font=("Segoe UI", 9),
                    ).pack(fill="x", anchor="w")

            elif hecho["tipo"] == "check":
                vars_check = {}
                self.variables[hecho["clave"]] = vars_check
                for valor, etiqueta in hecho["opciones"]:
                    var = tk.BooleanVar(value=False)
                    vars_check[valor] = var
                    tk.Checkbutton(
                        caja, text=etiqueta, variable=var,
                        bg=FONDO, fg=TEXTO, selectcolor=PANEL, activebackground=FONDO,
                        activeforeground=TEXTO, anchor="w", font=("Segoe UI", 9),
                    ).pack(fill="x", anchor="w")

            else:  # texto
                var = tk.StringVar(value="")
                self.variables[hecho["clave"]] = var
                tk.Entry(
                    caja, textvariable=var, bg=PANEL, fg=TEXTO, insertbackground=TEXTO,
                    relief="flat", font=("Segoe UI", 10),
                ).pack(fill="x", pady=2)

    def _construir_panel_resultado(self, padre):
        marco = tk.Frame(padre, bg=PANEL, padx=14, pady=12)
        marco.grid(row=0, column=1, sticky="nsew")
        tk.Label(
            marco, text="Conclusión y razonamiento", bg=PANEL, fg=ACENTO,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")
        self.salida = tk.Text(
            marco, wrap="word", bg=PANEL, fg=TEXTO, relief="flat",
            font=("Segoe UI", 10), padx=6, pady=6, state="disabled",
        )
        self.salida.pack(fill="both", expand=True, pady=(8, 0))
        self.salida.tag_configure("titulo", foreground=ACENTO, font=("Segoe UI", 11, "bold"))
        self.salida.tag_configure("destacado", foreground="#FFFFFF", font=("Segoe UI", 12, "bold"))
        self.salida.tag_configure("sec", foreground=TEXTO_SEC)
        self._escribir("Completa el formulario y presiona\n«Obtener recomendación».", "sec")

    def _escribir(self, texto, tag=None):
        self.salida.configure(state="normal")
        if tag:
            self.salida.insert("end", texto + "\n", tag)
        else:
            self.salida.insert("end", texto + "\n")
        self.salida.configure(state="disabled")
        self.salida.see("end")

    # ------------------------------------------------------------- acciones
    def _recoger_respuestas(self):
        respuestas = {}
        for hecho in HECHOS:
            clave = hecho["clave"]
            var = self.variables[clave]
            if hecho["tipo"] == "check":
                marcadas = [v for v, boolean in var.items() if boolean.get()]
                if marcadas:
                    respuestas[clave] = marcadas
            else:
                valor = var.get().strip()
                if valor:
                    respuestas[clave] = valor
        return respuestas

    def recomendar(self):
        respuestas = self._recoger_respuestas()
        self.salida.configure(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.configure(state="disabled")

        faltantes = [h["enunciado"] for h in HECHOS
                     if h["tipo"] == "radio" and h["clave"] not in respuestas]
        if faltantes:
            self._escribir("⚠ Faltan respuestas por marcar:", "titulo")
            for enunciado in faltantes:
                self._escribir("  · " + enunciado, "sec")
            return

        motor = MotorInferencia()
        resultado = motor.inferir(hechos_desde_respuestas(respuestas))

        self._escribir("RECOMENDACIÓN", "titulo")
        if resultado["conclusiones"]:
            for genero in resultado["conclusiones"]:
                self._escribir("▶ " + NOMBRES_GENERO.get(genero, genero), "destacado")
                sugeridas = PELICULAS_SUGERIDAS.get(genero)
                if sugeridas:
                    self._escribir("   Sugerencias: " + sugeridas, "sec")
        else:
            self._escribir("Ninguna regla se activó con estas respuestas.", "sec")
        if resultado["formatos"]:
            self._escribir("Formato sugerido: " + ", ".join(resultado["formatos"]), "sec")
        if "pelicula_favorita" in respuestas:
            self._escribir("Gusto registrado: " + respuestas["pelicula_favorita"], "sec")

        self._escribir("")
        self._escribir("REGLAS APLICADAS", "titulo")
        for regla in resultado["reglas_disparadas"]:
            self._escribir(f'{regla["id"]} (prioridad {regla["prioridad"]}): {regla["explicacion"]}')

        self._escribir("")
        self._escribir("TRAZA DEL MOTOR DE INFERENCIA", "titulo")
        for paso in resultado["traza"]:
            self._escribir(f"  [{paso['fase']}] {paso['texto']}", "sec")

    def limpiar(self):
        for hecho in HECHOS:
            var = self.variables[hecho["clave"]]
            if hecho["tipo"] == "check":
                for boolean in var.values():
                    boolean.set(False)
            else:
                var.set("")
        self.salida.configure(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.configure(state="disabled")
        self._escribir("Formulario reiniciado.", "sec")


def main():
    Aplicacion().mainloop()


if __name__ == "__main__":
    main()
