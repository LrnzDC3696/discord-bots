import os
import random

from hata import Client, Embed, Guild
from hata.ext.commands import Pagination
import hata.ext.asyncio

from cat import Client as CatClient
from config import CAT_API_KEY
from bot_utils.utils import get_event_color
from bot_utils.shared_data import TEST_GUILD


Floppus: Client
MyNeko = CatClient(CAT_API_KEY)


ORDER_CHOICES = {
  'Descending' : 'desc',
  'Ascending'  : 'asc' ,
  'Random'     : 'rand',
 }

@Floppus.interactions(guild=TEST_GUILD)
async def neko(client, event,
    limit: ('int', 'How many cats?') = 10,
    page : ('int', 'Jump to page..?') = 0,
    order: (ORDER_CHOICES, 'In what order?') = 'rand',
  ):
  """Gives you nekos"""
  yield
  
  cats = await MyNeko.get_cat(limit, page, order)
  
  color = get_event_color(event)
  pages = []
  
  for x, cat in enumerate(cats):
    
    if breeds := cat.breeds:
      desc = \
        f', Breed Name: {",".join(breed.name for breed in breeds)}'\
        f', Breed Id: {",".join(breed.id for breed in breeds)}'
    else:
      desc = ''
    
    pages.append(Embed('Here is your neko nya!', url = cat.url, color = color)\
      .add_image(cat.url)\
      .add_footer(f'Page: {x+1}/{len(cats)}\nCat Id: {cat.id} {desc}')
    )
  
  await Pagination(client, event, pages)


@Floppus.commands
async def cat_gui(client, message):
  """
  The cat gui for the cat stuff
  """


@Floppus.commands
async def find_breed(client, message):
  """
  Finds the given breed of the cat
  """


@Floppus.commands
async def find_cat(client, message):
  """
  Finds that cat using the given id of the cat
  """
