import gi
import threading
import platform

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Pango, Gdk, GdkPixbuf

from core import CATEGORIES, organize_directory, IS_WINDOWS
from settings import load as cfg_load, save as cfg_save, DEFAULTS
import sysinfo

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
/* ── Light tokens ── */
@define-color md_primary            #6750A4;
@define-color md_on_primary         #FFFFFF;
@define-color md_primary_container  #EADDFF;
@define-color md_on_primary_container #21005D;
@define-color md_secondary_container #E8DEF8;
@define-color md_surface            #FFFBFE;
@define-color md_surface_variant    #E7E0EC;
@define-color md_on_surface         #1C1B1F;
@define-color md_on_surface_variant #49454F;
@define-color md_outline            #79747E;
@define-color md_outline_variant    #CAC4D0;

window.org-dark {
    background-color: #1C1B1F;
}
window.org-dark headerbar {
    background-color: #2B2930;
    border-bottom-color: #49454F;
}

/* ── Cards ── */
.md-card {
    background-color: @md_surface;
    border: 1px solid @md_outline_variant;
    border-radius: 12px;
    padding: 16px;
}
window.org-dark .md-card {
    background-color: #2B2930;
    border-color: #49454F;
}
.md-card-tonal {
    background-color: @md_secondary_container;
    border-radius: 12px;
    padding: 14px;
}
window.org-dark .md-card-tonal {
    background-color: #4A4458;
}

