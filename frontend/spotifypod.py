# This file gets called to start the application

import tkinter as tk 
import time
from datetime import timedelta
from tkinter import ttk
from view_model import *
from PIL import ImageTk, Image
from sys import platform
import os
from fullEncoder import FullEncoder
from my_tk_pages import tkinterApp, SearchFrame, Marquee, NowPlayingFrame, StartPage

# Setting all my pins as constants for easy changing
CENTER_BTN_PIN = 10
DOWN_BTN_PIN = 11
RIGHT_BTN_PIN = 7
UP_BTN_PIN = 15
LEFT_BTN_PIN = 16
ENC1_PIN = 32
ENC2_PIN = 33
HOLDSWITCH_PIN = 31


DIVIDER_HEIGHT = 3
SCREEN_TIMEOUT_SECONDS = 60

last_interaction = time.time()
screen_on = True

def screen_sleep():
    global screen_on
    screen_on = False
    os.system('xset -display :0 dpms force off')

def screen_wake():
    global screen_on
    screen_on = True
    os.system('xset -display :0 dpms force on')

# Single function that is the callback function for the class FullEncoder, which handles all input
# logic for my clickwheel
def processMyInput(myVal):
    if myVal == "locked":
        return
    elif myVal == "center":
        onSelectPressed()
    elif myVal == "down":
        onPlayPressed()
    elif myVal == "right":
        onNextPressed()
    elif myVal == "up":
        onBackPressed()
    elif myVal == "left":
        onPrevPressed()
    elif (myVal == 'L'):
        onUpPressed()
    elif (myVal == 'R'):
        onDownPressed()

    # TODO: Handle screen wakeup/sleep 


def onPlayPressed():
    global page, app
    page.nav_play()
    render(app, page.render())
    
def onSelectPressed():
    global page, app
    if (not page.has_sub_page):
        return
    page.render().unsubscribe()
    page = page.nav_select()
    render(app, page.render())

def onBackPressed():
    global page, app
    previous_page = page.nav_back()
    if (previous_page):
        page.render().unsubscribe()
        page = previous_page
        render(app, page.render())
    
def onNextPressed():
    global page, app
    page.nav_next()
    render(app, page.render())

def onPrevPressed():
    global page, app
    page.nav_prev()
    render(app, page.render())

def onUpPressed():
    global page, app
    page.nav_up()
    render(app, page.render())

def onDownPressed():
    global page, app
    page.nav_down()
    render(app, page.render())

def update_search(q, ch, loading, results):
    global app, page
    search_page = app.frames[SearchFrame]
    if (results is not None):
        page.render().unsubscribe()
        page = SearchResultsPage(page, results)
        render(app, page.render())
    else:
        search_page.update_search(q, ch, loading)

def render_search(app, search_render):
    app.show_frame(SearchFrame)
    search_render.subscribe(app, update_search)

def render_menu(app, menu_render):
    app.show_frame(StartPage)
    page = app.frames[StartPage]
    if(menu_render.total_count > MENU_PAGE_SIZE):
        page.show_scroll(menu_render.page_start, menu_render.total_count)
    else:
        page.hide_scroll()
    for (i, line) in enumerate(menu_render.lines):
        page.set_list_item(i, text=line.title, line_type = line.line_type, show_arrow = line.show_arrow) 
    page.set_header(menu_render.header, menu_render.now_playing, menu_render.has_internet)

def update_now_playing(now_playing):
    frame = app.frames[NowPlayingFrame]
    frame.update_now_playing(now_playing)

def render_now_playing(app, now_playing_render):
    app.show_frame(NowPlayingFrame)
    now_playing_render.subscribe(app, update_now_playing)

def render(app, render):
    if (render.type == MENU_RENDER_TYPE):
        render_menu(app, render)
    elif (render.type == NOW_PLAYING_RENDER):
        render_now_playing(app, render)
    elif (render.type == SEARCH_RENDER):
        render_search(app, render)

# Here we are going from defining functions to actually writing code to initialize the program
   
# Driver Code 
page = RootPage(None)
app = tkinterApp() 
render(app, page.render())
app.overrideredirect(True)
app.overrideredirect(False)

# Setting up my encoder
e1 = FullEncoder(ENC1_PIN, ENC2_PIN, CENTER_BTN_PIN, DOWN_BTN_PIN, RIGHT_BTN_PIN, UP_BTN_PIN, LEFT_BTN_PIN, HOLDSWITCH_PIN, processMyInput)

loop_count = 0

# This gets called last, so the app stays in this loop once everything is initialized
def app_main_loop():
    global app, page, loop_count, last_interaction, screen_on

    # TODO: Get sleep function working properly
    while true:
        if (time.time() - last_interaction > SCREEN_TIMEOUT_SECONDS and screen_on):
            screen_sleep()
        render(app, page.render())
       
app.after(5, app_main_loop)
app.mainloop()