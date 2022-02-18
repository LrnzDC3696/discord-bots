from hata.discord.activity import ActivityRich, ACTIVITY_TYPES
from hata.discord.client import Client
from hata.ext.commands import setup_ext_commands
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
from hata.ext.slash import setup_ext_slash

from src import config

Client__1 = Client(
    token=config.CLIENT__1__TOKEN,
    client_id=config.CLIENT__1__ID,
    status=None,
    activity=ActivityRich("UwU", type_=ACTIVITY_TYPES.watching),
)
setup_ext_slash(Client__1)
setup_ext_commands(
    Client__1, config.CLIENT__1__PREFIX, default_category_name="Uncategorized"
)
Client.commands(
    SubterraneanHelpCommand(lambda _client, msg, _name: msg.author.color_at(msg.guild)),
    "help",
)


@Client__1.events
async def ready(client):
    print(f"{client:f} logged in.")


@Client__1.events
async def message_create(client, message):
    if message.author.is_bot:
        return

    if message.content == "ping":
        await client.message_create(message.channel, "pong")
