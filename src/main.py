#!/usr/bin/env python3
import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

from ui import OrganitoWindow


class OrganitoApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.github.aleff959.Organito")

    def do_activate(self):
        win = self.get_active_window()
        if not win:
            win = OrganitoWindow(application=self)
        win.present()


if __name__ == "__main__":
    sys.exit(OrganitoApp().run(sys.argv))
