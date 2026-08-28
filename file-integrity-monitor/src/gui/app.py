import customtkinter as ctk
from tkinterdnd2 import TkinterDnD

from .theme import APP_BG, PANEL_BG, BORDER
from .navigation import NavigationManager
from .components.sidebar import Sidebar
from .pages.dashboard import DashboardPage
from .pages.monitoring import MonitoringPage
from .pages.incidents.page import IncidentsPage
from .pages.reports.page import ReportsPage
from .pages.settings import SettingsPage


class FIMApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        TkinterDnD._require(self)

        self.title("File Integrity Monitor")
        self.geometry("1280x760")
        self.minsize(1000, 650)
        self.configure(fg_color=APP_BG)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self, self._navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content = ctk.CTkFrame(
            self,
            fg_color=PANEL_BG,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.navigation = NavigationManager(self.content)

        pages = {
            "dashboard": DashboardPage(self.content),
            "monitoring": MonitoringPage(self.content),
            "incidents": IncidentsPage(self.content),
            "reports": ReportsPage(self.content),
            "settings": SettingsPage(self.content),
        }

        for name, page in pages.items():
            self.navigation.register(name, page)

        self.navigation.show("dashboard")

    def _navigate(self, page_name):
        self.navigation.show(page_name)


def run():
    app = FIMApplication()
    app.mainloop()