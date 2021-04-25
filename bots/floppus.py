from hata import Client
from hata.ext.slash import setup_ext_slash
from hata.ext.commands import setup_ext_commands
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand

from config import FLUPPUS_PREFIX


Floppus : Client

setup_ext_slash(Floppus)
setup_ext_commands(Floppus, FLUPPUS_PREFIX, default_category_name="Uncategorized",)

Floppus.commands(SubterraneanHelpCommand(
  lambda _client, msg, _name: msg.author.color_at(msg.guild)
  ),'help',)