/* ── Typography ── */
.label-section {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: @md_on_surface_variant;
}
window.org-dark .label-section { color: #CAC4D0; }

.label-body  { font-size: 14px; color: @md_on_surface; }
window.org-dark .label-body  { color: #E6E1E5; }

.label-sub   { font-size: 12px; color: @md_on_surface_variant; }
window.org-dark .label-sub   { color: #CAC4D0; }

.label-title { font-size: 22px; font-weight: 300; color: @md_primary; letter-spacing: -0.3px; }
window.org-dark .label-title { color: #D0BCFF; }

.label-mono  { font-family: monospace; font-size: 12px; color: @md_on_surface_variant; }
window.org-dark .label-mono  { color: #CAC4D0; }

/* ── Folder row ── */
.folder-row {
    background-color: @md_surface_variant;
    border-radius: 12px;
    padding: 12px 16px;
}
window.org-dark .folder-row { background-color: #49454F; }

/* ── Buttons ── */
.btn-outlined {
    background: transparent;
    border: 1px solid @md_primary;
    border-radius: 20px;
    color: @md_primary;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 14px;
    box-shadow: none;
}
.btn-outlined:hover { background-color: alpha(@md_primary, 0.08); }
window.org-dark .btn-outlined { border-color: #D0BCFF; color: #D0BCFF; }

.btn-filled {
    background-color: @md_primary;
    color: @md_on_primary;
    border-radius: 20px;
    padding: 12px 28px;
    font-weight: 600;
    font-size: 15px;
    border: none;
    box-shadow: 0 1px 3px alpha(#000, 0.25);
}
.btn-filled:hover { background-color: shade(@md_primary, 0.92); box-shadow: 0 2px 8px alpha(#000,.3); }
.btn-filled:disabled { background-color: alpha(@md_on_surface, 0.12); color: alpha(@md_on_surface, 0.38); box-shadow: none; }
window.org-dark .btn-filled { background-color: #D0BCFF; color: #381E72; }
window.org-dark .btn-filled:disabled { background-color: alpha(#E6E1E5, 0.12); color: alpha(#E6E1E5, 0.38); }

/* ── Category chips ── */
.cat-chip {
    background-color: @md_surface_variant;
    border: 1px solid @md_outline_variant;
    border-radius: 8px;
    padding: 6px 10px;
    margin: 3px;
}
window.org-dark .cat-chip { background-color: #49454F; border-color: #938F99; }
.cat-chip label { font-size: 13px; color: @md_on_surface; }
window.org-dark .cat-chip label { color: #E6E1E5; }

/* ── Progress ── */
progressbar trough { background-color: @md_secondary_container; border-radius: 4px; min-height: 6px; border: none; }
progressbar progress { background-color: @md_primary; border-radius: 4px; min-height: 6px; }
window.org-dark progressbar trough { background-color: #4A4458; }
window.org-dark progressbar progress { background-color: #D0BCFF; }

/* ── Badge ── */
.badge {
    background-color: @md_primary_container;
    color: @md_on_primary_container;
    border-radius: 10px;
    padding: 1px 8px;
    font-size: 11px;
    font-weight: 600;
}
window.org-dark .badge { background-color: #4F378B; color: #EADDFF; }

/* ── Switch ── */
switch:checked { background-color: @md_primary; }
window.org-dark switch:checked { background-color: #D0BCFF; }

/* ── Settings rows ── */
.setting-row {
    padding: 4px 0;
}

/* ── Sysinfo value ── */
.sys-value {
    font-size: 13px;
    font-weight: 500;
    color: @md_on_surface;
}
window.org-dark .sys-value { color: #E6E1E5; }

/* ── Progress bar mini (sysinfo) ── */
.bar-mini trough { min-height: 4px; background-color: @md_secondary_container; border-radius: 2px; border: none; }
.bar-mini progress { min-height: 4px; background-color: @md_primary; border-radius: 2px; }
window.org-dark .bar-mini trough { background-color: #4A4458; }
window.org-dark .bar-mini progress { background-color: #D0BCFF; }

/* ── Popover menu ── */
popover.menu-popover contents {
    padding: 6px 0;
    min-width: 200px;
}
popover.menu-popover button {
    border-radius: 0;
    padding: 10px 20px;
    font-size: 14px;
    box-shadow: none;
    border: none;
    background: transparent;
}
popover.menu-popover button:hover {
    background-color: alpha(@md_primary, 0.08);
}
window.org-dark popover.menu-popover contents {
    background-color: #2B2930;
}
window.org-dark popover.menu-popover button {
    color: #E6E1E5;
}
"""

CATEGORY_ICONS = {
    "Imagens": "🖼", "Documentos": "📄", "Planilhas": "📊",
    "Apresentações": "📽", "Vídeos": "🎬", "Áudio": "🎵",
    "Compactados": "📦", "Instaladores": "⚙", "Código": "💻",
    "Fontes": "🔤", "Banco de Dados": "🗄", "3D e CAD": "🧊",
    "Torrents e P2P": "🔗",
}

_css_applied = False

def apply_css():
    global _css_applied
    if _css_applied:
        return
    provider = Gtk.CssProvider()
    provider.load_from_data(CSS.encode())
    Gdk.Display.get_default().connect(
        "opened",
        lambda d: Gtk.StyleContext.add_provider_for_display(
            d, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    )
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    _css_applied = True


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_section_label(text: str) -> Gtk.Label:
    lbl = Gtk.Label(label=text)
    lbl.set_halign(Gtk.Align.START)
    lbl.add_css_class("label-section")
    return lbl

def make_row(label: str, widget: Gtk.Widget, sublabel: str = "") -> Gtk.Box:
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    row.set_margin_top(2)
    row.set_margin_bottom(2)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    vbox.set_hexpand(True)
    lbl = Gtk.Label(label=label)
    lbl.set_halign(Gtk.Align.START)
    lbl.add_css_class("label-body")
    vbox.append(lbl)
    if sublabel:
        sub = Gtk.Label(label=sublabel)
        sub.set_halign(Gtk.Align.START)
        sub.add_css_class("label-sub")
        sub.set_wrap(True)
        sub.set_xalign(0)
        vbox.append(sub)
    row.append(vbox)
    widget.set_valign(Gtk.Align.CENTER)
    row.append(widget)
    return row

def make_card(*children, spacing=10) -> Gtk.Box:
    card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
    card.add_css_class("md-card")
    for c in children:
        card.append(c)
    return card

def scrolled_clamp(child, max_width=500, top=20, bottom=24, start=16, end=16) -> Gtk.ScrolledWindow:
    scroll = Gtk.ScrolledWindow()
    scroll.set_vexpand(True)
    clamp = Adw.Clamp()
    clamp.set_maximum_size(max_width)
    scroll.set_child(clamp)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    box.set_margin_top(top)
    box.set_margin_bottom(bottom)
    box.set_margin_start(start)
    box.set_margin_end(end)
    clamp.set_child(box)
    box.append(child) if not isinstance(child, list) else [box.append(c) for c in child]
    return scroll, box


# ─────────────────────────────────────────────────────────────────────────────
# Main Window
# ─────────────────────────────────────────────────────────────────────────────

class OrganitoWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Organito")
        self.set_default_size(480, 700)

        self._cfg = cfg_load()
        self._adw = Adw.StyleManager.get_default()
        self.selected_path = None

        apply_css()
        self.add_css_class("organito-window")
        self._apply_theme(self._cfg.get("theme", "auto"))

        # Toast overlay → root
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toast_overlay.set_child(root)

        # ── Header ──
        header = Adw.HeaderBar()
        header.set_centering_policy(Adw.CenteringPolicy.STRICT)

        # Hamburger button (left)
        self._menu_btn = Gtk.MenuButton()
        self._menu_btn.set_icon_name("open-menu-symbolic")
        self._menu_btn.add_css_class("flat")
        self._build_hamburger_popover()
        header.pack_start(self._menu_btn)

        root.append(header)

        # ── Stack (pages) ──
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_vexpand(True)
        root.append(self.stack)

        self.stack.add_named(self._build_home(), "home")
        self.stack.add_named(self._build_settings(), "settings")
        self.stack.add_named(self._build_system(), "system")
        self.stack.add_named(self._build_help(), "help")
        self.stack.add_named(self._build_about(), "about")
        self.stack.add_named(self._build_advanced(), "advanced")

        self._show_page("home")

    # ── Hamburger ─────────────────────────────────────────────────────────────

    def _build_hamburger_popover(self):
        popover = Gtk.Popover()
        popover.add_css_class("menu-popover")
        popover.set_has_arrow(True)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        popover.set_child(vbox)

        items = [
            ("🏠  Início",          "home"),
            ("⚙  Configurações",    "settings"),
            ("💻  Sistema",         "system"),
            ("❓  Ajuda",           "help"),
            None,  # separator
            ("ℹ  Sobre",            "about"),
        ]
        for item in items:
            if item is None:
                sep = Gtk.Separator()
                sep.set_margin_top(4)
                sep.set_margin_bottom(4)
                vbox.append(sep)
                continue
            label, page = item
            btn = Gtk.Button(label=label)
            btn.set_halign(Gtk.Align.FILL)
            btn.add_css_class("flat")
            p = page
            btn.connect("clicked", lambda b, pg=p: (popover.popdown(), self._show_page(pg)))
            vbox.append(btn)

        self._menu_btn.set_popover(popover)

    def _show_page(self, name: str):
        self.stack.set_visible_child_name(name)

    # ── Theme ─────────────────────────────────────────────────────────────────

    def _apply_theme(self, mode: str):
        self._cfg["theme"] = mode
        if mode == "dark":
            self._adw.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            self.add_css_class("org-dark")
        elif mode == "light":
            self._adw.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            self.remove_css_class("org-dark")
        else:
            self._adw.set_color_scheme(Adw.ColorScheme.DEFAULT)
            self.remove_css_class("org-dark")
        cfg_save(self._cfg)
        if hasattr(self, "_theme_radios"):
            for m, rb in self._theme_radios.items():
                rb.set_active(m == mode)

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: Home
    # ─────────────────────────────────────────────────────────────────────────

    def _build_home(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        # Card pasta
        folder_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        folder_card.add_css_class("md-card")
        folder_card.append(make_section_label("PASTA ALVO"))

        folder_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        folder_row.add_css_class("folder-row")
        folder_row.append(Gtk.Label(label="📁"))

        txt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        txt.set_hexpand(True)
        self.folder_label = Gtk.Label(label="Nenhuma pasta selecionada")
        self.folder_label.set_halign(Gtk.Align.START)
        self.folder_label.add_css_class("label-body")
        self.folder_label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        self.folder_sublabel = Gtk.Label(label="Toque em Selecionar para começar")
        self.folder_sublabel.set_halign(Gtk.Align.START)
        self.folder_sublabel.add_css_class("label-sub")
        txt.append(self.folder_label)
        txt.append(self.folder_sublabel)
        folder_row.append(txt)

        btn_sel = Gtk.Button(label="Selecionar")
        btn_sel.add_css_class("btn-outlined")
        btn_sel.set_valign(Gtk.Align.CENTER)
        btn_sel.connect("clicked", self.on_select)
        folder_row.append(btn_sel)
        folder_card.append(folder_row)
        box.append(folder_card)

        # Card categorias
        cat_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        cat_card.add_css_class("md-card")

        hdr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        ct = make_section_label("CATEGORIAS")
        ct.set_hexpand(True)
        badge = Gtk.Label(label=f"{len(CATEGORIES)} tipos")
        badge.add_css_class("badge")
        hdr.append(ct)
        hdr.append(badge)
        cat_card.append(hdr)

        trow = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        for lbl, st in [("Ativar todos", True), ("Limpar todos", False)]:
            b = Gtk.Button(label=lbl)
            b.add_css_class("flat")
            b.set_hexpand(True)
            s = st
            b.connect("clicked", lambda _, state=s: self._set_all_switches(state))
            trow.append(b)
        cat_card.append(trow)
        cat_card.append(Gtk.Separator())

        flow = Gtk.FlowBox()
        flow.set_selection_mode(Gtk.SelectionMode.NONE)
        flow.set_column_spacing(0)
        flow.set_row_spacing(0)
        cat_card.append(flow)

        self.switches = {}
        for cat in CATEGORIES:
            icon = CATEGORY_ICONS.get(cat, "📂")
            chip = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            chip.add_css_class("cat-chip")
            chip.append(Gtk.Label(label=icon))
            chip.append(Gtk.Label(label=cat))
            sw = Gtk.Switch(active=True, valign=Gtk.Align.CENTER)
            chip.append(sw)
            item = Gtk.FlowBoxChild()
            item.set_child(chip)
            item.set_focusable(False)
            flow.append(item)
            self.switches[cat] = sw

        box.append(cat_card)

        self.progress = Gtk.ProgressBar()
        self.progress.set_visible(False)
        self.progress.set_show_text(True)
        box.append(self.progress)

        self.btn_run = Gtk.Button(label="Organizar Pasta")
        self.btn_run.add_css_class("btn-filled")
        self.btn_run.set_sensitive(False)
        self.btn_run.connect("clicked", self.on_run)
        box.append(self.btn_run)

        return scroll

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: Settings
    # ─────────────────────────────────────────────────────────────────────────

    def _build_settings(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        title = Gtk.Label(label="Configurações")
        title.add_css_class("label-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        # ── APARÊNCIA ──
        theme_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        theme_card.add_css_class("md-card")
        theme_card.append(make_section_label("APARÊNCIA"))

        theme_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self._theme_radios = {}
        first_rb = None
        for mode, lbl in [("light", "☀ Claro"), ("auto", "⬤ Automático"), ("dark", "🌙 Escuro")]:
            rb = Gtk.CheckButton(label=lbl)
            if first_rb:
                rb.set_group(first_rb)
            else:
                first_rb = rb
            rb.set_active(self._cfg.get("theme", "auto") == mode)
            m = mode
            rb.connect("toggled", lambda b, mo=m: self._apply_theme(mo) if b.get_active() else None)
            theme_row.append(rb)
            self._theme_radios[mode] = rb
        theme_card.append(theme_row)
        box.append(theme_card)

        # ── ARQUIVOS ──
        def sw_row(key, label, sub=""):
            sw = Gtk.Switch(active=self._cfg.get(key, True))
            sw.connect("state-set", lambda s, v, k=key: (self._cfg.update({k: v}), cfg_save(self._cfg)))
            return make_row(label, sw, sub)

        files_card = make_card(
            make_section_label("ARQUIVOS"),
            sw_row("ignore_hidden", "Ignorar arquivos ocultos", "Arquivos com nome iniciando em '.'"),
            sw_row("ignore_system", "Ignorar arquivos do sistema", "Thumbs.db, .directory, desktop.ini…"),
            sw_row("ignore_temp",   "Ignorar arquivos temporários", ".tmp, .crdownload, .part, .lock…"),
        )
        box.append(files_card)

        # ── CONFLITO DE NOMES ──
        conflict_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        conflict_card.add_css_class("md-card")
        conflict_card.append(make_section_label("CONFLITO DE NOMES"))

        conflict_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self._conflict_radios = {}
        first_cr = None
        current_conflict = self._cfg.get("conflict", "rename")
        for val, lbl in [("rename", "Renomear"), ("skip", "Pular"), ("replace", "Substituir")]:
            rb = Gtk.CheckButton(label=lbl)
            if first_cr:
                rb.set_group(first_cr)
            else:
                first_cr = rb
            rb.set_active(current_conflict == val)
            v = val
            rb.connect("toggled", lambda b, vl=v: (
                self._cfg.update({"conflict": vl}), cfg_save(self._cfg)
            ) if b.get_active() else None)
            conflict_row.append(rb)
            self._conflict_radios[val] = rb

        conflict_card.append(conflict_row)
        warn = Gtk.Label(label="⚠ Substituir apaga o arquivo de destino permanentemente.")
        warn.set_halign(Gtk.Align.START)
        warn.add_css_class("label-sub")
        warn.set_wrap(True)
        warn.set_xalign(0)
        conflict_card.append(warn)
        box.append(conflict_card)

        # ── SEGURANÇA ──
        sec_card = make_card(
            make_section_label("SEGURANÇA"),
            sw_row("confirm_before_move", "Confirmar antes de mover",
                   "Exibe diálogo de confirmação a cada execução"),
            sw_row("use_trash", "Mover para Lixeira (reversível)",
                   "Requer 'send2trash' instalado"),
        )
        box.append(sec_card)

        # ── Windows (só se IS_WINDOWS) ──
        if IS_WINDOWS:
            win_card = make_card(
                make_section_label("WINDOWS"),
                sw_row("win_ignore_system", "Ignorar Thumbs.db, desktop.ini, autorun.inf"),
                sw_row("win_reserved", "Tratar nomes reservados (CON, PRN, AUX, NUL…)"),
            )
            box.append(win_card)

        # ── Avançado ──
        adv_btn = Gtk.Button(label="⚙  Avançado →")
        adv_btn.add_css_class("flat")
        adv_btn.set_halign(Gtk.Align.END)
        adv_btn.connect("clicked", lambda _: self._show_page("advanced"))
        box.append(adv_btn)

        # ── Sobre o app ──
        about_card = make_card(
            make_section_label("SOBRE O APP"),
            self._info_row("Versão", "1.0"),
            self._info_row("ID", "io.github.aleff959.Organito"),
            self._info_row("Licença", "MIT"),
        )
        box.append(about_card)

        return scroll

    def _info_row(self, label: str, value: str) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        l = Gtk.Label(label=label)
        l.add_css_class("label-sub")
        l.set_hexpand(True)
        l.set_halign(Gtk.Align.START)
        v = Gtk.Label(label=value)
        v.add_css_class("sys-value")
        v.set_halign(Gtk.Align.END)
        v.set_selectable(True)
        row.append(l)
        row.append(v)
        return row

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: Advanced Settings
    # ─────────────────────────────────────────────────────────────────────────

    def _build_advanced(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        back_btn = Gtk.Button(label="← Configurações")
        back_btn.add_css_class("flat")
        back_btn.set_halign(Gtk.Align.START)
        back_btn.connect("clicked", lambda _: self._show_page("settings"))
        box.append(back_btn)

        title = Gtk.Label(label="Avançado")
        title.add_css_class("label-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        def sw(key, label, sub=""):
            s = Gtk.Switch(active=self._cfg.get(key, False))
            s.connect("state-set", lambda w, v, k=key: (self._cfg.update({k: v}), cfg_save(self._cfg)))
            return make_row(label, s, sub)

        # ── Simulação ──
        box.append(make_card(
            make_section_label("SIMULAÇÃO"),
            sw("dry_run", "Dry run (simular sem mover)",
               "Mostra o que seria feito sem mover nenhum arquivo"),
        ))

        # ── Subpastas ──
        rec_sw = Gtk.Switch(active=self._cfg.get("recursive", False))
        rec_sw.connect("state-set", lambda w, v: (self._cfg.update({"recursive": v}), cfg_save(self._cfg)))

        depth_spin = Gtk.SpinButton.new_with_range(1, 10, 1)
        depth_spin.set_value(self._cfg.get("max_depth", 1))
        depth_spin.connect("value-changed", lambda s: (
            self._cfg.update({"max_depth": int(s.get_value())}), cfg_save(self._cfg)
        ))

        box.append(make_card(
            make_section_label("SUBPASTAS"),
            make_row("Processar recursivamente", rec_sw,
                     "⚠ Move arquivos de subpastas existentes também"),
            make_row("Profundidade máxima", depth_spin),
        ))

        # ── Filtros de tamanho ──
        def size_spin(key, default=0):
            sp = Gtk.SpinButton.new_with_range(0, 99999, 1)
            sp.set_value(self._cfg.get(key, default))
            sp.connect("value-changed", lambda s, k=key: (
                self._cfg.update({k: int(s.get_value())}), cfg_save(self._cfg)
            ))
            return sp

        box.append(make_card(
            make_section_label("FILTROS DE TAMANHO (KB)"),
            make_row("Tamanho mínimo (0 = sem limite)", size_spin("min_size")),
            make_row("Tamanho máximo (0 = sem limite)", size_spin("max_size")),
        ))

        # ── Desempenho ──
        max_files_spin = Gtk.SpinButton.new_with_range(0, 99999, 10)
        max_files_spin.set_value(self._cfg.get("max_files", 0))
        max_files_spin.connect("value-changed", lambda s: (
            self._cfg.update({"max_files": int(s.get_value())}), cfg_save(self._cfg)
        ))

        delay_spin = Gtk.SpinButton.new_with_range(0, 5000, 10)
        delay_spin.set_value(self._cfg.get("move_delay_ms", 0))
        delay_spin.connect("value-changed", lambda s: (
            self._cfg.update({"move_delay_ms": int(s.get_value())}), cfg_save(self._cfg)
        ))

        box.append(make_card(
            make_section_label("DESEMPENHO"),
            make_row("Limite de arquivos (0 = sem limite)", max_files_spin),
            make_row("Pausa entre movimentos (ms)", delay_spin,
                     "Útil em SSDs com muita escrita simultânea"),
        ))

        # ── Log ──
        log_sw = Gtk.Switch(active=self._cfg.get("log_enabled", False))
        log_sw.connect("state-set", lambda w, v: (
            self._cfg.update({"log_enabled": v}), cfg_save(self._cfg)
        ))

        log_entry = Gtk.Entry()
        log_entry.set_text(self._cfg.get("log_path", ""))
        log_entry.set_hexpand(True)
        log_entry.connect("changed", lambda e: (
            self._cfg.update({"log_path": e.get_text()}), cfg_save(self._cfg)
        ))

        box.append(make_card(
            make_section_label("LOG"),
            make_row("Salvar log das operações", log_sw),
            make_row("Local do log", log_entry),
        ))

        # ── Windows avançado (só se IS_WINDOWS) ──
        if IS_WINDOWS:
            long_sw = Gtk.Switch(active=self._cfg.get("win_long_paths", False))
            long_sw.connect("state-set", lambda w, v: (
                self._cfg.update({"win_long_paths": v}), cfg_save(self._cfg)
            ))
            box.append(make_card(
                make_section_label("WINDOWS — AVANÇADO"),
                make_row("Habilitar caminhos longos (>260 chars)", long_sw,
                         "Requer configuração no registro do Windows"),
            ))

        return scroll

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: System Info
    # ─────────────────────────────────────────────────────────────────────────

    def _build_system(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        title = Gtk.Label(label="Sistema")
        title.add_css_class("label-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        # Carregar dados em thread
        loading = Gtk.Label(label="Carregando informações…")
        loading.add_css_class("label-sub")
        box.append(loading)

        def load_and_fill():
            info = sysinfo.get_info()
            GLib.idle_add(self._fill_sysinfo, box, loading, info)

        threading.Thread(target=load_and_fill, daemon=True).start()
        return scroll

    def _fill_sysinfo(self, box, loading_lbl, info):
        box.remove(loading_lbl)

        def ir(label, value):
            return self._info_row(label, str(value))

        def bar_row(label, percent):
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            lbl_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            l = Gtk.Label(label=label)
            l.add_css_class("label-sub")
            l.set_hexpand(True)
            l.set_halign(Gtk.Align.START)
            p = Gtk.Label(label=f"{percent:.0f}%")
            p.add_css_class("label-sub")
            lbl_row.append(l)
            lbl_row.append(p)
            bar = Gtk.ProgressBar()
            bar.set_fraction(min(percent / 100.0, 1.0))
            bar.add_css_class("bar-mini")
            vbox.append(lbl_row)
            vbox.append(bar)
            return vbox

        # OS
        box.append(make_card(
            make_section_label("SISTEMA OPERACIONAL"),
            ir("Sistema",       info.get("os_name", "—")),
            ir("Kernel",        info.get("kernel", "—")),
            ir("Arquitetura",   info.get("arch", "—")),
            ir("Desktop",       info.get("desktop", "—")),
            ir("Sessão",        info.get("session", "—")),
            ir("Hostname",      info.get("hostname", "—")),
        ))

        # Hardware
        box.append(make_card(
            make_section_label("HARDWARE"),
            ir("Modelo",        info.get("hw_model", "—")),
            ir("Processador",   info.get("cpu_model", "—")),
            ir("Núcleos lógicos",  info.get("cpu_cores", "—")),
            ir("Núcleos físicos",  info.get("cpu_physical", "—")),
        ))

        # RAM
        ram_card = make_card(
            make_section_label("MEMÓRIA RAM"),
            ir("Total",         info.get("ram_total", "—")),
            ir("Disponível",    info.get("ram_avail", "—")),
            bar_row("Uso",      info.get("ram_percent", 0)),
        )
        box.append(ram_card)

        # Disco
        disk_card = make_card(
            make_section_label("ARMAZENAMENTO"),
            ir("Total",         info.get("disk_total", "—")),
            ir("Livre",         info.get("disk_free", "—")),
            bar_row("Uso",      info.get("disk_percent", 0)),
        )
        box.append(disk_card)

        # App / Runtime
        box.append(make_card(
            make_section_label("APLICATIVO / RUNTIME"),
            ir("Organito",      info.get("app_version", "—")),
            ir("Python",        info.get("python_version", "—")),
            ir("GTK",           info.get("gtk_version", "—")),
            ir("libadwaita",    info.get("adw_version", "—")),
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: Help
    # ─────────────────────────────────────────────────────────────────────────

    def _build_help(self):
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(20)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        title = Gtk.Label(label="Como usar")
        title.add_css_class("label-title")
        title.set_halign(Gtk.Align.START)
        box.append(title)

        steps = [
            ("1", "Selecione a pasta",
             "Toque em Selecionar e escolha a pasta que deseja organizar."),
            ("2", "Escolha as categorias",
             "Ative ou desative cada tipo. Use Ativar todos / Limpar todos para agilizar."),
            ("3", "Organize",
             "Clique em Organizar Pasta. Os arquivos vão para subpastas dentro da pasta escolhida."),
            ("4", "Acompanhe o progresso",
             "A barra mostra quantos arquivos já foram processados em tempo real."),
            ("5", "Pronto",
             "Arquivos sem tipo reconhecido ficam no lugar. Nomes duplicados ganham sufixo automático."),
        ]
        for num, t, d in steps:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
            row.set_valign(Gtk.Align.START)
            n = Gtk.Label(label=num)
            n.set_css_classes(["label-title"])
            n.set_valign(Gtk.Align.START)
            n.set_margin_top(2)
            row.append(n)
            txt = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            txt.set_hexpand(True)
            tl = Gtk.Label()
            tl.set_markup(f"<b>{t}</b>")
            tl.set_css_classes(["label-body"])
            tl.set_halign(Gtk.Align.START)
            dl = Gtk.Label(label=d)
            dl.set_css_classes(["label-sub"])
            dl.set_halign(Gtk.Align.START)
            dl.set_wrap(True)
            dl.set_xalign(0)
            txt.append(tl)
            txt.append(dl)
            row.append(txt)
            card = make_card(row, spacing=0)
            box.append(card)

        note = Gtk.Label(label="⚠ Apenas arquivos na raiz da pasta são processados por padrão. Ative Processar recursivamente em Configurações → Avançado para incluir subpastas.")
        note.set_wrap(True)
        note.set_xalign(0)
        note.add_css_class("label-sub")
        nc = Gtk.Box()
        nc.add_css_class("md-card-tonal")
        nc.append(note)
        box.append(nc)

        return scroll

    # ─────────────────────────────────────────────────────────────────────────
    # PAGE: About
    # ─────────────────────────────────────────────────────────────────────────

    def _build_about(self):
        dlg_trigger = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        # Usa Adw.AboutWindow nativo
        def open_about():
            dlg = Adw.AboutWindow()
            dlg.set_application_name("Organito")
            dlg.set_version("1.0")
            dlg.set_developer_name("aleff959")
            dlg.set_license_type(Gtk.License.MIT_X11)
            dlg.set_comments(
                "Sua pasta de Downloads não deveria parecer um depósito.\n"
                "Arquivos têm tipos, tipos têm lugar.\n"
                "Sem nuvem, sem rastreamento — só organização local e rápida."
            )
            dlg.set_application_icon("system-file-manager")
            dlg.set_transient_for(self)
            dlg.present()

        # Página Sobre como conteúdo inline + botão
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        clamp = Adw.Clamp()
        clamp.set_maximum_size(500)
        scroll.set_child(clamp)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        box.set_margin_top(40)
        box.set_margin_bottom(24)
        box.set_margin_start(16)
        box.set_margin_end(16)
        clamp.set_child(box)

        icon_lbl = Gtk.Label(label="🗂")
        icon_lbl.set_halign(Gtk.Align.CENTER)
        attrs = Pango.AttrList()
        attrs.insert(Pango.AttrSize.new(56 * Pango.SCALE))
        icon_lbl.set_attributes(attrs)
        box.append(icon_lbl)

        name_lbl = Gtk.Label(label="Organito")
        name_lbl.add_css_class("label-title")
        name_lbl.set_halign(Gtk.Align.CENTER)
        attrs2 = Pango.AttrList()
        attrs2.insert(Pango.AttrSize.new(32 * Pango.SCALE))
        name_lbl.set_attributes(attrs2)
        box.append(name_lbl)

        ver = Gtk.Label(label="Versão 1.0")
        ver.add_css_class("label-sub")
        ver.set_halign(Gtk.Align.CENTER)
        box.append(ver)

        box.append(Gtk.Separator())

        phil = ("Sua pasta de Downloads não deveria parecer um depósito. "
                "Arquivos têm tipos, tipos têm lugar. "
                "Sem configuração complexa, sem nuvem, sem rastreamento — "
                "apenas organização local, rápida e reversível.")
        phil_lbl = Gtk.Label(label=phil)
        phil_lbl.set_wrap(True)
        phil_lbl.set_xalign(0)
        phil_lbl.add_css_class("label-sub")
        phil_card = Gtk.Box()
        phil_card.add_css_class("md-card")
        phil_card.append(phil_lbl)
        box.append(phil_card)

        meta_card = make_card(
            make_section_label("DETALHES"),
            self._info_row("ID",       "io.github.aleff959.Organito"),
            self._info_row("Licença",  "MIT"),
            self._info_row("Stack",    "Python · GTK4 · libadwaita"),
        )
        box.append(meta_card)

        more_btn = Gtk.Button(label="Ver informações completas")
        more_btn.add_css_class("btn-outlined")
        more_btn.set_halign(Gtk.Align.CENTER)
        more_btn.connect("clicked", lambda _: open_about())
        box.append(more_btn)

        return scroll

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _set_all_switches(self, state: bool):
        for sw in self.switches.values():
            sw.set_active(state)

    def _toast(self, msg):
        t = Adw.Toast.new(msg)
        t.set_timeout(4)
        self.toast_overlay.add_toast(t)

    # ── Folder select ─────────────────────────────────────────────────────────

    def on_select(self, btn):
        dialog = Gtk.FileDialog()
        dialog.set_title("Escolha uma pasta")
        dialog.select_folder(self, None, self.on_folder_selected)

    def on_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                self.selected_path = folder.get_path()
                self.folder_label.set_label(self.selected_path)
                self.folder_sublabel.set_label("Pasta selecionada ✓")
                self.btn_run.set_sensitive(True)
        except Exception:
            pass

    # ── Run ───────────────────────────────────────────────────────────────────

    def on_run(self, btn):
        if self._cfg.get("confirm_before_move", False):
            dlg = Adw.MessageDialog.new(self, "Confirmar organização",
                f"Mover arquivos em:\n{self.selected_path}")
            dlg.add_response("cancel", "Cancelar")
            dlg.add_response("ok", "Organizar")
            dlg.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
            dlg.connect("response", lambda d, r: self._start_run() if r == "ok" else None)
            dlg.present()
        else:
            self._start_run()

    def _start_run(self):
        self.btn_run.set_sensitive(False)
        self.progress.set_visible(True)
        self.progress.set_fraction(0.0)
        self.progress.set_text("Iniciando…")
        active = {cat: sw.get_active() for cat, sw in self.switches.items()}
        opts = {
            "ignore_hidden":      self._cfg.get("ignore_hidden", True),
            "ignore_system":      self._cfg.get("ignore_system", True),
            "ignore_temp":        self._cfg.get("ignore_temp", True),
            "conflict":           self._cfg.get("conflict", "rename"),
            "dry_run":            self._cfg.get("dry_run", False),
            "recursive":          self._cfg.get("recursive", False),
            "max_depth":          self._cfg.get("max_depth", 1),
            "min_size":           self._cfg.get("min_size", 0) * 1024,
            "max_size":           self._cfg.get("max_size", 0) * 1024,
            "max_files":          self._cfg.get("max_files", 0),
            "move_delay_ms":      self._cfg.get("move_delay_ms", 0),
            "use_trash":          self._cfg.get("use_trash", False),
            "win_reserved":       self._cfg.get("win_reserved", True),
            "win_long_paths":     self._cfg.get("win_long_paths", False),
            "log_enabled":        self._cfg.get("log_enabled", False),
            "log_path":           self._cfg.get("log_path", ""),
        }
        threading.Thread(target=self._run_bg, args=(active, opts), daemon=True).start()

    def _run_bg(self, active, opts):
        try:
            delay = opts.pop("move_delay_ms", 0)
            import time

            original_move = __import__("shutil").move
            if delay > 0:
                import shutil as _sh
                def slow_move(src, dst):
                    time.sleep(delay / 1000.0)
                    return original_move(src, dst)
                _sh.move = slow_move

            def update(current, total):
                frac = current / total if total > 0 else 0
                GLib.idle_add(self.progress.set_fraction, frac)
                GLib.idle_add(self.progress.set_text, f"{current} / {total}")

            result = organize_directory(self.selected_path, active, opts, update)

            if delay > 0:
                import shutil as _sh
                _sh.move = original_move

            GLib.idle_add(self._on_done, result)
        except Exception as e:
            GLib.idle_add(self._on_done, {"moved": 0, "skipped": 0, "errors": [str(e)]})

    def _on_done(self, result):
        self.progress.set_visible(False)
        self.btn_run.set_sensitive(True)
        moved   = result.get("moved", 0)
        skipped = result.get("skipped", 0)
        errors  = result.get("errors", [])
        dry     = self._cfg.get("dry_run", False)

        if errors:
            self._toast(f"⚠ {len(errors)} erro(s). {moved} movidos.")
        elif dry:
            self._toast(f"🔍 Dry run: {moved} seriam movidos, {skipped} pulados.")
        else:
            self._toast(f"✓ {moved} arquivo(s) organizados, {skipped} pulados.")
        self.folder_sublabel.set_label(f"Última execução: {moved} movidos, {skipped} pulados")
