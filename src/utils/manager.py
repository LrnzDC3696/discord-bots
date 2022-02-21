import os

from hata.discord.client import ClientWrapper, Client
from hata.ext.extension_loader import EXTENSION_LOADER


class ClientExtManager:
    def __init__(self, exts_path):
        self.exts_path = os.path.abspath(exts_path)
        self.ext_client = {}
        self._get_exts_name()

    def _get_exts_name(self):
        for file_name in os.listdir(self.exts_path):
            if (not file_name.endswith(".py")) or (file_name.startswith("__")):
                continue

            file_name = file_name[:-3]
            self.ext_client[file_name] = set()

    def add_client(self, client, exts):
        for ext in set(exts):
            self.ext_client[ext].add(client)

    def add_clients(self, client_exts):
        for client, exts in client_exts:
            self.add_client(client, exts)

    def load_extensions(self):
        for ext, clients in self.ext_client.items():
            if not clients:
                continue
            EXTENSION_LOADER.load_extension(
                f"src.exts.{ext}", CLIENT=ClientWrapper(*clients)
            )

    def create_client(self, config_dict, exts):
        client = Client(**config_dict)
        self.add_client(client, exts)
        return client
