import os

# Loading Environment Variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

# BOT STUFF
CLIENT__1__TOKEN = os.getenv("CLIENT__1__TOKEN")
CLIENT__1__ID = 944224160782123009
CLIENT__1__PREFIX = "1."
