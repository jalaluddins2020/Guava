import os
import json
import requests
import amqp_setup
from dotenv import load_dotenv  
load_dotenv()

twilioAccountSID = os.getenv("TWILIO_ACCOUNT_SID")
twilioAuthToken = os.getenv("TWILIO_AUTH_TOKEN")
monitorBindingKey='*.notify'

def receiveNotification():
    amqp_setup.check_setup()
    
    queue_name = "Notification"  

    # Set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    # It doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\n**************** Start of Notification ****************")
    print("\n\nReceived an notification from: " + __file__)
    processNotification(body)
    print() # print a new line feed

def processNotification(notificationMsg):
    print("\nPrinting the notification message received:")
    try:
        notification = json.loads(notificationMsg)
        print("\n-- JSON RECEIVED:", notification)
        acceptedListingID = str(notification["data"]["listingID"])
        sendSMS(acceptedListingID)
        print("\n\n**************** End of Notification ****************")

    except Exception as e:
        print("\n--NOT JSON RECEIVED:", e)
        print("\n--DATA:", notificationMsg)
    print()

def sendSMS(acceptedListingID):
    twilioUrl = "https://"+twilioAccountSID+":"+twilioAuthToken+"@api.twilio.com/2010-04-01/Accounts/"+twilioAccountSID+"/Messages.json"
    smsContent = {
                    "To": "+6596739311", 
                    "From": "+17579822788", 
                    "Body": "Hi! Your listing has been accepted, do check it out: http://0000:5001/listing/"+acceptedListingID
                }
    response = requests.post(twilioUrl,data=smsContent)
    smsStatusCode = response.status_code
    if smsStatusCode == 201:
        print("\nSMS sent successfully!")
    else:
        print("\nIssue with sending the SMS...")

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')    
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
