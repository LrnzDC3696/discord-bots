import os

try:
  from dotenv import load_dotenv
  load_dotenv()
except ModuleNotFoundError:
  pass

#BOT STUFF
KOURIN_TOKEN  = os.getenv('KOURIN_TOKEN')
KOURIN_ID     = 820624250247446549
KOURIN_PREFIX = 'r.'
