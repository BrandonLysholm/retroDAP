import tkinter as tk 
import json
import time
from datetime import timedelta
from select import select
from tkinter import ttk
from view_model import *
from PIL import ImageTk, Image
from sys import platform
import os

# Setting up styles  
LARGEFONT =("ChicagoFLF", 90) 
MED_FONT =("ChicagoFLF", 70) 
SCALE = 1
SPOT_GREEN = "#1DB954"
SPOT_BLACK = "#191414"
SPOT_WHITE = "#FFFFFF"
DIVIDER_HEIGHT = 3

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


# using the python library tkinter too create the basis of the app (import tkinter as tk)  
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, *args, **kwargs):  
        global LARGEFONT, MED_FONT, SCALE
        # __init__ function for class Tk 
        tk.Tk.__init__(self, *args, **kwargs)

        if (platform == 'darwin'):
            self.geometry("320x240") # I am using the same screen resolution, so I should not have any issues with that
            SCALE = 0.3
        else:
            self.attributes('-fullscreen', True)
            SCALE = self.winfo_screenheight() / 930

        LARGEFONT =("ChicagoFLF", int(72 * SCALE))
        MED_FONT =("ChicagoFLF", int(52 * SCALE))
        # creating a container 
        container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) 
   
        # initializing frames to an empty array 
        self.frames = {}   
   
        # iterating through a tuple consisting 
        # of the different page layouts 
        for F in (StartPage, NowPlayingFrame, SearchFrame): 
   
            frame = F(container, self) 
   
            # initializing frame of that object from 
            # startpage, page1, page2 respectively with  
            # for loop 
            self.frames[F] = frame  
   
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(StartPage) 
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

