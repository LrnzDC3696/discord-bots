import os

#Loading Environment Variables
try:
  from dotenv import load_dotenv
  load_dotenv()
except ModuleNotFoundError:
  pass

#BOT STUFF
FLUPPUS_TOKEN  = os.getenv('FLUPPUS_TOKEN')
FLUPPUS_ID     = 820624250247446549
FLUPPUS_PREFIX = '.'

#NEKO STUFF
CAT_API_KEY = os.getenv('CAT_API_KEY')
