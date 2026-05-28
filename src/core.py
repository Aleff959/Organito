import os
import shutil
import platform
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"

CATEGORIES = {
    "Imagens": [
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp", ".tiff", ".tif",
        ".ico", ".heic", ".heif", ".avif", ".raw", ".cr2", ".cr3", ".nef", ".arw",
        ".dng", ".orf", ".rw2", ".pef", ".srw", ".x3f", ".psd", ".ai", ".eps",
        ".xcf", ".jxl", ".jp2", ".j2k", ".exr", ".hdr", ".tga", ".wbmp", ".pbm",
        ".pgm", ".ppm",
    ],
    "Documentos": [
        ".pdf", ".docx", ".doc", ".odt", ".txt", ".rtf", ".md", ".markdown",
        ".tex", ".latex", ".wpd", ".wps", ".pages", ".abw", ".zabw", ".sxw",
        ".fodt", ".uot", ".epub", ".mobi", ".azw", ".azw3", ".fb2", ".djvu",
        ".oxps", ".xps", ".hwp", ".hwpx", ".sdw", ".vor", ".dot", ".dotx",
        ".docm", ".dotm", ".rst", ".asciidoc", ".adoc", ".org", ".wiki",
        ".textile", ".log", ".nfo", ".info",
    ],
    "Planilhas": [
        ".xlsx", ".xls", ".ods", ".csv", ".tsv", ".xlsm", ".xlsb", ".xltx",
        ".xltm", ".xlt", ".xlam", ".xlw", ".fods", ".uos", ".sxc", ".stc",
        ".dif", ".slk", ".numbers", ".gnumeric", ".wk1", ".wk3", ".wk4",
        ".wb2", ".qpw", ".dbf",
    ],
    "Apresentações": [
        ".pptx", ".ppt", ".odp", ".pps", ".ppsx", ".ppsm", ".pptm", ".potx",
        ".potm", ".pot", ".fodp", ".uop", ".sxi", ".sti", ".key", ".kth",
    ],
    "Vídeos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v",
        ".mpeg", ".mpg", ".mpe", ".ts", ".mts", ".m2ts", ".vob", ".ogv",
        ".3gp", ".3g2", ".f4v", ".f4p", ".asf", ".rm", ".rmvb", ".divx",
        ".xvid", ".amv", ".dv", ".mxf", ".roq", ".nsv", ".svi", ".yuv",
        ".wtv", ".dvr-ms",
    ],
    "Áudio": [
        ".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".opus",
        ".aiff", ".aif", ".ape", ".mka", ".mpc", ".mp2", ".ac3", ".dts",
        ".ra", ".ram", ".mid", ".midi", ".kar", ".gsm", ".spx", ".caf",
        ".au", ".snd", ".amr", ".awb", ".tta", ".vox", ".8svx", ".w64",
        ".rf64", ".bwf",
    ],
    "Compactados": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tar.gz",
        ".tar.bz2", ".tar.xz", ".tar.zst", ".tgz", ".tbz", ".tbz2", ".txz",
        ".lz", ".lzma", ".lzo", ".zst", ".br", ".cab", ".iso", ".img",
        ".dmg", ".pkg", ".mpkg", ".cpio", ".ar", ".arj", ".lzh", ".lha",
        ".ace", ".sit", ".sitx", ".sea", ".z", ".taz", ".tz",
    ],
    "Instaladores": [
        ".deb", ".rpm", ".appimage", ".sh", ".exe", ".msi", ".dmg", ".pkg",
        ".apk", ".ipa", ".snap", ".flatpakref", ".run", ".bin", ".jar",
        ".war", ".ear", ".nupkg", ".vsix", ".crx", ".xpi", ".oxt",
        ".install", ".setup",
    ],
    "Código": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".htm", ".css", ".scss",
        ".sass", ".less", ".php", ".rb", ".java", ".c", ".cpp", ".cc", ".cxx",
        ".h", ".hpp", ".cs", ".go", ".rs", ".swift", ".kt", ".kts", ".dart",
        ".lua", ".pl", ".pm", ".r", ".R", ".m", ".mm", ".asm", ".s", ".sql",
        ".bash", ".zsh", ".fish", ".ps1", ".psm1", ".bat", ".cmd",
        ".vb", ".vbs", ".fs", ".fsx", ".clj", ".cljs", ".ex", ".exs",
        ".erl", ".hrl", ".hs", ".lhs", ".ml", ".mli", ".nim", ".nims",
        ".cr", ".d", ".jl", ".scala", ".groovy", ".gradle", ".cmake",
        ".make", ".mk", ".toml", ".yaml", ".yml", ".json", ".xml", ".ini",
        ".cfg", ".conf", ".env",
    ],
    "Fontes": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".fnt", ".pfb",
        ".pfm", ".afm", ".bdf", ".pcf", ".snf", ".pfa", ".dfont", ".sfd",
    ],
    "Banco de Dados": [
        ".db", ".sqlite", ".sqlite3", ".db3", ".s3db", ".sl3", ".mdb",
        ".accdb", ".mdf", ".ldf", ".ndf", ".frm", ".ibd", ".myd", ".myi",
        ".fdb", ".gdb", ".nsf", ".ntf", ".dump", ".bak",
    ],
    "3D e CAD": [
        ".stl", ".obj", ".fbx", ".dae", ".3ds", ".blend", ".skp", ".dwg",
        ".dxf", ".step", ".stp", ".iges", ".igs", ".x3d", ".wrl", ".vrml",
        ".glb", ".gltf", ".usd", ".usda", ".usdc", ".abc", ".ply", ".ptx",
        ".ma", ".mb", ".max", ".c4d", ".lwo", ".lws", ".zpr", ".ztl",
    ],
    "Torrents e P2P": [
        ".torrent",
    ],
}