# Used to create scrolling text
class Marquee(tk.Canvas):
    def __init__(self, parent, text, margin=2, borderwidth=0, relief='flat', fps=24):
        tk.Canvas.__init__(self, parent, highlightthickness=0, borderwidth=borderwidth, relief=relief, background=SPOT_BLACK)
        self.fps = fps
        self.margin = margin
        self.borderwidth = borderwidth
        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas. 
        self.saved_text = text
        self.text = self.create_text(0, -1000, text=text, font=LARGEFONT, fill=SPOT_GREEN, anchor="w", tags=("text",))
        (x0, y0, x1, y1) = self.bbox("text")
        self.width = (x1 - x0) + (2*margin) + (2*borderwidth)
        self.height = (y1 - y0) + (2*margin) + (2*borderwidth)
        self.configure(width=self.width, height=self.height)
        self.reset = True
        self.pause_ctr = 100
        self.after_id = None
        self.redraw()

    def set_text(self, text):
        if (self.saved_text == text):
            return
        self.saved_text = text
        self.itemconfig(self.text, text=text)
        (x0, y0, x1, y1) = self.bbox("text")
        self.width = (x1 - x0) + (2*self.margin) + (2*self.borderwidth)
        self.height = (y1 - y0) + (2*self.margin) + (2*self.borderwidth)
        self.configure(width=self.width, height=self.height)
        if (self.width > self.winfo_width()):
            self.coords("text", 100, self.winfo_height()/2)
        else:
            self.coords("text", (self.winfo_width() / 2) - (self.width / 2), self.winfo_height()/2)
        self.pause_ctr = 100
        self.reset = True
        self.redraw()

    def redraw(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        (x0, y0, x1, y1) = self.bbox("text")
        win_width = self.winfo_width()
        if win_width < 2:
            pass
        elif self.width < win_width:
            self.coords("text", (win_width / 2) - (self.width / 2), self.winfo_height()/2)
            return 
        elif x1 < 0 or y0 < 0 or self.reset:
            self.reset = False
            self.animating = True
            x0 = 20
            y0 = int(self.winfo_height()/2)
            self.pause_ctr = 100
            self.coords("text", x0, y0)
        elif self.pause_ctr > 0:
            self.pause_ctr = self.pause_ctr - 1
        else:
            self.move("text", -2, 0)
        self.after_id = self.after(int(1000/self.fps), self.redraw)
   
class SearchFrame(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.configure(bg=SPOT_BLACK)
        self.header_label = tk.Label(self, text ="Search", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.header_label.grid(sticky='we', padx=(0, 10))
        self.grid_columnconfigure(0, weight=1)
        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=(10, int(160 * SCALE)), padx=(10, 30))
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        self.query_label = tk.Label(contentFrame, text ="", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.letter_label= tk.Label(contentFrame, text ="a", font = LARGEFONT, background=SPOT_GREEN, foreground=SPOT_BLACK) 
        self.query_label.grid(row = 0, column = 0, sticky = "nsw", padx=(120,0))
        self.letter_label.grid(row = 0, column = 1, sticky = "nsw")
        contentFrame.grid_columnconfigure(1, weight=1)
        search_line = tk.Canvas(self)
        search_line.configure(bg=SPOT_GREEN, height=5, bd=0, highlightthickness=0, relief='ridge')
        search_line.grid(row = 3, column = 0, sticky ="we", pady=10, padx=120)
        self.loading_label = tk.Label(self, text ="", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_WHITE) 
        self.loading_label.grid(row = 4, column = 0, sticky ="we", pady=(int(100 * SCALE), 0))

    def update_search(self, query, active_char, loading):
        self.query_label.configure(text=query)
        self.letter_label.configure(text=active_char)
        loading_text = "Loading..." if loading else ""
        self.loading_label.configure(text=loading_text)

class NowPlayingFrame(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.inflated = False
        self.active = False
        self.update_time = False
        self.configure(bg=SPOT_BLACK)
        self.header_label = tk.Label(self, text ="Now Playing", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.header_label.grid(sticky='we', padx=(0, 10))
        self.grid_columnconfigure(0, weight=1)
        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=10, padx=(10, 30))
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        contentFrame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.context_label = tk.Label(contentFrame, text ="", font = MED_FONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.context_label.grid(row=0, column=0,sticky ="w", padx=int(50 * SCALE))
        self.artist_label = tk.Label(contentFrame, text ="", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.artist_label.grid(row=2, column=0,sticky ="we", padx=(10, 30))
        self.album_label = tk.Label(contentFrame, text ="", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.album_label.grid(row=3, column=0,sticky ="we", padx=(10, 30))
        self.track_label = Marquee(contentFrame, text="")
        self.track_label.grid(row=1, column=0,sticky ="we", padx=(30, 50))
        self.progress_frame = tk.Canvas(contentFrame, height=int(72 * SCALE), bg=SPOT_BLACK, highlightthickness=0)
        self.progress_frame.grid(row=4, column=0,sticky ="we", pady=(int(52 * SCALE), 0), padx=(30, 50))
        self.frame_img = ImageTk.PhotoImage(flattenAlpha(Image.open('prog_frame.png')))
        self.time_frame = tk.Canvas(contentFrame, bg=SPOT_BLACK, highlightthickness=0)
        self.time_frame.grid(row=5, column=0,sticky ="we", padx=0, pady=(10, 0))
        self.time_frame.grid_columnconfigure(0, weight=1)
        self.elapsed_time = tk.Label(self.time_frame, text ="00:00", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN)
        self.elapsed_time.grid(row=0, column=0, sticky ="nw", padx = int(40 * SCALE))
        self.remaining_time = tk.Label(self.time_frame, text ="-00:00", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN)
        self.remaining_time.grid(row=0, column=1, sticky ="ne", padx = int(60 * SCALE))
        self.cached_album = None
        self.cached_artist = None
        
    def update_now_playing(self, now_playing):
        if not self.inflated:
            parent_width = self.winfo_width()
            if parent_width > 2:
                self.midpoint = (parent_width / 2) - 40
                self.progress_width = self.frame_img.width()
                self.progress_start_x = self.midpoint - self.progress_width / 2
                self.progress = self.progress_frame.create_rectangle(self.progress_start_x, 0, self.midpoint, int(72 * SCALE) , fill=SPOT_GREEN)
                self.progress_frame.create_image(self.midpoint, (self.frame_img.height() - 1)/2, image=self.frame_img)
                self.inflated = True
        if not now_playing:
            return
        self.track_label.set_text(now_playing['name'])
        artist = now_playing['artist']
        if self.cached_artist != artist:
            truncd_artist = artist if len(artist) < 20 else artist[0:17] + "..."
            self.artist_label.configure(text=truncd_artist)
            self.cached_artist = artist
        album = now_playing['album']
        if self.cached_album != album:
            truncd_album = album if len(album) < 20 else album[0:17] + "..."
            self.album_label.configure(text=truncd_album)
            self.cached_album = album
        context_name = now_playing['context_name']
        truncd_context = context_name if context_name else "Now Playing"
        truncd_context = truncd_context if len(truncd_context) < 20 else truncd_context[0:17] + "..."
        self.header_label.configure(text=truncd_context)
        update_delta = 0 if not now_playing['is_playing'] else (time.time() - now_playing["timestamp"]) * 1000.0
        adjusted_progress_ms = now_playing['progress'] + update_delta
        adjusted_remaining_ms = max(0, now_playing['duration'] - adjusted_progress_ms)
        if self.update_time:
            progress_txt = ":".join(str(timedelta(milliseconds=adjusted_progress_ms)).split('.')[0].split(':')[1:3])
            remaining_txt = "-" + ":".join(str(timedelta(milliseconds=adjusted_remaining_ms)).split('.')[0].split(':')[1:3])
            self.elapsed_time.configure(text=progress_txt)
            self.remaining_time.configure(text=remaining_txt)
        self.update_time = not self.update_time
        if self.inflated:
            adjusted_progress_pct = min(1.0, adjusted_progress_ms / now_playing['duration'])
            self.progress_frame.coords(self.progress, self.progress_start_x, 0, self.progress_width * adjusted_progress_pct + self.progress_start_x, int(72 * SCALE))
        if(now_playing['track_index'] < 0):
            self.context_label.configure(text="")
            return
        context_str = str(now_playing['track_index']) + " of " + str(now_playing['track_total'])
        self.context_label.configure(text=context_str)
          
class StartPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 
        self.green_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_arrow_grn.png')))
        self.black_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_arrow_blk.png')))
        self.empty_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_arrow_empty.png')))
        self.play_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_play.png')))
        self.pause_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_pause.png')))
        self.space_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_space.png')))
        self.wifi_image = ImageTk.PhotoImage(flattenAlpha(Image.open('pod_wifi.png')))
        self.configure(bg=SPOT_BLACK)
        header_container = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        header_container.grid(sticky='we')
        self.header_label = tk.Label(header_container, text ="sPot", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN) 
        self.header_label.grid(sticky='we', column=1, row=0, padx=(0, 10))
        self.play_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.play_indicator.grid(sticky='w', column=0, row=0, padx=(70 * SCALE,0))
        self.wifi_indicator = tk.Label(header_container, image=self.space_image, background=SPOT_BLACK)
        self.wifi_indicator.grid(sticky='w', column=2, row=0, padx=(0,90 * SCALE))
        header_container.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        divider = tk.Canvas(self)
        divider.configure(bg=SPOT_GREEN, height=DIVIDER_HEIGHT, bd=0, highlightthickness=0, relief='ridge')
        divider.grid(row = 1, column = 0, sticky ="we", pady=10, padx=(10, 30))
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row = 2, column = 0, sticky ="nswe")
        self.grid_rowconfigure(2, weight=1)
        listFrame = tk.Canvas(contentFrame)
        listFrame.configure(bg=SPOT_BLACK, bd=0, highlightthickness=0)
        listFrame.grid(row=0, column=0, sticky="nsew")
        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)

        # scrollbar 
        self.scrollFrame = tk.Canvas(contentFrame)
        self.scrollFrame.configure(bg=SPOT_BLACK, width=int(50 * SCALE), bd=0, highlightthickness=4, highlightbackground=SPOT_GREEN)
        self.scrollBar = tk.Canvas(self.scrollFrame, bg=SPOT_GREEN, highlightthickness=0, width=int(20 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5,  y=int(10 * SCALE), anchor="n", relwidth=.6, relheight=.9)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))
        
        self.listItems = []
        self.arrows=[]
        for x in range(6):
            item = tk.Label(listFrame, text =" " + str(x), justify=tk.LEFT, anchor="w", font = LARGEFONT, background=SPOT_BLACK, foreground=SPOT_GREEN, padx=(30 * SCALE))
            imgLabel = tk.Label(listFrame, image=self.green_arrow_image, background=SPOT_BLACK)
            imgLabel.image = self.green_arrow_image
            imgLabel.grid(row=x, column=1, sticky="nsw", padx = (0, 30))
            item.grid(row = x, column = 0, sticky="ew",padx = (10, 0))
            self.listItems.append(item)
            self.arrows.append(imgLabel)
        listFrame.grid_columnconfigure(0, weight=1)
        # listFrame.grid_columnconfigure(1, weight=1)
    

    def show_scroll(self, index, total_count):
        scroll_bar_y_rel_size = max(0.9 - (total_count - MENU_PAGE_SIZE) * 0.06, 0.03)
        scroll_bar_y_raw_size = scroll_bar_y_rel_size * self.scrollFrame.winfo_height()
        percentage = index / (total_count - 1)
        offset = ((1 - percentage) * (scroll_bar_y_raw_size + int(20 * SCALE))) - (scroll_bar_y_raw_size + int(10 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5, rely=percentage, y=offset, anchor="n", relwidth=.66, relheight=scroll_bar_y_rel_size)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))

    def hide_scroll(self):
        self.scrollFrame.grid_forget()

    def set_header(self, header, now_playing = None, has_wifi = False):
        truncd_header = header if len(header) < 20 else header[0:17] + "..."
        self.header_label.configure(text=truncd_header)
        play_image = self.space_image
        if now_playing is not None:
            play_image = self.play_image if now_playing['is_playing'] else self.pause_image
        self.play_indicator.configure(image = play_image)
        self.play_indicator.image = play_image
        wifi_image = self.wifi_image if has_wifi else self.space_image
        self.wifi_indicator.configure(image = wifi_image)
        self.wifi_indicator.image = wifi_image
    
    def set_list_item(self, index, text, line_type = LINE_NORMAL, show_arrow = False):
        bgColor = SPOT_GREEN if line_type == LINE_HIGHLIGHT else SPOT_BLACK
        txtColor = SPOT_BLACK if line_type == LINE_HIGHLIGHT else \
            (SPOT_GREEN if line_type == LINE_NORMAL else SPOT_WHITE)
        truncd_text = text if len(text) < 17 else text[0:15] + "..."
        self.listItems[index].configure(background=bgColor, foreground=txtColor, text=truncd_text)
        arrow = self.arrows[index]
        arrow.grid(row=index, column=1, sticky="nsw", padx = (0, 30))
        arrowImg = self.empty_arrow_image if not show_arrow else \
            (self.black_arrow_image if line_type == LINE_HIGHLIGHT else self.green_arrow_image)
        arrow.configure(background=bgColor, image=arrowImg)
        arrow.image = arrowImg

