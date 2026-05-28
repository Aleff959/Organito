"""
Coleta informações do sistema de forma multiplataforma.
"""
import platform
import os
from pathlib import Path

def _read_os_release() -> dict:
    data = {}
    try:
        for line in Path("/etc/os-release").read_text().splitlines():
            if "=" in line:
                k, _, v = line.partition("=")
                data[k.strip()] = v.strip().strip('"')
    except Exception:
        pass
    return data

def get_info() -> dict:
    info = {}

    # ── OS ──
    system = platform.system()
    if system == "Linux":
        rel = _read_os_release()
        info["os_name"]    = rel.get("PRETTY_NAME", platform.platform())
        info["os_id"]      = rel.get("ID", "linux")
    elif system == "Windows":
        info["os_name"]    = platform.version()
        info["os_id"]      = "windows"
    elif system == "Darwin":
        info["os_name"]    = f"macOS {platform.mac_ver()[0]}"
        info["os_id"]      = "macos"
    else:
        info["os_name"]    = platform.platform()
        info["os_id"]      = system.lower()

    info["kernel"]     = platform.release()
    info["arch"]       = platform.machine()
    info["hostname"]   = platform.node()

    # ── Desktop (Linux) ──
    info["desktop"]    = os.environ.get("XDG_CURRENT_DESKTOP", "") or \
                         os.environ.get("DESKTOP_SESSION", "") or "—"
    info["session"]    = os.environ.get("XDG_SESSION_TYPE", "—")

    # ── CPU ──
    info["cpu_model"]  = platform.processor() or "—"
    try:
        import psutil
        info["cpu_cores"]  = psutil.cpu_count(logical=True)
        info["cpu_physical"]= psutil.cpu_count(logical=False)
    except ImportError:
        try:
            info["cpu_cores"] = os.cpu_count() or "—"
            info["cpu_physical"] = "—"
        except Exception:
            info["cpu_cores"] = "—"
            info["cpu_physical"] = "—"

    # ── Hardware model ──
    hw_model = "—"
    try:
        p = Path("/sys/devices/virtual/dmi/id")
        vendor = (p / "sys_vendor").read_text().strip()
        product = (p / "product_name").read_text().strip()
        hw_model = f"{vendor} {product}"
    except Exception:
        pass
    info["hw_model"] = hw_model

    # ── RAM ──
    try:
        import psutil
        vm = psutil.virtual_memory()
        total_gb = vm.total / (1024**3)
        avail_gb = vm.available / (1024**3)
        info["ram_total"] = f"{total_gb:.1f} GiB"
        info["ram_avail"] = f"{avail_gb:.1f} GiB"
        info["ram_percent"] = vm.percent
    except Exception:
        info["ram_total"] = "—"
        info["ram_avail"] = "—"
        info["ram_percent"] = 0

    # ── Disco (root / C:) ──
    try:
        import psutil
        mount = "C:\\" if platform.system() == "Windows" else "/"
        du = psutil.disk_usage(mount)
        total_gb = du.total / (1024**3)
        free_gb  = du.free  / (1024**3)
        info["disk_total"]   = f"{total_gb:.1f} GB"
        info["disk_free"]    = f"{free_gb:.1f} GB"
        info["disk_percent"] = du.percent
    except Exception:
        info["disk_total"]   = "—"
        info["disk_free"]    = "—"
        info["disk_percent"] = 0

    # ── Python / GTK / Adw ──
    info["python_version"] = platform.python_version()
    try:
        import gi
        gi.require_version("Gtk", "4.0")
        gi.require_version("Adw", "1")
        from gi.repository import Gtk, Adw
        info["gtk_version"] = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        info["adw_version"] = f"{Adw.VERSION_S}" if hasattr(Adw, "VERSION_S") else "1.x"
    except Exception:
        info["gtk_version"] = "—"
        info["adw_version"] = "—"

    info["app_version"] = "1.0"

    return info
