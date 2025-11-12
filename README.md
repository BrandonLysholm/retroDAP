# Overview:

This project is a fork of https://github.com/dupontgu/retro-ipod-spotify-client and is ready for deployment

# Hardware
See docs for more detailed list/links

- Raspberry Pi Zero 2W (for development, will switch to Zero 2W)
- Waveshare 2" screen communicating via FBCP
- Adafruit #5001 Directional Navigation and Scroll Wheel Rotary Encoder
- Nuforce USB DAC/amp
- 18650 battery and charger
- 3D printed case


# Operating System
RaspberryOS Lite Bullseye 64 bit

# Deployment Instructions:

My instructions are based heavily off of: https://github.com/dupontgu/retro-ipod-spotify-client/issues/69
I use VIM, but the previous one uses nano. If you prefer nano, I recommend following the original tutorial, so that you can copy/paste commands in, but there will be a few paths you will need to modify, and steps to skip.

I recommend connecting to the Pi through SSH, and then just copying the commands into terminal.

If this project is still being actively maintained when you are deploying, it may be worth considering forking the repo, so that you can save your device ID into a github repo, which should make updates a bit easier. It would involve having to keep track of when I make changes upstream, and then you syncing the fork.

## Install Updates

    sudo apt-get update -y
    sudo apt-get upgrade -y

## Install Required Packages

    sudo apt install python-setuptools python3-setuptools -y
    sudo apt install python3-pip -y
    sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
    sudo apt-get install python3-tk -y
    sudo apt-get install redis-server -y
    sudo apt-get install openbox -y
    sudo apt install xorg -y
    sudo apt-get install lightdm -y
    sudo apt-get install x11-xserver-utils -y
    sudo apt-get install git -y
    sudo apt-get instal vim -y

## Clone this repo and install dependencies

    git clone https://github.com/BrandonLysholm/retroDAP.git
    cd ~/retroDAP/frontend
    pip3 install -r requirements.txt

## Setup spotify API

TODO: copy the section from https://github.com/dupontgu/retro-ipod-spotify-client/issues/69

## Disable screensavers
    cd ~
    sudo vi .bash_profile

