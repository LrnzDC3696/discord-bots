from hata.discord.client import start_clients
from hata.discord.client.utils import wait_for_interruption
from hata.discord.activity import ActivityRich, ACTIVITY_TYPES
from src import config
from src.utils.manager import ClientExtManager


c1 = {
    "token": config.CLIENT__1__TOKEN,
    "client_id": config.CLIENT__1__ID,
    "status": None,
    "activity": ActivityRich("UwU", type_=ACTIVITY_TYPES.watching),
    "prefix": config.CLIENT__1__PREFIX,
    "extensions": ["slash", "commands_v2"],
}


def main():
    manager = ClientExtManager("src/exts")
    manager.create_client(c1, ["smh"])
    manager.load_extensions()

    start_clients()
    wait_for_interruption()


if __name__ == "__main__":
    main()
