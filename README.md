# Overview:

This project is a fork of https://github.com/dupontgu/retro-ipod-spotify-client and is currently not ready for deployment yet

# Hardware
Raspberry Pi 3A+
Waveshare 2" screen communicating via FBCP
Adafruit #5001 Directional Navigation and Scroll Wheel Rotary Encoder
Nuforce USB DAC/amp
Waveshare BAttery HAT that takes in a 14500 battery

# Operating System
RaspberryOS Lite Bullseye 64 bit

# Frontend

The frontend of this application is a custom Spotify application based off of tkinter. The following dependencies are used:
- tkinter
- Spotipy 2.25.1
- PIL

The basis of the application is that it is a tkinter application. All communication with the Spotify API is done through Spotipy. For playback that is handled on the backend

# Backend
To handle playback, this project relies on Raspotify.

