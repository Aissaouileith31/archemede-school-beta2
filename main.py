import flet as ft
from app_file.pages.login import login
from app_file.pages.home_page import home

def main_location(page: ft.Page):

    def route_change(e):
        page.clean()
        print("🔄 Route changed to:", page.route)

        try:
            if page.route == "/":
                # If already logged in → go directly home
                if page.client_storage.get("logged_in") == "yes":
                    print(f'user allredy log in username')
                    return page.go("/home")

                login(page)

            elif page.route == "/home":
                username = page.client_storage.get("username")

                if page.client_storage.get("logged_in") != "yes":
                    print("⚠️ Not logged in → redirect to login")
                    return page.go("/")

                home(page, username)

            else:
                page.add(ft.Text("404: Page not found"))

        except Exception as ex:
            print("Error:", ex)

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main_location, assets_dir="assets/")
