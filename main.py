import flet as ft
from threading import Thread
import threading
from bs4 import BeautifulSoup
import win32api
import requests
from win32api import GetSystemMetrics
global close
from time import sleep
close = False
def scrap():
    global t, close
    while (close == False):
        global t, page, schedule_widget,schedule_main_widget, schedule_mainest_widget
        if t.selected_index ==0:
            url = 'https://www.fcbarcelona.com/en/football/first-team/schedule'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')


            #### Dates ##### 
            dates_tag = soup.find_all("div", class_="fixture-result-list__fixture-date")
            dates=[]
                            
            for date in dates_tag:
                dates.append(date.text.strip().replace("\n", ""))


            #### Time of Matches ####
            times_tag = soup.find_all("div", class_="fixture-info__time")
            times=[]
                            
            for time in times_tag:
                times.append(time.text.strip().replace("\n", ""))



            #### Name of Competition #####
            competition_names_tag = soup.find_all("span", class_="fixture-result-list__name visually-hidden")
            competition_names=[]
                            
            for competition_name in competition_names_tag:
                competition_names.append(competition_name.text.strip().replace("\n", ""))



            ##### Match Day Number  #####
            matchdays_tag = soup.find_all("div", class_="fixture-result-list__stage")
            matchdays=[]
                            
            for matchday in matchdays_tag:
                matchdays.append(matchday.text.strip().replace("\n", ""))



            ##### Name of Home Team ####
            home_names_tag = soup.find_all("div", class_="fixture-info__name fixture-info__name--home")
            home_names=[]
                            
            for home_name in home_names_tag:
                home_names.append(home_name.text.strip().replace("\n", ""))



            ##### Name of Away Team ####
            away_names_tag = soup.find_all("div", class_="fixture-info__name fixture-info__name--away")
            away_names=[]
                            
            for away_name in away_names_tag:
                away_names.append(away_name.text.strip().replace("\n", ""))



            ##### Logo of Home Team
            home_logo_divs=soup.find_all('div',{"class":"fixture-info__badge fixture-info__badge--home"})
            home_logo=[]

            for home_logo_div in home_logo_divs:
                home_logo.append(home_logo_div.find('img').attrs['srcset'].split(",")[1].replace("2x",""))


            ##### Logo of Away Team
            away_logo_divs=soup.find_all('div',{"class":"fixture-info__badge fixture-info__badge--away"})
            away_logo=[]

            for away_logo_div in away_logo_divs:
                away_logo.append(away_logo_div.find('img').attrs['srcset'].split(",")[1].replace("2x",""))

            
            schedule_widget.controls.clear()
            schedule_widget.controls.append(ft.Text(""))

            for x in range(len(home_names)):
                match = ft.Container(content=
                    ft.Row ([
                        ft.Text(f"{home_names[x]} v/s {away_names[x]}   |  "),
                        ft.Text(f"{dates[x]} | {times[x]}")
                    ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding = ft.padding.only(30,10,30,10),
                    width=GetSystemMetrics(0)-300,
                    border_radius=10,
                    border = ft.border.all(3, ft.colors.GREY)
                )
                schedule_widget.controls.append(match)
                
            schedule_widget.update()

def main(page: ft.Page):
    global t, thread2, close, schedule_widget, schedule_main_widget,schedule_mainest_widget
    page.title = "F.C. Barcelona - Manas Sujal"
    page.window.width= GetSystemMetrics(0)-50
    page.window.height= GetSystemMetrics(1)-70
    page.theme_mode = ft.ThemeMode.DARK
    
    def handle_window_event(e):
        if e.data == "close":
            page.window.visible = False
            page.update()
            page.window.destroy()
            page.update()
            global close
            close = True
            
    page.window.prevent_close = True
    page.window.on_event = handle_window_event
    page.fonts={
            "Kippax Modern" : "fonts/barselona.ttf",
        }
    top_column=ft.Container(#begin=ft.alignment.center_left , end=ft.alignment.center_left
        gradient=ft.RadialGradient(radius = 5.8, colors=["#680630", "#06167D"]),
        content=ft.Column(controls=[
            ft.Text(""),
            ft.Row([
                ft.Image(
                    src="assets/images/logo.png",
                    width=100,
                    height=100,
                    fit=ft.ImageFit.CONTAIN,
                ),
                ft.Text("     "),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "F.C. Barcelona",
                            ft.TextStyle(
                                size=55,
                                decoration=ft.TextDecoration.UNDERLINE
                                ))], font_family="Kippax Modern"),
                ft.Text("     "),
                ft.Image(
                    src=f"assets/images/logo.png",
                    width=100,
                    height=100,
                    fit=ft.ImageFit.CONTAIN,
                ),

                        
                ],alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(""),
            ]))
    schedule_widget = ft.Column(controls=[ft.Text("")])
    schedule_main_widget = ft.Row([schedule_widget],alignment=ft.MainAxisAlignment.CENTER)
    schedule_mainest_widget = ft.Column(controls=[schedule_main_widget],scroll=ft.ScrollMode.ALWAYS)
    page.update()
    
    t = ft.Tabs(                
                tab_alignment=ft.TabAlignment.CENTER,
                selected_index=0,
                animation_duration=0,
                indicator_color = "#680630",
                label_text_style=ft.TextStyle(
                                size=20,
                                font_family="Kippax Modern"),
                label_color="#0c2bf5",
                unselected_label_color="#c20757",
                
                tabs=[
                    ft.Tab(text="     Fixtures     ", content=ft.Container(content=schedule_mainest_widget)),       
                        
                    ft.Tab(text="     Results     "),

                    ft.Tab(text="     Tables     "),

                    ft.Tab(text="     Players     "),
                ],
            )   
    page.add(
        ft.Column([
            ft.Container(content=top_column),
            ft.Container(content=t, bgcolor="#061831"),
        ], spacing=0)
        )
        
    thread2 = threading.Thread(target=scrap)
    thread2.start()
    
ft.app(target=main, assets_dir="assets")


