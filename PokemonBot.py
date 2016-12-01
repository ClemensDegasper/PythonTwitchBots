##Socket library
import socket
import time
import win32com.client as comclt
import SendKeys
from ctypes import windll

# this bot reads chat commands from your users and turns them into button presses on your computer
# this can be used to let your twitch viewers play pokemon on your pc
# in the function below you can read which command correlates to which button press.
# when a viewer types "up" for example the bot emulates  a press of the "1" key
# this only works on windows machine because of the use of the windll lib

def Up(sender):
	keycode = windll.user32.VkKeyScanA(ord("1"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":up\n"
def Down(sender):
	keycode = windll.user32.VkKeyScanA(ord("2"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":down\n"
def Left(sender):
	keycode = windll.user32.VkKeyScanA(ord("3"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":left\n"
def Right(sender):
	keycode = windll.user32.VkKeyScanA(ord("4"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":right\n"
def A(sender):
	keycode = windll.user32.VkKeyScanA(ord("5"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":a\n"
def B(sender):
	keycode = windll.user32.VkKeyScanA(ord("6"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":b\n"
def Select(sender):
	keycode = windll.user32.VkKeyScanA(ord("9"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":select\n"
def Start(sender):
	keycode = windll.user32.VkKeyScanA(ord("0"))
	scancode = windll.user32.MapVirtualKeyA(keycode, 0)
	windll.user32.keybd_event(keycode, scancode, 0, 0)
	time.sleep(0.1)
	windll.user32.keybd_event(keycode, scancode, 2, 0)
	print str(sender) + ":start\n"

##IRC connection data
HOST="irc.twitch.tv" ##This is the Twitch IRC ip, don't change it.
PORT=6667 ##Same with this port, leave it be.
NICK="your name here" ##This has to be your bots username.
PASS="your code here" ##Instead of a password, use this http://twitchapps.com/tmi/, since Twitch is soon updating to it.
IDENT="your name here" ##Bot username again
REALNAME="your name here" ##This doesn't really matter.
CHANNEL="#your channel here" ##This is the channel your bot will be working on.
s = socket.socket( ) ##Creating the socket variable
s.connect((HOST, PORT)) ##Connecting to Twitch
s.send("PASS %s\r\n" % PASS) ##Notice how I'm sending the password BEFORE the username!
##Just sending the rest of the data now.
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
##Connecting to the channel.
s.send("JOIN %s\r\n" % CHANNEL)
##Eternal loop letting the bot run.
text=s.recv(2040)  #receive the text
time.sleep(3)
print "joined: " + HOST + " in " + CHANNEL 
s.send("PRIVMSG "+CHANNEL+" :Hi all!\r\n")
text=s.recv(2040)  #receive the text
text = ""
wsh= comclt.Dispatch("WScript.Shell")

while (1):
	text=s.recv(2040)  #receive the text
	if (text != ""):
		#print text   #print text to console
		if text.find('PING') != -1:                          #check if 'PING' is found
			s.send('PONG ' + text.split() [1] + '\r\n') #returnes 'PONG' back to the server (prevents pinging out!)
			continue
		if text.find("PRIVMSG"):
			text = text.strip("\n\r")
			try:
				sender = text.split("@")[0].split("!")[1]
				msg = text.split(":")[2]
			except IndexError:
				continue
			if (msg == "up"):
				Up(sender)
			if (msg == "down"):
				Down(sender)
			if (msg == "left"):
				Left(sender)
			if (msg == "right"):
				Right(sender)
			if (msg == "a"):
				A(sender)
			if (msg == "b"):
				B(sender)
			if (msg == "start"):
				Start(sender)
			if (msg == "select"):
				Select(sender)