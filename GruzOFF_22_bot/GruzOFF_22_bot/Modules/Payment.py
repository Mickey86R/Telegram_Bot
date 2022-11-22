from yookassa import Configuration, Webhook 
 
Configuration.configure_auth_token('<Bearer Token>') 
 
response = Webhook.add({ 
    "event": "payment.succeeded", 
    "url": "https://www.example.com/notification_url", 
})

