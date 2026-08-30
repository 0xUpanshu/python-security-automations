from pathlib import Path

EXECUTABLE_EXTENSIONS = {".exe",".scr",".com",".bat",".cmd",".ps1",".vbs",".vbe",".js",".jse",".wsf",".wsh",".msi",}


def check_double_extension(file_path: str) -> bool:

    # Detect filenames that contain multiple extensions where the final extension is executable/script-like.

    path = Path(file_path)
    suffixes = [suffix.lower() for suffix in path.suffixes]

    if len(suffixes) < 2:
        return False

    return suffixes[-1] in EXECUTABLE_EXTENSIONS


def check_hidden_file(file_path: str) -> bool:


   # Detect hidden files based on OS-specific conventions.
    path = Path(file_path)

    # Unix/Linux/macOS hidden-file convention.
    if path.name.startswith("."):
        return True

    # Windows hidden attribute.
    try:
        import ctypes

        FILE_ATTRIBUTE_HIDDEN = 0x2

        attributes = ctypes.windll.kernel32.GetFileAttributesW(str(path))

        if attributes == -1:
            return False

        return bool(attributes & FILE_ATTRIBUTE_HIDDEN)

    except (AttributeError, OSError):
        # ctypes.windll is unavailable on non-Windows systems.
        return False


def check_suspicious_extension(file_path: str) -> bool:

    return Path(file_path).suffix.lower() in EXECUTABLE_EXTENSIONS


def analyze_file(file_path: str) -> dict:    

    indicators = []

    if check_double_extension(file_path):
        indicators.append("double_extension")

    if check_hidden_file(file_path):
        indicators.append("hidden_file")

    if check_suspicious_extension(file_path):
        indicators.append("executable_or_script")

    return {
        "file_path": str(file_path),
        "suspicious": bool(indicators),
        "indicators": indicators,
    }