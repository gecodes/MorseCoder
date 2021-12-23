# Programming Language Research Project
# Morse Coder
# Graham Gammon-Everitt - 041014182
# CST8333-450

# Import Module
import tkinter as tk
from tkinter import *
import numpy
import pygame


# Coder Class with encryption functions ################################################################################
class Coder:
    def __init__(self):
        # Define Morse codes by letter in a dictionary as key:value pairs.
        self.MORSE_DICT = {
            # Letters
            'A': '.-', 'B': '-...', 'C': '-.-.',
            'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-',
            'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',
            # Numbers
            '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....',
            '7': '--...', '8': '---..', '9': '----.',
            '0': '-----',
            # Punctuation
            ',': '--..--', '.': '.-.-.-', '?': '..--..',
            '/': '-..-.', '-': '-....-', '(': '-.--.',
            ')': '-.--.-', '\'': '.----.', '&': '.-...',
            '!': '-.-.--', '"': '.-..-.', ':': '---...',
            '@': '.--.-.',
            # Space
            ' ': '/'
        }

    # Encryption function that loops through string message and translates into Morse using the dictionary
    def encrypt(self, message):
        message = message.upper()
        cipher = ''
        for letter in message:
            if letter in self.MORSE_DICT:
                cipher += self.MORSE_DICT[letter] + ' '
            else:
                cipher = 'This message has invalid characters.'
        return cipher

    # Decryption function. May be an included later on but not an original requirement
    def decrypt(self, message):
        message = message.upper()
        # extra space added at the end to access the last morse code
        message += ' '

        decipher = ''
        morse_char = ''
        for letter in message:
            # checks for space, denoting the end of a character code
            if letter != ' ':
                # storing morse code of a single character
                morse_char += letter

            # When a space denoting the end of a character code
            else:
                # accessing the keys using their values (reverse of encryption)
                decipher += list(self.MORSE_DICT.keys())[list(self.MORSE_DICT.values()).index(morse_char)]
                morse_char = ''

        return decipher


class Beeper:
    def play_audio_code(self, message):

        # Setting up the tone to be sampled
        sampleRate = 24100
        freq = 440

        pygame.mixer.init(24100, -16, 1, 512)

        arr = numpy.array(
            [4096 * numpy.sin(2.0 * numpy.pi * freq * x / sampleRate) for x in range(0, sampleRate)]).astype(
            numpy.int16)
        arr2 = numpy.c_[arr, arr]
        beep = pygame.sndarray.make_sound(arr2)

        # Morse code timing
        # Dot: 1 unit
        # Dash: 3 units
        # Intra-character space (the gap between dots and dashes within a character): 1 unit
        # Inter-character space (the gap between the characters of a word): 3 units
        # Word space (the gap between two words): 7 units

        # let one unit be 75ms
        for character in message:
            if character == '.':
                beep.play(-1)
                pygame.time.delay(75)
                beep.stop()
                pygame.time.delay(75)

            elif character == '-':
                beep.play(-1)
                pygame.time.delay(225)
                beep.stop()
                pygame.time.delay(75)

            elif character == ' ':
                pygame.time.delay(225)

            elif character == '/':
                pygame.time.delay(75)


# View and Controller functions ########################################################################################
root = tk.Tk()

output = StringVar()


# code_button onclick controller
def code_button_function():
    coder = Coder()
    output.set(coder.encrypt(user_input.get("1.0", "end-1c")))


def play_button_function():
    coder = Coder()
    beeper = Beeper()

    # convert message to a string representation of the morse code
    message_to_play = coder.encrypt(user_input.get("1.0", "end-1c"))
    output.set(message_to_play)
    beeper.play_audio_code(message_to_play)


root.title("Morse Coder: Bleep on bleepin' on!")
root.geometry('700x350')

# Canvas used for GUI formatting
canvas = tk.Canvas(
    root,
    width=700,
    height=350,
    bg="#FFB740"
)
canvas.grid(columnspan=3, rowspan=4)

# Title label
title = tk.Label(
    root,
    text="Morse Coder",
    font="Helvetica",
    bg="#FFB740",
    fg="#22577A"
)
title.grid(row=0, column=1)

# User input textbox
user_input = tk.Text(
    root,
    height=1,
    width=70,
    bg="#FDE49C",
    fg="#22577A"
)
user_input.grid(row=1, column=1)

# Code output box
code_output = tk.Label(
    root,
    textvariable=output,
    font="Helvetica",
    borderwidth=2,
    relief="groove",
    height=8,
    width=50,
    wraplength=500,
    bg="#FDE49C",
    fg="#22577A"
)
code_output.grid(row=2, column=1)

# Encode button
code_button = tk.Button(
    root,
    text="ENCODE",
    width=15,
    height=1,
    bg="#DF711B",
    fg="#FDE49C",
    command=lambda: code_button_function()
)
code_button.grid(row=3, column=0, padx=15)

# Play button
play_button = tk.Button(
    root,
    text="PLAY",
    width=15,
    height=1,
    bg="#DF711B",
    fg="#FDE49C",
    command=lambda: play_button_function()
)
play_button.grid(row=3, column=2, padx=15)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Fix application size
root.resizable(FALSE, FALSE)
root.mainloop()
