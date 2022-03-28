# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
         body='\n Hi there! Your listing has been accepted by a user. Do check it out now!. shorturl.at/kuyXY',
         from_='+17579822788',
         status_callback='http://postb.in/1234abcd',
         to='+6596739311'
     )

print(message.sid)