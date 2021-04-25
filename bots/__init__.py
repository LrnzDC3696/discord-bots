import os

from hata import Client, start_clients, ActivityRich, ActivityTypes, ClientWrapper
from hata.ext.extension_loader import EXTENSION_LOADER

import config

#Clients
Floppus = Client(
  token     = config.FLUPPUS_TOKEN,
  client_id = config.FLUPPUS_ID,
  status    = None,
  activity  = ActivityRich('Boku no Pico', type_ = ActivityTypes.watching),
)

#All Clients
All = ClientWrapper()

#Loading Clients
EXTENSION_LOADER.add_default_variables(Floppus = Floppus, All = All)


#Extentions in bots 
print('-----main-----')
path = os.path.abspath('bots')

for file_name in os.listdir(path):
  
  if (not file_name.endswith('.py')) or file_name.startswith('__'):
    continue
  != 
  file_name = file_name[:-3]
  EXTENSION_LOADER.load_extension(f'bots.{file_name}', locked=True)
  
  print(f'Main extension {file_name} has been loaded')
print('-----done-----\n')


#Extensions in folders
print('-----ext-----')
path = os.path.abspath('.')

for folder_name in os.listdir(path):
  
  if not folder_name.endswith('_extension'):
    continue
    
  folder_path = os.path.join(path, folder_name)
  
  for file_name in os.listdir(folder_path):
    if not file_name.endswith('.py'):
      continue
        
    file_name = file_name[:-3]
    EXTENSION_LOADER.add(f'{folder_name}.{file_name}')
    
    print(f'Extension {file_name} has been loaded')
print('-----done-----\n')

#Loader
EXTENSION_LOADER.load_all()

