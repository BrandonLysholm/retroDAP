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

There are three sections you should change:

    