In that file input the following:
    #!/bin/bash
    [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor
    # Disable any form of screen saver / screen blanking / power management
    xset s off
    xset s noblank
    export SPOTIPY_CLIENT_ID='your_SPOTIPY_CLIENT_ID'
    export SPOTIPY_CLIENT_SECRET='your_SPOTIPY_CLIENT_SECRET'
    export SPOTIPY_REDIRECT_URI='http://localhost:8080'
    export DISPLAY=:0.0

## Configure Xintric
    sudo vi /etc/X11/xinitrc

Make that file look like the following: 
    #!/bin/sh
    # /etc/X11/xinit/xinitrc
    # global xinitrc file, used by all X sessions started by xinit (startx)
    # invoke global X session script 
    #. /etc/X11/Xsession' 

    exec openbox-session #-> This is the one that launches Openbox
    
## Spotify Chredentials:

    sudo vi /etc/xdg/openbox/environment
Paste the following in:

    export SPOTIPY_CLIENT_ID='your_SPOTIPY_CLIENT_ID'
    export SPOTIPY_CLIENT_SECRET='your_SPOTIPY_CLIENT_SECRET'
    export SPOTIPY_REDIRECT_URI='http://localhost:8080'

## Configure Raspotify

    sudo vi /etc/raspotify/conf

There are four sections you should change:
Changing the audio device to the DAC (line 70)
    LIBRESPOT_DEVICE="hw:CARD=Audio,DEV=0"
Changing the type of device (line 76)
    LIBRESPOT_DEVICE_TYPE=smartphone
Comment out volume normalization (line 106)
Change device name (line 121)
    libespot_name="retroDAP"

Then apply the changes:
    sudo systemctl restart raspotify

## Enteriing Device ID
To obtain your device id you first have to go to https://developer.spotify.com/console/get-users-available-devices/
when you go the the website it will probably not list it, so start playback on your device, and then it should appear

    cd ~/retroDAP/frontend
    vi spotify_manager.py

On line 11, switch out the value in DEVICE_ID to your DEVICE_ID. You will also have to modify this whenever you update the software, as the Github Repo will store my value. A workaround to this is to create a fork of my repo, with the only change being the device ID.

    cd ~/.local/lib/python3.9/site-packages/spotipy/
    vi client.py

You may have to alter the directory path a bit, if you are not running python3.9 (tab for autocomplete path directories makes this easy)

Go to line 1810, and replace the method with devices(self) with the following:

    def devices(self):
        data = {"device_ids": ["xx"], "play": force_play}
        return self._put("me/player", payload=data)

replace the xx with your device ID

## Generate .cache files:
For this section, I recommend using a more powerful Pi. I used a Raspberry Pi 3a+, but any will do. If you only have a the Zero 2W, it should work, but it will be slow

    sudo apt install midori
    cd ~
    git clone https://github.com/perelin/spotipy_oauth_demo
    cd ~/spotipy_oauth_demo
    sudo apt-get install python3-pip python-dev
    pip3 install -r requirements.txt

Before running it modify the client id and secret also your scopes in with:
    vi spotipy_oath_demo.py

Scope:
    SCOPE = "user-follow-read," \
            "user-library-read," \
            "user-library-modify," \
            "user-modify-playback-state," \
            "user-read-playback-state," \
            "user-read-currently-playing," \
            "app-remote-control," \
            "playlist-modify," \
            "playlist-read-private," \
            "playlist-read-collaborative," \
            "playlist-modify-public," \
            "playlist-modify-private," \
            "streaming," \
            "user-follow-modify," \
            "user-follow-read"

Before reboot, do the following:
    sudo raspi-config
And navigate the following:
system options --> boot / auto login --> console autologin
Restart the Pi
At this point, you will need to connect the pi to a mouse, keyboard, and a display. 

Once the Pi is connected, you will just see a black screen and a cursor. Right click with your mouse, and select "Terminal Emulator" and enter the following commands:

    cd spotify_oauth_demo
    python3 spotify_oauth_demo.py

Then, on the black desktop, right click and select Web Browser Midori. Once the browser launches, visit the website http://localhost:8080 and go through the process of logging in via that website. Once you reach the page of gibberish, the authentication is successful. Once done, you can close both the web browser and the terminal emulator. If using a Raspberry Pi other than a Zero 2W, shutdown and switch back to the Zero 2W. SSH back into the Pi 

Once logged back in enter the following commands:
    cp ~/spotipy_oauth_demo/.spotipyoauthcache ~/retroDAP/frontend/.cache
    chmod 777 ~/retroDAP/frontend/.cache

## Install screen driver
The screen installation is following the manufacturer's setup instructions found here: https://www.waveshare.com/wiki/2inch_LCD_Module?amazon#FBCP_Porting. It is worth noting that this driver is a fork of: https://github.com/juj/fbcp-ili9341

    sudo apt-get install cmake -y
    cd ~
    wget https://files.waveshare.com/upload/1/18/Waveshare_fbcp.zip
    unzip Waveshare_fbcp.zip
    cd Waveshare_fbcp/
    sudo chmod +x ./shell/*

Then, you need to modify the config file, to set the inactive percentage to 0.1%

    TODO: Add instructions here

Modify the config file

    sudo vi /boot/config.txt

And comment out the following lines
    #dtoverlay=vc4-kms-vs3
    #max_framebuffers=2

You will need to restart (this command schedules it a minute in advance, for you to exit the SSH session gracefully)
    sudo shutdown -r
    exit

Once restarted, SSH back into the Pi and do the following commands

    cd Waveshare_fbcp/
    mkdir build
    cd build
    sudo cmake -DSPI_BUS_CLOCK_DIVISOR=20 -DWAVESHARE_2INCH_LCD=ON -DBACKLIGHT_CONTROL=ON -DSTATISTICS=0 ..
    sudo make -j

Then, set the screen to start automatically:
    sudo cp ~/Waveshare_fbcp/build/fbcp /usr/local/bin/fbcp
    sudo vi /etc/rc.local

Add fbcp& before exit 0 at the end of the file

Set the user interface display size in the /boot/config.txt file. 
    sudo vi /boot/config.txt

Add the following lines at the end of config.txt
    hdmi_force_hotplug=1
    hdmi_cvt=640 480 60 1 0 0 0
    hdmi_group=2
    hdmi_mode=1
    hdmi_mode=87
    display_rotate=0

## Set retroDAP to autolaunch
Disable the cursor:

    sudo vi /.bash_profile

change the second line to the following:

    [[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor

Then set retroDAP to autostart

    sudo vi /etc/xdg/openbox/autostart

And paste the following at the end

    cd /home/YOUR_USERNAME/retroDAP/frontend/
    sudo -H -u YOUR_USERNAME --preserve-env=SPOTIPY_REDIRECT_URI,SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET python3 spotifypod.py &

## Finishing up
Restart the Pi and it should autolaunch the program. It will take a few moments. For the first launch, it takes longer since it needs to load your library. Once launched, it is ready, but we need to revert it back to not load your library each time, since it caches it. Edit the following:

    TODO add instructions for this

Then, it is ready for use. So far, I have noticed that it requires me to start playback on a separate device, connect to retroDAP, and then it is ready for use. I suspect this issue is due to not authenticating raspotify yet, and plan on debugging this in the future
