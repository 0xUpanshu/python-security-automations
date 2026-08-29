import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .theme import APP_BG, PANEL_BG, BORDER
from .navigation import NavigationManager
from .components.sidebar import Sidebar
from .pages.dashboard.page import DashboardPage
from .pages.monitoring.page import MonitoringPage
from .pages.incidents.page import IncidentsPage
from .pages.reports.page import ReportsPage
from .pages.settings.page import SettingsPage


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def _handle(self, event):
        if not event.is_directory:
            self.callback()

    def on_created(self, event):
        self._handle(event)

    def on_modified(self, event):
        self._handle(event)

    def on_deleted(self, event):
        self._handle(event)

    def on_moved(self, event):
        self._handle(event)


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

        self.sidebar = Sidebar(
            self,
            self._navigate,
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

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

        self.pages = {
            "dashboard": DashboardPage(
                self.content
            ),
            "monitoring": MonitoringPage(
                self.content
            ),
            "incidents": IncidentsPage(
                self.content
            ),
            "reports": ReportsPage(
                self.content
            ),
            "settings": SettingsPage(
                self.content
            ),
        }

        for name, page in self.pages.items():
            self.navigation.register(
                name,
                page,
            )

        self.navigation.show("dashboard")

        self.current_page = "dashboard"
        self.sidebar.set_active(
            "dashboard"
        )

        self.observer = None
        self.refresh_job = None
        self.folder_check_job = None
        self.watched_folders = set()

        self._start_watcher()
        self._check_folders()

        self.protocol(
            "WM_DELETE_WINDOW",
            self._close,
        )

    def _navigate(self, page_name):
        self.current_page = page_name

        self.navigation.show(
            page_name
        )

        self.sidebar.set_active(
            page_name
        )

        page = self.pages.get(page_name)

        if page and hasattr(
            page,
            "refresh",
        ):
            page.refresh()

    def _get_monitored_folders(self):
        try:
            monitoring_page = self.pages[
                "monitoring"
            ]

            return set(
                monitoring_page.service.get_folders()
            )

        except Exception:
            return set()

    def _start_watcher(self):
        self._stop_watcher()

        folders = (
            self._get_monitored_folders()
        )

        if not folders:
            self.watched_folders = set()
            return

        self.observer = Observer()

        handler = FileChangeHandler(
            self._on_file_change
        )

        for folder in folders:
            try:
                self.observer.schedule(
                    handler,
                    folder,
                    recursive=True,
                )
            except Exception:
                continue

        self.observer.start()

        self.watched_folders = folders

    def _stop_watcher(self):
        if self.observer is None:
            return

        self.observer.stop()
        self.observer.join(
            timeout=2
        )
        self.observer = None

    def _on_file_change(self):
        if self.refresh_job is not None:
            self.after_cancel(
                self.refresh_job
            )

        self.refresh_job = self.after(
            700,
            self._process_file_change,
        )

    def _process_file_change(self):
        self.refresh_job = None

        try:
            service = (
                self.pages[
                    "monitoring"
                ].service
            )

            if service.baseline_exists():
                service.scan()

            self._refresh_pages()

        except Exception:
            self._refresh_pages()

    def _refresh_pages(self):
        for page in self.pages.values():
            if hasattr(
                page,
                "refresh",
            ):
                try:
                    page.refresh()
                except Exception:
                    pass

    def _check_folders(self):
        current_folders = (
            self._get_monitored_folders()
        )

        if current_folders != self.watched_folders:
            self._start_watcher()

        self.folder_check_job = self.after(
            1000,
            self._check_folders,
        )

    def _close(self):
        if self.refresh_job is not None:
            self.after_cancel(
                self.refresh_job
            )

        if self.folder_check_job is not None:
            self.after_cancel(
                self.folder_check_job
            )

        self._stop_watcher()
        self.destroy()


def run():
    app = FIMApplication()
    app.mainloop()