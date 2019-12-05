import telebot
import translate
import json
import sys

token=''

try:
	f = open('token.txt', 'r')
	token = f.read()
except FileNotFoundError:
	print('ERROR: token.txt does not exist. Create file token.txt in the same directory and'\
		'place Telegram Bot\'s token there. To get a token write to @botfather')
	sys.exit()
else:
	f.close()

bot = telebot.TeleBot(token)

def detect_language(text):
	avg = 0
	cnt = 0
	mx = 0
	for i in text:
		if i.isalpha():
			avg += ord(i)
			cnt += 1
			if mx < ord(i):
				mx = ord(i)
	if cnt > 0:
		avg /= cnt
	if abs(avg - 100) > abs(avg - 1000):
		if mx > 1104:
			return 'kk'
		else:
			return 'ru'
	return 'en'

def pr(sonj):
	print(json.dumps(sonj, indent=2))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#print(message.keys())
	bot.send_message(message.chat.id, "Send text in english, russian or kazakh, I will paraphrase it")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	x = message.text
	langs = [detect_language(x), 'pt', 'tr']
	for i in range(len(langs)):
		x = translate.google(x, langs[i], langs[(i+1) % len(langs)])
	bot.send_message(message.chat.id, 'Please wait, paraphrasing...')
	bot.reply_to(message, x)

bot.polling()