# Extensões temporárias/de sistema que podem ser ignoradas
TEMP_EXTENSIONS = {
    ".tmp", ".temp", ".crdownload", ".part", ".partial",
    ".downloading", ".opdownload", ".~", ".swp", ".swo",
    ".lock", ".lck",
}

SYSTEM_FILES_LINUX = {
    ".directory", ".ds_store", ".localized",
}

SYSTEM_FILES_WINDOWS = {
    "thumbs.db", "desktop.ini", "autorun.inf",
    "ntldr", "bootmgr", "pagefile.sys", "hiberfil.sys",
}

WINDOWS_RESERVED_NAMES = {
    "con", "prn", "aux", "nul",
    "com1","com2","com3","com4","com5","com6","com7","com8","com9",
    "lpt1","lpt2","lpt3","lpt4","lpt5","lpt6","lpt7","lpt8","lpt9",
}


def get_unique_path(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path
    stem, suffix, directory = target_path.stem, target_path.suffix, target_path.parent
    counter = 1
    while True:
        new_path = directory / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def is_system_file(file_path: Path) -> bool:
    name_lower = file_path.name.lower()
    if name_lower in SYSTEM_FILES_LINUX:
        return True
    if IS_WINDOWS and name_lower in SYSTEM_FILES_WINDOWS:
        return True
    return False


def is_temp_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in TEMP_EXTENSIONS


def is_windows_reserved(name: str) -> bool:
    stem = Path(name).stem.lower()
    return stem in WINDOWS_RESERVED_NAMES


def organize_directory(source_dir: str, active_categories: dict,
                       options: dict = None, callback_progress=None) -> dict:
    """
    Organiza arquivos em source_dir.
    options: dict com chaves:
        ignore_hidden (bool)
        ignore_system (bool)
        ignore_temp (bool)
        conflict (str): 'rename' | 'skip' | 'replace'
        dry_run (bool)
        recursive (bool)
        max_depth (int)
        min_size (int) bytes, 0 = sem limite
        max_size (int) bytes, 0 = sem limite
        max_files (int) 0 = sem limite
        use_trash (bool)
        win_reserved (bool)
        win_long_paths (bool)
        log_enabled (bool)
        log_path (str)
    Retorna dict: moved, skipped, errors, log_lines
    """
    if options is None:
        options = {}

    ignore_hidden   = options.get("ignore_hidden", True)
    ignore_system   = options.get("ignore_system", True)
    ignore_temp     = options.get("ignore_temp", True)
    conflict        = options.get("conflict", "rename")
    dry_run         = options.get("dry_run", False)
    recursive       = options.get("recursive", False)
    max_depth       = options.get("max_depth", 1)
    min_size        = options.get("min_size", 0)
    max_size        = options.get("max_size", 0)
    max_files_limit = options.get("max_files", 0)
    use_trash       = options.get("use_trash", False)
    win_reserved    = options.get("win_reserved", True)
    win_long_paths  = options.get("win_long_paths", False)
    log_enabled     = options.get("log_enabled", False)
    log_path        = options.get("log_path", "")

    source_path = Path(source_dir)
    if not source_path.exists() or not source_path.is_dir():
        raise ValueError("Diretório inválido.")

    def collect_files(path: Path, depth: int):
        result = []
        try:
            for f in path.iterdir():
                if f.is_file():
                    result.append((f, depth))
                elif f.is_dir() and recursive and depth < max_depth:
                    # Não entrar nas pastas de categoria já criadas
                    if f.name not in CATEGORIES:
                        result.extend(collect_files(f, depth + 1))
        except PermissionError:
            pass
        return result

    all_files = collect_files(source_path, 1)
    moved, skipped, errors = 0, 0, []
    log_lines = []

    total = len(all_files)
    if max_files_limit > 0:
        all_files = all_files[:max_files_limit]
        total = len(all_files)

    for index, (file_path, _depth) in enumerate(all_files):
        name = file_path.name

        # Filtros
        if ignore_hidden and name.startswith('.'):
            skipped += 1
            if callback_progress: callback_progress(index + 1, total)
            continue
        if ignore_system and is_system_file(file_path):
            skipped += 1
            if callback_progress: callback_progress(index + 1, total)
            continue
        if ignore_temp and is_temp_file(file_path):
            skipped += 1
            if callback_progress: callback_progress(index + 1, total)
            continue

        # Tamanho
        try:
            size = file_path.stat().st_size
            if min_size > 0 and size < min_size:
                skipped += 1
                if callback_progress: callback_progress(index + 1, total)
                continue
            if max_size > 0 and size > max_size:
                skipped += 1
                if callback_progress: callback_progress(index + 1, total)
                continue
        except OSError:
            pass

        # Windows: nomes reservados
        if IS_WINDOWS and win_reserved and is_windows_reserved(name):
            skipped += 1
            log_lines.append(f"[SKIP] Nome reservado: {name}")
            if callback_progress: callback_progress(index + 1, total)
            continue

        # Windows: caminhos longos
        if IS_WINDOWS and not win_long_paths:
            if len(str(file_path)) > 260:
                skipped += 1
                log_lines.append(f"[SKIP] Caminho longo: {file_path}")
                if callback_progress: callback_progress(index + 1, total)
                continue

        ext = file_path.suffix.lower()
        target_category = next(
            (cat for cat, exts in CATEGORIES.items() if ext in exts), None
        )

        if target_category and active_categories.get(target_category, True):
            target_dir = source_path / target_category
            if not dry_run:
                target_dir.mkdir(exist_ok=True)

            dest_path = get_unique_path(target_dir / name)

            if conflict == "skip" and (target_dir / name).exists():
                skipped += 1
                log_lines.append(f"[SKIP] Já existe: {name}")
                if callback_progress: callback_progress(index + 1, total)
                continue

            if conflict == "replace":
                dest_path = target_dir / name

            try:
                if not dry_run:
                    if use_trash:
                        try:
                            import send2trash
                            if dest_path.exists():
                                send2trash.send2trash(str(dest_path))
                        except ImportError:
                            pass
                    shutil.move(str(file_path), str(dest_path))
                moved += 1
                log_lines.append(f"[OK] {name} → {target_category}/")
            except Exception as e:
                errors.append(str(e))
                log_lines.append(f"[ERRO] {name}: {e}")

        if callback_progress:
            callback_progress(index + 1, total)

    # Salvar log
    if log_enabled and log_path and log_lines:
        try:
            import datetime
            log_file = Path(log_path) / f"organito_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            log_file.write_text("\n".join(log_lines), encoding="utf-8")
        except Exception as e:
            errors.append(f"Log: {e}")

    return {"moved": moved, "skipped": skipped, "errors": errors, "log_lines": log_lines}
