import customtkinter as ctk

from .theme import (
    APP_BG,
    PANEL_BG,
    BORDER,
    TEXT_PRIMARY,
    FONT_FAMILY,
)

from .navigation import NavigationManager
from .components.sidebar import Sidebar

from .pages.dashboard import DashboardPage
from .pages.monitoring import MonitoringPage
from .pages.incidents import IncidentsPage
from .pages.reports import ReportsPage
from .pages.settings import SettingsPage


class FIMApplication(ctk.CTk):
    """
    Main CustomTkinter application window.
    """

    def __init__(self):
        super().__init__()

        self.title("File Integrity Monitor")

        self.geometry("1280x760")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(
            fg_color=APP_BG
        )

        self._configure_grid()
        self._build_sidebar()
        self._build_content()
        self._build_pages()

        self.navigation.show("dashboard")

    def _configure_grid(self):
        self.grid_rowconfigure(
            0,
            weight=1,
        )

        self.grid_columnconfigure(
            0,
            weight=0,
        )

        self.grid_columnconfigure(
            1,
            weight=1,
        )

    def _build_sidebar(self):
        self.sidebar = Sidebar(
            self,
            on_navigate=self._navigate,
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

    def _build_content(self):
        self.content = ctk.CTkFrame(
            self,
            fg_color=PANEL_BG,
            corner_radius=0,
            border_width=1,
            border_color=BORDER,
        )

        self.content.grid(
            row=0,
            column=1,
            padx=(0, 0),
            pady=0,
            sticky="nsew",
        )

        self.content.grid_rowconfigure(
            0,
            weight=1,
        )

        self.content.grid_columnconfigure(
            0,
            weight=1,
        )

        self.navigation = NavigationManager(
            self.content
        )

    def _build_pages(self):
        pages = {
            "dashboard": DashboardPage(self.content),
            "monitoring": MonitoringPage(self.content),
            "incidents": IncidentsPage(self.content),
            "reports": ReportsPage(self.content),
            "settings": SettingsPage(self.content),
        }

        for name, page in pages.items():
            self.navigation.register(
                name,
                page,
            )

    def _navigate(self, page_name: str):
        # Handle sidebar navigation

        self.navigation.show(page_name)
        self.sidebar.set_active(page_name)


def run():

    app = FIMApplication()
    app.mainloop()