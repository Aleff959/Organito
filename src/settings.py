"""
Persistência de configurações via JSON em ~/.config/organito/settings.json
"""
import json
import platform
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import os
    _CFG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "Organito"
    DEFAULT_LOG_PATH = str(_CFG_DIR / "logs")
else:
    _CFG_DIR = Path.home() / ".config" / "organito"
    DEFAULT_LOG_PATH = str(Path.home() / ".local" / "share" / "organito" / "logs")

_CFG_FILE = _CFG_DIR / "settings.json"

DEFAULTS = {
    # Aparência
    "theme": "auto",
    # Arquivos
    "ignore_hidden": True,
    "ignore_system": True,
    "ignore_temp": True,
    # Conflito
    "conflict": "rename",   # rename | skip | replace
    # Segurança
    "confirm_before_move": False,
    "use_trash": False,
    # Avançado — subpastas
    "recursive": False,
    "max_depth": 1,
    # Avançado — tamanho
    "min_size": 0,
    "max_size": 0,
    # Avançado — desempenho
    "max_files": 0,
    "move_delay_ms": 0,
    # Avançado — log
    "log_enabled": False,
    "log_path": DEFAULT_LOG_PATH,
    # Avançado — dry run
    "dry_run": False,
    # Windows
    "win_ignore_system": True,
    "win_reserved": True,
    "win_long_paths": False,
}


def load() -> dict:
    if _CFG_FILE.exists():
        try:
            data = json.loads(_CFG_FILE.read_text(encoding="utf-8"))
            merged = {**DEFAULTS, **data}
            return merged
        except Exception:
            pass
    return dict(DEFAULTS)


def save(cfg: dict):
    _CFG_DIR.mkdir(parents=True, exist_ok=True)
    _CFG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
