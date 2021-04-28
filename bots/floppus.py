from hata import Client
from hata.ext.slash import abort
from hata.ext.extension_loader import EXTENSION_LOADER

from bot_utils.shared_data import NEKO_MANCER, TEST_GUILD


Floppus : Client
FLOPPUS = Floppus.interactions(None, name='file', description='files stuff for owner', guild = TEST_GUILD)
FLOPPUS_EXT_PATH_NAME = 'floppus_extension'


FILES = {'all':'all'}

for ext in Floppus.extensions:
  name = ext.name_short
  FILES[name] = name

  
@FLOPPUS.interactions
async def load(client, event,
  choice: (FILES, 'Which file do you want to load?') = None,
  file_name: ('str', 'What is file name?') = None,
  ):
  """loads the chosen file"""
  
  #not owner
  if event.user != NEKO_MANCER:
    abort('Never gonna give you up, Never gonna let you down, Never gonna run this command for you')
  yield
  
  #checks
  if choice and file_name:
    abort('Pick only one you dummy')
  elif not (choice or file_name):
    abort('Give me something tho')
  
  #code
  file = choice or file_name
  
  if file == 'all':
    await EXTENSION_LOADER.load_all()
    yield 'All files are now loaded.'
    return
  
  try:
    EXTENSION_LOADER.load_extension(f'{FLOPPUS_EXT_PATH_NAME}.{file_name}')
    yield 'file has been loaded onee chan'
  except ModuleNotFoundError:
    yield "NANI!!!! that file does not exist is my ext folder"


@FLOPPUS.interactions
async def reload(client, event,
  choice: (FILES, 'Which file do you want to reload?') = None,
  file_name: ('str', 'What is file name?') = None,
  ):
  """Reloads the chosen file"""
  
  #not owner
  if event.user != NEKO_MANCER:
    abort('Never gonna give you up, Never gonna let you down, Never gonna run this command for you')
  yield
  
  #checks
  if choice and file_name:
    abort('Pick only one you dummy')
  elif not (choice or file_name):
    abort('Give me something tho')
  
  #code
  file = choice or file_name
  
  if file == 'all':
    await EXTENSION_LOADER.reload_all()
    yield 'All files are now loaded.'
    return
  
  try:
    EXTENSION_LOADER.reload(f'{FLOPPUS_EXT_PATH_NAME}.{file_name}')
    yield 'file has been loaded onee chan'
  except ModuleNotFoundError:
    yield "NANI!!!! that file does not exist is my ext folder"


@FLOPPUS.interactions
async def unload(client, event,
  choice: (FILES, 'Which file do you want to unload?') = None,
  file_name: ('str', 'What is file name?') = None,
  ):
  """Unloads the chosen file"""
  
  #not owner
  if event.user != NEKO_MANCER:
    abort('Never gonna give you up, Never gonna let you down, Never gonna run this command for you')
  yield
  
  #checks
  if choice and file_name:
    abort('Pick only one you dummy')
  elif not (choice or file_name):
    abort('Give me something tho')
  
  #code
  file = choice or file_name
  
  if file == 'all':
    await EXTENSION_LOADER.unload_all()
    yield 'All files are now loaded.'
    return
  
  try:
    EXTENSION_LOADER.unload(f'{FLOPPUS_EXT_PATH_NAME}.{file_name}')
    yield 'file has been loaded onee chan'
  except ModuleNotFoundError:
    yield "NANI!!!! that file does not exist is my ext folder"
