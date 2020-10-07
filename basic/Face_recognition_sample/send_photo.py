import telegram

token = "1171072467:AAHqz6QI90f1KjLRybL8uwYRZblIzAYSSnQ"
bot = telegram.Bot(token)
print(bot.get_me())
# if bot.get_updates():
chat_id = "573611170"
photo = "/home/shyam/Pictures/A Final Eligibility Check.png"
pic = 'https://bitcoin.org/img/icons/opengraph.png'
bot.send_photo(chat_id, photo=open(photo, 'rb'))

# else:
	# print("Empty list. Please chat with the bot")
