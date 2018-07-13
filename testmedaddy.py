from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

import googlemaps
from datetime import datetime

from dbhelper import DBuser
from dbhelper import DBbike

import logging

DBu = DBuser()
DBb = DBbike()

gmaps = googlemaps.Client(key='GMAPSKEYIFYOUGOTONE') #Was thoght of for another function, not used jet

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token="HERENEEDSTOGOYOURTOKEN!") #FILL IN YOUR TOKEN!
dispatcher = updater.dispatcher

FAHRRAD, LOCATION = range(2)

AUSLEIHEN, AUSWAHL = range(2)

ENFWAHL, ENFBIKE = range(2)

AUTHHIM, CONFIRMAUTH = range(2)

HINFB, POSITION, PASSWORD, SPENDER = range(4)

ENFU, USERENF = range(2)


def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Hallo "+update.message.from_user.first_name+" :) leider musst du fuer diesen Dienst angemeldet sein. Frag einfach NAME wenn du mitmachen willst!\nLeite einfach diese Nachricht an ihn weiter:")
	bot.send_message(chat_id=update.message.chat_id, text=str(update.message.chat_id))
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#Testfunction

# def wo(bot, update):
# 	bot.sendVenue(chat_id=update.message.chat_id, latitude="52.521918", longitude="13.413215", title="Fahrrad nr. 1", address="An der TU Berlin")
# 	usser=DBu.get_authuser()
# 	bot.send_message(chat_id=update.message.chat_id, text="das kommt"+str(usser))


#With this funcion you make yourself the boss. not the best workaround, but I needed it quick TODO:MASTERUSER needs to be your number (usernumber)
def littleboo(bot, update):
	usser=DBu.get_authuser()
	if "MASTERUSER" not in usser:
		DBu.add_authuser("MASTERUSER")
		bot.send_message(chat_id=update.message.chat_id, text="Hallo!")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Wie kommst du drauf?")


# ABSTELLEN

