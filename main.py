import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.converter import convertir_pdf_a_markdown


def seleccionar_pdf(ruta_pdf):
    """Permite seleccionar el PDF que se va a convertir."""
    pdf_path = filedialog.askopenfilename(
        title="Seleccionar PDF",
        filetypes=[("Archivos PDF", "*.pdf")],
    )
    if pdf_path:
        ruta_pdf.set(pdf_path)


def seleccionar_carpeta_salida(carpeta_salida):
    """Permite seleccionar la carpeta donde se guardara el Markdown."""
    output_folder = filedialog.askdirectory(title="Seleccionar carpeta de salida")
    if output_folder:
        carpeta_salida.set(output_folder)


def ejecutar_conversion(pdf_path, output_folder, resultado_queue):
    """Ejecuta la conversion en segundo plano y envia el resultado."""
    try:
        output_path = convertir_pdf_a_markdown(pdf_path, output_folder)
        resultado_queue.put(("exito", output_path))
    except Exception as error:
        resultado_queue.put(("error", str(error)))


def revisar_resultado(
    ventana,
    resultado_queue,
    barra_progreso,
    boton_convertir,
    mensaje_estado,
):
    """Comprueba si el hilo termino sin bloquear la ventana."""
    try:
        resultado, mensaje = resultado_queue.get_nowait()
    except queue.Empty:
        ventana.after(
            100,
            lambda: revisar_resultado(
                ventana,
                resultado_queue,
                barra_progreso,
                boton_convertir,
                mensaje_estado,
            ),
        )
        return

    barra_progreso.stop()
    barra_progreso.configure(
        mode="determinate",
        value=100 if resultado == "exito" else 0,
    )
    boton_convertir.configure(state="normal")

    if resultado == "exito":
        mensaje_estado.set(f"Conversion exitosa. Archivo generado: {mensaje}")
    else:
        mensaje_estado.set(f"Error durante la conversion: {mensaje}")
        messagebox.showerror("Error de conversion", mensaje)


def convertir_pdf(
    ventana,
    ruta_pdf,
    carpeta_salida,
    barra_progreso,
    boton_convertir,
    mensaje_estado,
):
    """Valida los datos e inicia la conversion sin congelar la interfaz."""
    pdf_path = ruta_pdf.get()
    output_folder = carpeta_salida.get()

    if not pdf_path or not output_folder:
        mensaje_estado.set("Selecciona un PDF y una carpeta de salida.")
        messagebox.showwarning(
            "Datos incompletos",
            "Debes seleccionar un PDF y una carpeta de salida.",
        )
        return

    boton_convertir.configure(state="disabled")
    barra_progreso.configure(mode="indeterminate", value=0)
    barra_progreso.start(10)
    mensaje_estado.set("Convirtiendo PDF... La ventana sigue disponible.")

    resultado_queue = queue.Queue()
    hilo_conversion = threading.Thread(
        target=ejecutar_conversion,
        args=(pdf_path, output_folder, resultado_queue),
        daemon=True,
    )
    hilo_conversion.start()

    ventana.after(
        100,
        lambda: revisar_resultado(
            ventana,
            resultado_queue,
            barra_progreso,
            boton_convertir,
            mensaje_estado,
        ),
    )


def main():
    ventana = tk.Tk()
    ventana.title("Convertidor de PDF a Markdown")
    ventana.geometry("700x360")
    ventana.minsize(600, 320)

    estilo = ttk.Style(ventana)
    estilo.configure("Titulo.TLabel", font=("TkDefaultFont", 16, "bold"))
    estilo.configure("Estado.TLabel", foreground="#444444")

    ruta_pdf = tk.StringVar()
    carpeta_salida = tk.StringVar()
    mensaje_estado = tk.StringVar(value="Selecciona un PDF para comenzar.")

    contenedor = ttk.Frame(ventana, padding=20)
    contenedor.pack(fill="both", expand=True)
    contenedor.columnconfigure(1, weight=1)

    ttk.Label(
        contenedor,
        text="Convertidor de PDF a Markdown",
        style="Titulo.TLabel",
    ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

    ttk.Label(contenedor, text="Archivo PDF:").grid(
        row=1, column=0, sticky="w", padx=(0, 10), pady=8
    )
    ttk.Entry(contenedor, textvariable=ruta_pdf, state="readonly").grid(
        row=1, column=1, sticky="ew", pady=8
    )
    ttk.Button(
        contenedor,
        text="Seleccionar PDF",
        command=lambda: seleccionar_pdf(ruta_pdf),
    ).grid(row=1, column=2, padx=(10, 0), pady=8)

    ttk.Label(contenedor, text="Carpeta de salida:").grid(
        row=2, column=0, sticky="w", padx=(0, 10), pady=8
    )
    ttk.Entry(contenedor, textvariable=carpeta_salida, state="readonly").grid(
        row=2, column=1, sticky="ew", pady=8
    )
    ttk.Button(
        contenedor,
        text="Seleccionar carpeta",
        command=lambda: seleccionar_carpeta_salida(carpeta_salida),
    ).grid(row=2, column=2, padx=(10, 0), pady=8)

    barra_progreso = ttk.Progressbar(contenedor, mode="determinate")
    barra_progreso.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(20, 12))

    boton_convertir = ttk.Button(contenedor, text="Convertir a Markdown")
    boton_convertir.configure(
        command=lambda: convertir_pdf(
            ventana,
            ruta_pdf,
            carpeta_salida,
            barra_progreso,
            boton_convertir,
            mensaje_estado,
        )
    )
    boton_convertir.grid(row=4, column=0, columnspan=3, pady=8)

    ttk.Separator(contenedor).grid(
        row=5, column=0, columnspan=3, sticky="ew", pady=12
    )
    ttk.Label(
        contenedor,
        textvariable=mensaje_estado,
        style="Estado.TLabel",
        wraplength=650,
    ).grid(row=6, column=0, columnspan=3, sticky="w")

    ventana.mainloop()


if __name__ == "__main__":
    main()