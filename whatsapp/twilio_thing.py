# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         from_='whatsapp:+14155238886',
         body='Hi Joe! Thanks for placing an order with us. We’ll let you know once your order has been processed and delivered. Your order number is O12235234',
         to='whatsapp:+15005550006'
     )

print(message.sid)
