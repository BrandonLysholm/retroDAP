# This code is a mess.
# This is me learning Python as I go.
# This is not how I write code for my day job.

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

def flattenAlpha(img):
    global SCALE
    [img_w, img_h] = img.size
    img = img.resize((int(img_w * SCALE), int(img_h * SCALE)))
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 50  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(255)  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))

    img.putalpha(mask)

    return img





# Single function that is the callback function for the class FullEncoder, which handles all input
# logic for my clickwheel
def processMyInput(myVal):
    if myVal == "center":
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
e1 = FullEncoder(ENC1_PIN, ENC2_PIN, CENTER_BTN_PIN, DOWN_BTN_PIN, RIGHT_BTN_PIN, UP_BTN_PIN, LEFT_BTN_PIN, processMyInput)

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