from pathlib import Path

import pymupdf4llm


def _limpiar_markdown(markdown):
    """Reduce espacios vacíos repetidos sin modificar el contenido extraído."""
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    cleaned_lines = []
    previous_line_was_empty = False

    for line in lines:
        if line.strip() == "":
            if not previous_line_was_empty:
                cleaned_lines.append("")
            previous_line_was_empty = True
            continue

        cleaned_lines.append(line)
        previous_line_was_empty = False

    while cleaned_lines and cleaned_lines[0] == "":
        cleaned_lines.pop(0)

    while cleaned_lines and cleaned_lines[-1] == "":
        cleaned_lines.pop()

    return "\n".join(cleaned_lines)


def convertir_pdf_a_markdown(pdf_path, output_folder):
    """Convierte un PDF en Markdown y devuelve la ruta del archivo generado."""
    pdf_path = Path(pdf_path)
    output_folder = Path(output_folder)

    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo PDF: {pdf_path}")

    if not pdf_path.is_file():
        raise ValueError(f"La ruta del PDF no es un archivo: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"El archivo debe tener extensión .pdf: {pdf_path}")

    output_folder.mkdir(parents=True, exist_ok=True)
    output_path = output_folder / f"{pdf_path.stem}.md"

    try:
        markdown = pymupdf4llm.to_markdown(str(pdf_path))
        cleaned_markdown = _limpiar_markdown(markdown)
        output_path.write_text(cleaned_markdown, encoding="utf-8")
    except Exception as error:
        raise RuntimeError(f"No se pudo convertir el PDF '{pdf_path}': {error}") from error

    return str(output_path)