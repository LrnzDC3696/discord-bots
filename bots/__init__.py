import os, config

from hata import Client, start_clients, ActivityRich, ActivityTypes, ClientWrapper
from hata.ext.extension_loader import EXTENSION_LOADER
from hata.ext.slash import setup_ext_slash
from hata.ext.commands import setup_ext_commands
from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand


#Clients
Floppus = Client(token = config.FLUPPUS_TOKEN, client_id = config.FLUPPUS_ID, status = None,
  activity = ActivityRich('Boku no Pico', type_ = ActivityTypes.watching),)

Pixie = Client(token = config.PIXIE_TOKEN, client_id = config.PIXIE_ID, status = None,
  activity = ActivityRich('Mahouka', type_ = ActivityTypes.watching),)

#Floppus
setup_ext_slash(Floppus)
setup_ext_commands(Floppus, config.FLUPPUS_PREFIX, default_category_name = 'Uncategorized',)
Floppus.commands(SubterraneanHelpCommand(lambda _client, msg, _name: msg.author.color_at(msg.guild)),'help',)

#Pixie
setup_ext_slash(Pixies)
setup_ext_commands(Pixie, config.FLUPPUS_PREFIX, default_category_name = 'Uncategorized',)
Pixie.commands(SubterraneanHelpCommand(lambda _client, msg, _name: msg.author.color_at(msg.guild)),'help',)


#All Clients
All = ClientWrapper()

#Loading Clients
EXTENSION_LOADER.add_default_variables(Floppus = Floppus, Pixie = Pixie, All = All)


#Extensions in folders
print('-----ext-----')

path = os.path.abspath('.')
for folder_name in os.listdir(path):
  if not folder_name.endswith('_extension'):
    continue
  
  EXTENSION_LOADER.add(folder_name)
  print(f"Extensions in {folder_name} has been loaded")

EXTENSION_LOADER.load_all()
print('-----done-----\n')


#Extentions in bots 
print('-----main-----')
path = os.path.abspath('bots')

for file_name in os.listdir(path):
  if (not file_name.endswith('.py')) or (file_name.startswith('__')):
    continue
  
  file_name = file_name[:-3]
  EXTENSION_LOADER.load_extension(f"bots.{file_name}", locked = True)
  
  print(f"Main extension {file_name} has been loaded")
print('-----done-----\n')
