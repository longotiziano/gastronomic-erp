import os
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from utils.exceptions import ValidationError

ALLOWED_EXCEL_EXTENSIONS = {".xlsx", ".xls"}
MAX_EXCEL_SIZE_MB = 10

# Magic bytes: .xlsx es un zip (PK\x03\x04), .xls es OLE2 (D0 CF 11 E0)
EXCEL_SIGNATURES = {
    b"\x50\x4B\x03\x04": ".xlsx",
    b"\xD0\xCF\x11\xE0": ".xls",
}


def validate_excel_file(file: FileStorage | None, max_size_mb: int = MAX_EXCEL_SIZE_MB) -> str:
    """
    Valida un archivo Excel subido por formulario antes de guardarlo o procesarlo.
    Devuelve el filename saneado si es válido, o lanza ValidationError.
    """
    if not file or not file.filename:
        raise ValidationError("No se seleccionó ningún archivo.")

    filename = secure_filename(file.filename)
    if not filename:
        raise ValidationError("El nombre del archivo no es válido.")

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXCEL_EXTENSIONS:
        raise ValidationError("El archivo debe ser un Excel (.xlsx o .xls).")

    file.stream.seek(0, os.SEEK_END)
    size_mb = file.stream.tell() / (1024 * 1024)
    file.stream.seek(0)
    if size_mb > max_size_mb:
        raise ValidationError(f"El archivo supera el límite de {max_size_mb}MB.")
    if size_mb == 0:
        raise ValidationError("El archivo está vacío.")

    header = file.stream.read(4)
    file.stream.seek(0)
    if not any(header.startswith(sig) for sig in EXCEL_SIGNATURES):
        raise ValidationError("El archivo no parece ser un Excel válido.")

    print("Archivo con todo en orden!")
    return filename