def abstellen(bot, update):
	if auth(bot, update):
		bikes=DBb.get_bikes(update.message.chat_id)
		keystring=""
		if len(bikes) > 0:
			for x in range (0,len(bikes)):
				keystring+=str(bikes[x])
			reply_keyboard = [keystring]
			update.message.reply_text("Welches Fahrrad willst du abstellen?",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
			return FAHRRAD
		else:
			update.message.reply_text("Du hast nichts was ich wollen koennte",reply_markup=ReplyKeyboardRemove())


def fahrrad(bot, update, user_data):
	user = update.message.from_user
	logger.info("Number of %s: %s", user.first_name, update.message.text)

	update.message.reply_text("Nice, now send me the location of your Drahtesel!")

	user_data['bnr']=int(update.message.text)	

	return LOCATION

def location(bot, update, user_data):


	user=update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
	bnr=user_data['bnr']

	DBb.up_long(user_location.longitude,bnr)
	DBb.up_lat(user_location.latitude,bnr)
	DBb.up_status1(bnr)
	DBb.up_user(0,bnr)
	


	update.message.reply_text("Zenks Vor Treffeling With Deutsche Bike! ",reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END

def cancel(bot, update):
	user = update.message.from_user
	logger.info("User %s Wollte doch nicht")%user.first_name
	update.message.reply_text("tschau!",reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END


# AUSLEIHEN

def ausleihen(bot, update):
	if auth(bot, update):
		allmabikes=DBb.get_freebikes()
		if len(allmabikes)>0:
			keystring=""
			# for x in range (0,len(allmabikes)):
			# 	keystring+='['
			# 	keystring+='"'
			# 	keystring+=str(allmabikes[x])
			# 	keystring+='"'
			# 	keystring+=']'
			# 	if x < len(allmabikes)-1:
			# 		keystring+=','
			for x in range (0,len(allmabikes)):
				bot.sendVenue(chat_id=update.message.chat_id, latitude=str(DBb.get_lat(allmabikes[x])[0]), longitude=str(DBb.get_long(allmabikes[x])[0]), title="Fahrrad NR."+str(allmabikes[x]), address="Entfernung: ")
				keystring+=str(allmabikes[x])
				# if x < len(allmabikes)-1:
				# 	keystring+=''

			reply_keyboard = [keystring]

			update.message.reply_text("Welches Fahrrad willst du ausleihen?\nmit /cancelausl kannst du diesen Vorgang abbrechen",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))

			return AUSWAHL
		else:
			bot.send_message(chat_id=update.message.chat_id,text="Es ist leider kein Bike frei :)")
			

def auswahl(bot, update):
	if int(update.message.text)>=1 and int(update.message.text)<=400:
		bnr=int(update.message.text)
		freebikes=DBb.get_freebikes()
		if bnr in freebikes:
			update.message.reply_text("Dein Bike ist da:")
			bot.sendVenue(chat_id=update.message.chat_id, latitude=str(DBb.get_lat(bnr)[0]), longitude=str(DBb.get_long(bnr)[0]), title="Fahrrad NR."+str(bnr), address="Der Code ist: "+str(DBb.get_pw(bnr)[0]))
			DBb.up_status0(bnr)
			DBb.up_user(update.message.chat_id,bnr)

			return ConversationHandler.END

		else:
			bot.send_message(chat_id=update.message.chat_id,text="Ist zwar ne nummer, aber nimmer frei mein Freund!")
			return AUSWAHL
	else:
		bot.send_message(chat_id=update.message.chat_id,text="Iwas machste falsch, GIB MIR NE NUMMER! "+update.message.text)
		return AUSWAHL

def cancelausl(bot, update):
	user = update.message.from_user
	logger.info("User %s Wollte doch nicht abstellen")
	update.message.reply_text("tschau!",reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END

#AUTH

def auth(bot, update):
	authuser = DBu.get_authuser()
	if update.message.chat_id in authuser:
		# bot.send_message(chat_id=update.message.chat_id, text="Du bist dabei!")
		return 1
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Keinen Zugriff!")
		return 0

#ENFBIKE
def enfbike(bot,update):
	if checkmaster(bot,update):
		allbikes=DBb.get_allbikes()
		if len(allbikes)>0:
			keystring=""
			for x in range (0,len(allbikes)):
				keystring+=str(allbikes[x])

			reply_keyboard = [keystring]

			update.message.reply_text("Welches Fahrrad willst du LOESCHEN? mit\n/cancel kommst du zurueck",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))

			return ENFWAHL
		else:
			bot.send_message(chat_id=update.message.chat_id,text="Es gibt keine Bikes")

def enfwahl(bot, update):
	bnr=int(update.message.text)
	if bnr>0 and bnr <=400:
		DBb.delete_bike(str(bnr))
		update.message.reply_text("Bike nr %s wurde geloescht"%bnr)
		return ConversationHandler.END
	else:
		update.message.reply_text("Ne Nummer bitte!")
		return ENFBIKE

#HINFBIKE

def hinfb(bot, update):
	if checkmaster(bot,update):
		update.message.reply_text("Wie ist der Key?\nbitte nur Zahlen!")
		return PASSWORD
	else:
		update.message.reply_text("NANANAN-Batman")


def password(bot, update, user_data):
	user_data['passwordd']=int(update.message.text)
	if type(user_data['passwordd'])==int or type(user_data['passwordd'])==long and user_data['passwordd']<9:
		update.message.reply_text("Wie ist der Name des edlen Spenders?")
		return SPENDER
	else:
		update.message.reply_text("Bitte nur Zahlen")
		return PASSWORD

def spender(bot, update, user_data):
	user_data['spender']=str(update.message.text)
	if type(user_data['spender'])==str:
		update.message.reply_text("Wo steht das neue Fahrrad?")
		return POSITION
	else:
		update.message.reply_text("Str only!")
		return SPENDER

def position(bot, update, user_data):
	user=update.message.from_user
	user_location = update.message.location
	logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)

	password=user_data['passwordd']
	spender=user_data['spender']
	DBb.add_bike(1,user_location.latitude,user_location.longitude,password,spender)

	update.message.reply_text("Danke fuer das neue Fahrrad!",reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END



#AUTHCONVERS

def authhim(bot,update):
	if checkmaster(bot,update):
		update.message.reply_text("Wen moechtest du authen? mit\n/cancel kommst du zurueck")

		return CONFIRMAUTH

def confirmauth(bot, update):
	DBu.add_authuser(update.message.text)
	update.message.reply_text("Du hast %s zum Mitglied gemacht"%update.message.text)
	return ConversationHandler.END

#USER ENFERNEN

def enfu(bot, update):
	if checkmaster:
		update.message.reply_text("Wen moechtest du entfernen?\nmit /cancel kommst du zurueck")
		return USERENF

def userenf(bot, update):
	usertoenf=update.message.text
	DBu.delete_authuser(usertoenf)
	update.message.reply_text("Du hast %s entfernt"%usertoenf)
	return ConversationHandler.END
#TEST

def test(bot, update):
	freebikes=DBb.get_freebikes()
	bot.send_message(chat_id=update.message.chat_id, text="TESTCHECK"+str(freebikes))

	
	testresult=gmaps.origins(41.43206,-81.38992|-33.86748,151.20699)
	messageiwannasend=testresult[][][]

	bot.send_message(messageiwannasend)



test_handler = CommandHandler('test',test)
dispatcher.add_handler(test_handler)

# def bikeadder(bot, update):
# 	DBb.add_bike(1,12.3,13.3,3333,"\'samuel\'")
# 	bot.send_message(chat_id=update.message.chat_id, text="BOIII")

# bikeadder_handler = CommandHandler('bikeadder',bikeadder)
# dispatcher.add_handler(bikeadder_handler)

#MASTER

def checkmaster(bot, update):
	if auth(bot, update):
		masters = DBu.get_master()
		chat_id = update.message.chat_id
		if chat_id in masters:
			return 1
		else:
			return 0

def admin(bot, update):
	if checkmaster(bot, update):
		bot.send_message(chat_id=update.message.chat_id, text="ALLE BEFEHLE:\n/authhim - um eine Nummer ins System zu fuegen\n/bikeadder - fuegt ein Fahrrad hinzu, vorgefertigt\n/enfbike - entfernt ein bike")

# ID direkt nach dem Befehl muss erreicht werden idk how to
# MASTERNUMBER MUSS DEINE ID WERDEN!
def makemaster(bot, update):
	if auth(bot,update):
		masters = DBu.get_master()
		chat_id = update.message.chat_id
		if chat_id==MASTERNUMBER:
			bot.send_message(chat_id=update.message.chat_id, text="Du bist jetzt ein MASTER! "+str(chat_id))
			DBu.make_master("MASTERNUMBER")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Du bist leider kein MASTER! "+str(chat_id))

makemaster_handler = CommandHandler('makemaster', makemaster)
dispatcher.add_handler(makemaster_handler)

wo_handler = CommandHandler('wo', wo)
dispatcher.add_handler(wo_handler)

littleboo_handler = CommandHandler('littleboo', littleboo)
dispatcher.add_handler(littleboo_handler)

admin_handler = CommandHandler('admin', admin)
dispatcher.add_handler(admin_handler)

def main():
	DBu.setup()
	DBb.setup()
	authuser = DBu.get_authuser()

	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('abstellen', abstellen)],

		states={
			FAHRRAD: [MessageHandler(Filters.text, fahrrad, pass_user_data=True)],

			LOCATION: [MessageHandler(Filters.location, location, pass_user_data=True)]
		},

		fallbacks=[CommandHandler("cancel",cancel)]
	)

	dispatcher.add_handler(conv_handler)

	#conversation zum ausleihen eines bikes
	convausl_handler = ConversationHandler(
		entry_points=[CommandHandler('ausleihen', ausleihen)],

		states={
			AUSWAHL: [MessageHandler(Filters.text, auswahl)]
		},

		fallbacks=[CommandHandler("cancelausl",cancelausl)]
	)

	dispatcher.add_handler(convausl_handler)

	#conversation zum Hinzufuegen eines Bikes
	convhinfb_handler = ConversationHandler(
		entry_points=[CommandHandler('hinfb', hinfb)],

		states={

			PASSWORD: [MessageHandler(Filters.text, password, pass_user_data=True)],

			SPENDER: [MessageHandler(Filters.text, spender, pass_user_data=True)],

			POSITION: [MessageHandler(Filters.location, position, pass_user_data=True)]

		},

		fallbacks=[CommandHandler("cancel",cancel)]
	)

	dispatcher.add_handler(convhinfb_handler)


	#conversation zum Entfernen eines Bikes (ADMIN ONLY)
	convenf_handler = ConversationHandler(
		entry_points=[CommandHandler('enfbike', enfbike)],

		states={
			ENFWAHL: [MessageHandler(Filters.text, enfwahl)]
		},

		fallbacks=[CommandHandler("cancel",cancel)]
	)
	dispatcher.add_handler(convenf_handler)


	#conversation zum Authen eines Users	(ADMIN ONLY)
	convauth_handler = ConversationHandler(
		entry_points=[CommandHandler('authhim', authhim)],

		states={
			CONFIRMAUTH: [MessageHandler(Filters.text, confirmauth)]
		},

		fallbacks=[CommandHandler("cancel",cancel)]
	)
	dispatcher.add_handler(convauth_handler)


	#conversation zum Entfernen eines Users	(ADMIN ONLY)
	convenfu_handler = ConversationHandler(
		entry_points=[CommandHandler('enfu', enfu)],

		states={
			USERENF: [MessageHandler(Filters.text, userenf)]
		},

		fallbacks=[CommandHandler("cancel",cancel)]
	)

	dispatcher.add_handler(convenfu_handler)

	updater.start_polling()

	updater.idle()

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Ich habe dein Begehren nicht so ganz verstanden :(")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

if __name__ == "__main__":
	main()
