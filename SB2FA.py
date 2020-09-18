"""
Made by EvolveRedux
"""

import pyotp
import rumps
import pyperclip
import os
import time
import base64

if os.path.exists('otpcode') == False:
    f = open("otpcode", "x")
if os.path.exists('pwd') == False:
    f = open("pwd", "x")

size = os.stat("otpcode").st_size == 0
size2 = os.stat("pwd").st_size == 0

if size == True:
    window = rumps.Window(message='Please enter your 2FA Secret in the textbox below:', title="First Use Setup", default_text="", ok="Done", cancel=None, dimensions=(120, 100))
    response = window.run()
    if response.clicked:
        otpsecret = response.text
        while len(otpsecret) < 2:
            window = rumps.Window(message='Your 2FA secret is invalid. Please try again:', title="Error", default_text="", ok="Done", cancel=None, dimensions=(120, 100))
            response = window.run()
            if response.clicked:
                otpsecret = response.text
                otpsecret = otpsecret.replace(" ", "")

                f = open("otpcode", "w")
                f.write(otpsecret)
                f.close()
        while otpsecret.isnumeric() == True:
            window = rumps.Window(message='Your 2FA secret is invalid. Please try again:', title="Error", default_text="", ok="Done", cancel=None, dimensions=(120, 100))
            response = window.run()
            if response.clicked:
                otpsecret = response.text
                otpsecret = otpsecret.replace(" ", "")
                f = open("otpcode", "w")
                f.write(otpsecret)
                f.close()
        otpsecret = otpsecret.replace(" ", "")
        f = open("otpcode", "w")
        f.write(otpsecret)
        f.close()
if size2 == True:

    window = rumps.Window(message='Please enter a password for erasing the 2FA secret:', title="First Use Setup", default_text="", ok="Done", cancel=None, dimensions=(120, 100))
    response2 = window.run()
    if response2.clicked:
        pwd = response2.text
        message_bytes = pwd.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_pwd = base64_bytes.decode('ascii')
        f = open("pwd", "w")
        f.write(base64_pwd)

f = open("otpcode", "r")
secret = f.read()

otp = pyotp.TOTP(secret)

otpcode = otp.now()
@rumps.clicked('Generate code to clipboard')
def generateclip(_):
    otpcode = otp.now()
    pyperclip.copy(otpcode)
    rumps.notification("SB2FA", "Code Generation is on cooldown for 15 seconds.", " ", sound=None)
    time.sleep(15)
@rumps.clicked("Generate code in a window")
def genwindow(_):
    otpcode = otp.now()
    window = rumps.Window(message='Code generation will be on cooldown for 15 seconds after you close the window.', title="2FA Code: ", default_text=otpcode, ok="Copy code", cancel=None, dimensions=(320, 160))
    response = window.run()
    if response.clicked:
        pyperclip.copy(otpcode)
    time.sleep(15)
@rumps.clicked("Erase code")
def erasecode(_):
    window = rumps.Window(message='Please enter your password below:', title="Erase code", default_text="", ok="Done", cancel="Cancel", dimensions=(120, 100))
    response3 = window.run()
    if response3.clicked:
        pwdinput = response3.text
        f = open("pwd", "r")
        pwd = f.read()
        base64_pwd = pwd
        base64_bytes = base64_pwd.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        decodedpwd = message_bytes.decode('ascii')
        if decodedpwd == pwdinput:
            f = open('otpcode', 'r+')
            f.truncate(0)


app = rumps.App('SB2FA', menu=['Generate code to clipboard', "Generate code in a window", "Erase code"], quit_button='Quit')
app.run()
