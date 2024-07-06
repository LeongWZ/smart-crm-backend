import os
import ngrok

def connect_to_ngrok():
    # Establish connectivity
    listener = ngrok.forward(8000, authtoken_from_env=True, domain=os.getenv("NGROK_DOMAIN"))

    # Output ngrok url to console
    print(f"Ingress established at {listener.url()}")