from hata import ClientWrapper

All : ClientWrapper

@All.events
async def ready(client):
  print(f'{client:f} logged in')
