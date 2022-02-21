from hata.discord.client import Client
from src.constants import YAMETECH__GUILD


CLIENT: Client


@CLIENT.interactions(guild=YAMETECH__GUILD)
async def ping():
    return "Pong!"


@CLIENT.events
async def ready(client):
    print(f"{client:f} logged in.")
