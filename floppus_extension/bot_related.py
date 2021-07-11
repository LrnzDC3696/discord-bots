from sys import implementation
from datetime import datetime

from hata import Client, Embed, GUILDS, USERS, CLIENTS, __version__, time_to_id
from hata.ext.commands import Pagination, Closer

from bot_utils.shared_data import (
  CHANNEL__BOT_BUG_REPORTS, CHANNEL__BOT_SUGGESTIONS,
  GUILD__NEET_GUILD, GUILD__NEKO_DUNGEON, INVITE__SUPPORT_GUILD,
  LINK__SOURCE, LINK__HATA, LINK__RICK_ROLL, LINK__PYTHON
)
from bot_utils.utils import get_event_color, get_files_and_code_lines_count, chad_time_delta


# Something errors in android
import os, sys
sys.stderr = open(os.devnull, "w")
try:
  from psutil import virtual_memory
finally:
  sys.stderr = sys.__stderr__
#####

Floppus : Client
BOT_STUFF = Floppus.interactions(None, name = 'Bot', description = 'Bot Related Slash', is_global = True)
ALIVE_TIME = datetime.now()

BOT_INVITE_BASE_URL = 'https://discord.com/oauth2/authorize?client_id={}&permissions={}&scope=bot'

FILE_COUNT, CODE_LINES = get_files_and_code_lines_count('.')

NON_CATEGORIZE_CMD_ICON = ':white_medium_small_square:'
MAIN_COMMANDS_ICON = ':white_medium_square:'
SUB_COMMANDS_ICON = ':white_small_square:'


def formatify(byte):
  """formats your bytes"""
  for unit in 'KB', 'MB', 'GB':
    byte /= 1024.
    if byte < 1024.:
      break
  
  return f"{byte:.02f} {unit}"


@BOT_STUFF.interactions
async def info(client, event):
  """Get your information here"""
  yield
  
  name = client.full_name
  icon = client.avatar_url_as(size = 4096)
  color = get_event_color(event)
  support_guild_url = INVITE__SUPPORT_GUILD.url
  
  pages = []
  pages.append(Embed(name,)
    .add_field('Owner', f"{','.join([user.full_name for user in client.owners])}", True)
    .add_field('Support Guild', f"[{GUILD__NEET_GUILD.name}]({support_guild_url})", True)
    .add_field('Ping Pong', f"{client.gateway.latency*1000.:.0f} ms", True)
    .add_field('Guild Count', f"{len(GUILDS):,}", True)
    .add_field('User Count', f"{len(USERS):,}", True)
    .add_field('Command Count', f"{client.commands.command_count:,}", True)
    .add_field('Slash Count', f"{len(client.slasher.command_id_to_command):,}", True)
    .add_thumbnail(icon)
  )
  
  
  virtual_mem = virtual_memory()
  version = implementation.version
  pages.append(Embed(name,)
    .add_field('Uptime', f"{chad_time_delta((datetime.now() - ALIVE_TIME), '{d}D {h}H {m}M')}", True)
    .add_field('Shards', f"{client.shard_count:,}")
    .add_field('Source', f"[Github]({LINK__SOURCE})",True)
    .add_field('Python Ver', f"[Python {version[0]}.{version[1]}]({LINK__PYTHON})", True)
    .add_field('Lib Ver', f"[Hata {__version__}]({LINK__HATA})", True)
    .add_field('Memory Usage', f"{formatify(virtual_mem.used)}/{formatify(virtual_mem.total)}", True)
    .add_field('Code', f"Files: {FILE_COUNT:,}\nCode Lines: {CODE_LINES:,}", True)
    .add_thumbnail(icon)
  )
  
  pages.append(Embed(name).add_image(icon))
  pages.append(Embed('Join Us! Click me!', url = support_guild_url)
    .add_image(f"https://discordapp.com/api/guilds/{GUILD__NEET_GUILD.id}/widget.png?style=banner4")
  )
  
  color = get_event_color(event)
  page_length = len(pages)
  for page_num, page in enumerate(pages):
    page.add_footer(f"Page {page_num + 1}/{page_length}")
    page.color = color
  
  await Pagination(client, event, pages)


@BOT_STUFF.interactions(name = 'help')
async def help_(client, event):
  """Gives you an embeded help for the slash commands"""
  
  color = get_event_color(event)
  pages = []
  
  for slashes in client.slasher.command_id_to_command.values():
    embed = Embed(f"{MAIN_COMMANDS_ICON} {slashes.name.capitalize()}",
      f">>> {slashes.description}",
    )
    
    for slash in slashes._sub_commands.values():
      embed.add_field(
        f"{SUB_COMMANDS_ICON} {slash.name.capitalize()}", f">>> {slash.description}"
      )
    
    pages.append(embed)
  
  page_length = len(pages)
  for page_num, page in enumerate(pages):
    page.add_footer(f"Page {page_num + 1}/{page_length}")
    page.color = color
    
  await Pagination(client, event, pages)


@BOT_STUFF.interactions
async def invite(client, event, choice: (
  {
    'Admin Perms' : BOT_INVITE_BASE_URL.format(Floppus.id, 8),
    'Mod Perms'   : BOT_INVITE_BASE_URL.format(Floppus.id, 2081418487),
    'Simple Perms': BOT_INVITE_BASE_URL.format(Floppus.id, 2148005952)
  },
  'What kind of link do you want?')
):
  """Gives you an invite link for the bot"""
  author = event.user
  await Closer(client, event,
    Embed('Here is the link', 'I hope to see you in your guild', color = get_event_color(event), url = choice)
      .add_author(author.avatar_url, author.full_name)
  )


@BOT_STUFF.interactions
async def report_bug(client, event, msg:('str','Your Report')):
  """Report a bug to the owner"""
  author = event.user
  guild = event.guild
  color = get_event_color(event)
  
  await client.message_create(CHANNEL__BOT_BUG_REPORTS,
    Embed('Bug Report', msg, color, timestamp = datetime.now())
      .add_author(author.avatar_url, author.full_name)
      .add_field('User Info', f"Id {author.id}", True)
      .add_field('From ', f"{guild.name} `{guild.id}`", True)
  )
  
  yield await Closer(client, event, Embed('Thank you for letting us know !!!', color = color))


@BOT_STUFF.interactions
async def suggest(client, event, msg:('str','Your Suggestion')):
  """Suggest stuff to the owner"""
  author = event.user
  guild = event.guild
  color = get_event_color(event)

  await client.message_create(CHANNEL__BOT_SUGGESTIONS,
    Embed('Suggestion', msg, color, timestamp = datetime.now())
      .add_author(author.avatar_url, author.full_name)
      .add_field('User Info', f"Id {author.id}", True)
      .add_field('From ', f"{guild.name} `{guild.id}`", True)
  )

  yield await Closer(client, event, Embed('Thank you for letting us know !!!', color = color))
