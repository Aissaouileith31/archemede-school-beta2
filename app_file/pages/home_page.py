import flet as ft
import json
import time
import httpx

# 🔗 GitHub JSON link
message_url_from_github = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/messege.json"
crenau_url_from_github = "https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/crenau.json"
def home(page: ft.Page, username):
    # Import font
    page.fonts = {"Koulen": r"font\\koulen\\Koulen-Regular.ttf"}
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
   # Page setup
    page.title = "Archemede School"
    page.bgcolor = "#C0DA4A"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
    # 🔹 Function to load and filter messages
    def load_messages():
        try:
            url = f"https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/messege.json?nocache={int(time.time())}"
            with httpx.Client(timeout=5) as client:
                response = client.get(url, headers={"Cache-Control": "no-cache"})
                response.raise_for_status()
                data = response.json()
                return [msg for msg in data if msg.get("receiver") in (username, "all")]
        except Exception as e:
            print("Error loading messages:", e)
        return []

    def load_crenau():
        try:
            url = f"https://raw.githubusercontent.com/Aissaouileith31/school_data3/refs/heads/main/crenau.json?nocache={int(time.time())}"
            with httpx.Client(timeout=5) as client:
                response = client.get(url, headers={"Cache-Control": "no-cache"})
                response.raise_for_status()
                data = response.json()
                return [c for c in data if c.get("resiver_user") == username]
        except Exception as e:
            print("Error loading crenau:", e)
        return []
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
    
        
        #for now using it localy after using github as serve
    
        


#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
    # 🔹 Build UI
    def build_ui():
        page.clean()
        w = page.width
        h = page.height

        # Green background ellipse
        ellipse = ft.Container(
            width=w * 0.7,
            height=h * 1.2,
            bgcolor="#0C6D26",
            border_radius=w,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=-h * 0.15),
        )

        # Title
        title = ft.Text(
            "ARCHEMEDE SCHOOL",
            weight="bold",
            color="white",
            size=w * 0.08 if w < 600 else 35,
            font_family="Koulen",
            text_align="center",
            width=w * 0.8,
        )

        # White line
        line = ft.Container(width=w * 0.7, height=3, bgcolor="white")


       
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________


        info = load_crenau()
        if not info:
            crenau_list = [
                ft.Container(
                    content=ft.Text("pas crenau a ete trouve", color="black", size=16),
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    margin=10,
                    alignment=ft.alignment.center,
                )
            ]
        else:
            crenau_list= []
            for inf in info:


                
                creanu_box = ft.Container(
                    bgcolor="white",
                    border_radius=12,
                    padding=12,
                    margin=ft.margin.symmetric(vertical=6, horizontal=10),
                    content=ft.Column(
                        [
                            ft.Text(
                                f"""creanu: {inf.get("matier","pas info")} 
                                """,
                                color="#0C6D26",
                                size=14,
                                weight="bold",
                            ),
                            ft.Text(
                                f"""
                                date de inscription: {inf.get("date_de_iscription","pas info")}
                                jour: {inf.get("jour","pas info")}
                                temp: 
                                debu: {inf.get("debu","pas info")} 
                                fin: {inf.get("fin","pas info")}
                                nombre de cour: {inf.get("nbr_cour","pas info")}
                                expire: {inf.get("expire","pas info")}
                                
                                """,
                                color="black",
                                size=16,
                            ),
                        ],
                        spacing=4,
                    ),
                )
                crenau_list.append(creanu_box)

        

        messages = load_messages()
 
        # If no messages
        if not messages:
            message_list = [
                ft.Container(
                    content=ft.Text("📭 No messages found.", color="black", size=16),
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    margin=10,
                    alignment=ft.alignment.center,
                )
            ]
        else:
            message_list = []
            for msg in messages:
                student_info = ft.Container(
                content=ft.Column([
                    ft.Text(f"nom & prenom :{msg.get("nom_complet","pas info")}"),
                    ft.Text(f"id de eleve :{msg.get("id","pas info")}"),
                    ft.Text(f"nom de utilisateur :{username}"),

                        ])
                    )
                message_box = ft.Container(
                    bgcolor="white",
                    border_radius=12,
                    padding=12,
                    margin=ft.margin.symmetric(vertical=6, horizontal=10),
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Administrator le: {msg.get("date","pas date")} type de message: {msg.get("type_de_message","pas type")}",
                                color="#0C6D26",
                                size=14,
                                weight="bold",
                            ),
                            ft.Text(
                                msg.get("message", "No message content."),
                                color="black",
                                size=16,
                            ),
                        ],
                        spacing=4,
                    ),
                )
                message_list.append(message_box)
            message_list.reverse()#wi will make the list reverst to put the nwe messege on the top and the oldes onr to the down 
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________
#__________________________________________________________________

        # Create message list view
        messages_view = ft.ListView(
            controls=message_list,
            spacing=10,
            expand=True,
            
        )

        # Second tab: crenau
        crenau_view = ft.ListView(
            controls=crenau_list,
            spacing=10,
            expand=True,
            
        )
        def logout(e):
            page.client_storage.clear()
            page.client_storage.set("logged_in", "no")
            return page.go('/')
        
        setting = []
        
        setting_box = ft.ElevatedButton(
                'deconecter',
                bgcolor='#E1E645',
                color="black",
                on_click=logout,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    shadow_color="black",
                    elevation=6,

                ),
                expand=True)
                
        setting.append(setting_box)

        setting_vue = ft.ListView(
            controls=setting,
            spacing=10,
            expand=True,
            
        )



        # Tabs widget
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Messages", icon=ft.Icons.MESSAGE, content=messages_view),
                ft.Tab(text="séances & coure", icon=ft.Icons.BOOK, content=crenau_view),
                ft.Tab(text="parametre", icon=ft.Icons.SETTINGS, content=setting_vue),
            ],
            expand=1,
        )



        # Green box container with tabs
        green_box = ft.Container(
            width=w,
            height=500 if h > 600 else 400,
            bgcolor="#27943E",
            margin=ft.margin.only(0, 30),
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=10, color=ft.Colors.BLACK26),
            border_radius=10,
            padding=15,
            content=tabs,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        # Combine all UI
        page.add(
            ft.Stack(
                [
                    ft.Container(content=ellipse, alignment=ft.alignment.center),
                    ft.Column(
                        [
                            ft.Container(content=title, alignment=ft.alignment.center),
                            ft.Container(content=line, alignment=ft.alignment.center),
                            ft.Container(content=student_info, alignment=ft.alignment.center),
                            ft.Container(content=green_box, alignment=ft.alignment.center),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ]
            )
        )

    # Rebuild UI when resizing
    page.on_resize = lambda e: build_ui()
    

    build_ui()