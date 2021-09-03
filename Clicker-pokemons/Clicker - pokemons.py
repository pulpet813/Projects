# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 12:14:46 2021

@author: Kamil Lenkiewicz
"""

import time #Library needed for taking breaks in various situations
import pyautogui # Library used to get position of object using mouse click
import keyboard # Library used to repeat commands from keyboard
import cv2 # Library used in reading screenshots
import pytesseract # Library used in reading text from screenshot
import pyscreenshot as ImageGrab # Library used in taking desktop screenshots
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # Line needed for pytesseract to work

"""
This code is used as a some kind of bot or autoclicker in game Pokemon Planet, which is fanmade game based on gameboy
game "Pokemon". Code is based on fact, that every battle with pokemon have common attribute, more precisely
it's a wide belt with name of pokemon. How it works? Program takes screenshot of some portion of that wide belt,
read text from the belt and based of result do different actions (walk from left to right, heal pokemon, catch wild 
pokemon and so on). Code is not finished, it's possible to improve it. For now you need to run this code few times with
commenting some portion of code, to make this code work perfectly. Improvement will not take place because author 
of code (me) got banned from game.
"""

"""
Function "screen" takes screenshot of some portion of desktop, save it in folder, read it again,
then read text from screenshot
"""
def screen():
    im=ImageGrab.grab(bbox=(1015,153,1281,190)) #Takes screenshot. Numbers were taken from function "pyautogui.position()"
    im.save('im.png') #saves screen
    img = cv2.imread('im.png') #read screen in different format, neede to pytesseract work correctly
    text = pytesseract.image_to_string(img) #read text from screen
    return text #return readed text

"""
Function "click" makes mouse cursor click exact spot given as an arguments
"""

def click(x,y,liczba=1):
    pyautogui.click(x,y,clicks = liczba)

"""
Function "heal" is used to heal pokemon in case wild pokemon is not killed in one hit or not caught in first attempt.
It simply check if player is in "battle mode", which basically means if there is "battle" window (it can be recognize
by reading text form wide belt. If there is no text, there is no battle. So when player is outside battle, program always
heal player at least once
"""

def heal():
    while True:
        text = screen() #reading from screenshot gives information about if player is in battle
        if 'Wild' not in text and 'wild' not in text: # If text contains "Wild" or "wild", it means player is in battle. Difference in first letter uppercase is needed, becouse pytesseract reads this word different each time (I don't know why)
            pyautogui.moveTo(390,550) # Move cursor to given position based on where in inventory is heal potion
            time.sleep(0.25) # wait 1/4s, becouse too fast action can not be recognized by game
            pyautogui.click(clicks = 2, interval = 0.25) # click two times in interval 1/4s, to make sure heal potion will work
            time.sleep(0.25)
            pyautogui.moveTo(457,64) # moves cursor to pokemon
            time.sleep(0.25)
            click(404,64) #click on pokemon to heal him with potion
            return 0

"""
Function "wait" is used to make sure that battle is over. It makes screenshot of wide belt and check if there is word
"Wild" or "wild"
"""
def wait():
    im=ImageGrab.grab(bbox=(1015,153,1255,184))
    im.save('im.png')
    img = cv2.imread('im.png')
    text = pytesseract.image_to_string(img)
    while True:
        if 'wild' not in text and 'Wild' not in text:
            return 0

"""
Functon "kill" is used to kill specific pokemons. Program is "pressing" button "1", which serve as a fight button, as 
long as player is in "battle mode"
"""
def kill():
    while True:
        keyboard.press_and_release('1') # pressing "1" on keyboard
        text = screen() #check if there is battle
        if 'Wild' not in text and 'wild' not in text:
            return 0 # if not, then function is stopped

"""
Function "catch" is used to catch pokemons. Program clicks battle window in given spot, which serve as a button to
catch pokemon. Program click button as long as player is in the battle
"""
def catch():
    while True:
        click(836,723) # click in exact spot of battle window
        text = screen()
        if 'Wild' not in text and 'wild' not in text:
            return 0

"""
Function "check" is used to check if other players give trade request or friend request (it interrupts code).
Before running code, screenshot of trade/friend request is made. Function compare existed screen with new made screen.
If it's exactly the same screen, program clicks mouse cursor in exact spot, which serve as a refuse button.
"""
def check():
    im3=ImageGrab.grab(bbox=(805,559,890,586)) #Takes screenshot
    im3.save('im3.png') #saves it
    img3 = cv2.imread('im3.png') #read it again
    img2 = cv2.imread('im2.png') #read screen made before
    if img3.all() == img2.all(): #comparing pictures
        click(1049,577) # if pictures are equivalent, click on exact spot


print(pyautogui.position()) # Line is used in taking positions of needed spots

recorded1 = keyboard.record(until='esc') #save move in left

recorded2 = keyboard.record(until='esc') #save move in right

# Loop
number=0 # indicate number of taken loops
i=1 # used to exit loop
while i == 1:
    keyboard.play(recorded1) #play move in left
    text = screen() #read the screen
    if 'Wild' in text or 'wild' in text: # check if there is a battle
        if '[S]' in text or 'Machop' in text or 'Onix' in text: # If it's true, catch pokemon and heal pokemons
            catch()
            wait()
            heal()
            heal()
            heal()
        elif ('[E]' in text or 'Clefairy' in text) and '[S]' not in text: #check if there is pokemon to kill (and not Shiny)
            kill()
            wait()
            heal()
        else: # if any of it, run from pokemon
            p=0
            while p==0:
                keyboard.press_and_release('4') # "press" button "4", which serve as a "run from pokemon" button
                text = screen()
                if 'Wild' not in text and 'wild' not in text: #press button as long as player is in battle
                    p=1
    keyboard.play(recorded2) # play move in right, code above is analogical to upper
    text = screen()
    if 'Wild' in text or 'wild' in text:
        if '[S]' in text or 'Machop' in text or 'Onix' in text:
            catch()
            wait()
            heal()
        elif ('[E]' in text or 'Clefairy' in text) and '[S]' not in text:
            kill()
            wait()
            heal()
        else:
            p=0
            while p==0:
                keyboard.press_and_release('4')
                text = screen()
                if 'Wild' not in text and 'wild' not in text:
                    p=1
    number +=1
    if number%50 == 0: # if it's multiply of 50 loop, then check if there is trade/friends request
        check()