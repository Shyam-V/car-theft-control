import requests

def send_msg(text):
	token = "1171072467:AAHqz6QI90f1KjLRybL8uwYRZblIzAYSSnQ"
	chat_id = "573611170"

	url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
	results = requests.get(url_req)
	return results

send_msg("")