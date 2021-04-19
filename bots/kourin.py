from hata import Client
from hata.ext.commands import setup_ext_commands
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand

from config import KOURIN_PREFIX


Kourin : Client

setup_ext_commands(Kourin, KOURIN_PREFIX, default_category_name="Uncategorized",)
Kourin.commands(SubterraneanHelpCommand(
  lambda _client, msg, _name: msg.author.color_at(msg.guild)
  ),'help',
)
