##Socket library
import socket
import time

# to make this work you have to enter your or your bots login data in the IRC connection data section
# there are also some username checks in the code where you have to enter your username
# the bot saves Mario Maker levels in a list and lets you select the next ones
# two files are created codes.txt where all level codes are stored
# and a file which only saved the current level, this is meant for streamers so you can display the current level inkl code in your stream.
# your commands are: 
# !start(selects the first level after the bot is started and people entered levels in the list) 
# !done(when youre done with a level and want to select the next one)
# !bye (closes the bot)
# user commands are:
# !submit xxxx-xxxx-xxxx-xxxx (enters code into list, does not check if its a valid code)
# !queue (check if you have a level in the list atm, and on which position it is)

def writeList(liste):
	f = open("codes.txt","w")
	for item in liste:
		f.write(str(item[0]) + "\t\t" + str(item[1])+"\n")
	f.close()

def submit(sender, msg,s,liste):
	code = msg.split("!submit")[1]
	if(len(code) < 16):
		s.send("PRIVMSG " +CHANNEL+" :Please submit levels like this \"!submit xxxx-xxxx-xxxx-xxxx\".\r\n")
	else:
		liste.append((sender,code))
		s.send("PRIVMSG " +CHANNEL+" :"+sender+" submited: " + code +".\r\n")
		writeList(liste)

def findInListe(liste,sender):
	i = 0
	for item in liste:
		i+= 1
		if(item[0].find(sender) >= 0):
			return i 
	return -1

def writeCurrentLevel(liste):
	user = liste[0][0]
	code = liste[0][1]
	f = open("currentLevel.txt","w")
	f.write(str(user) + ": " + str(code))
	f.close()

##	IRC connection data
HOST="irc.twitch.tv" ##This is the Twitch IRC ip, don't change it.
PORT=6667 ##Same with this port, leave it be.
NICK="botname here" ##This has to be your bots username. # pw 12341234
PASS="your tmi here" ##Instead of a password, use this http://twitchapps.com/tmi/, since Twitch is soon updating to it.
IDENT="botname here" ##Bot username again
REALNAME="botname here" ##This doesn't really matter.
CHANNEL="#channelname here" ##This is the channel your bot will be working on.
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

liste = []
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
				print "msg IndexError"
				continue
		if msg.find("!submit") >= 0:
			submit(sender,msg,s,liste)
		if msg.find("!start") >= 0 and sender == "your user name here":
			writeCurrentLevel(liste)
		if msg.find("!done") >= 0 and sender == "your user name here":
			if(len(liste) < 1):
				print "liste leer"
				continue
			liste.pop(0)
			writeList(liste)
			writeCurrentLevel(liste)
		if(msg.find("!queue") >= 0):
			toprint = ""
			toprint += "Currently "+str(len(liste))+" levels in queue."
			pos = findInListe(liste, sender)
			if(pos < 0):
				toprint += "You dont have a level in queue."
			else:
				toprint += "Your Level is on Position " + str(pos) +"."
			s.send("PRIVMSG "+CHANNEL+" :"+toprint+"\r\n")
		if msg.find("!bye") >= 0 and sender == "your user name here":
			break
print "Done"