import customtkinter as ctk


class NavigationManager:

    def __init__(self, container):
        self.container = container
        self.pages = {}
        self.current_page = None

    def register(self, name: str, page):

        #Register a page using a unique name.

        self.pages[name] = page

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        page.grid_remove()

    def show(self, name: str):

        # Display one registered page and hide the others.

        if name not in self.pages:
            raise ValueError(f"Unknown page: {name}")

        if self.current_page == name:
            return

        if self.current_page is not None:
            self.pages[self.current_page].grid_remove()

        self.pages[name].grid()

        self.current_page = name