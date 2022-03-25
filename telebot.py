import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '5195002024:AAFOVxloVJsi_NdnEh3Ex-YWJn0pWpdJB68'
    bot_chatID = '121792469' #526817194
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()
    
test = telegram_bot_sendtext("Testing Telegram bot")
print(test)