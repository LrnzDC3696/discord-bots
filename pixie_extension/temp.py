from bot_utils.shared_data import GUILD__NEET_GUILD
from hata import Client

Pixie : Client

@Pixie.interactions(client=GUILD__NEET_GUILD)
async def temp(client, event):
  """temporary command"""
  
  await client.message_create(event, 'hi there!')
