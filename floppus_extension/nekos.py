import os, random

from hata import Client, Embed, Guild, chunkify
from hata.ext.commands import Pagination
import hata.ext.asyncio

from config import CAT_API_KEY
from bot_utils.utils import get_event_color
from bot_utils.shared_data import TEST_GUILD


Floppus: Client

CAT_API_URL = 'https://api.thecatapi.com/v1'

async def get_cat(route, params):
  """requests the api for the given params"""
  headers = {'x-api-key': CAT_API_KEY}
  
  async with Floppus.http.get(CAT_API_URL+route, params = params, headers = headers) as response:
    cat_data = await response.json()
    return cat_data


def make_pages(cats, color):
  """makes pages for the cats given
  - adds footer and color
  """
  pages = []
  
  for x, cat in enumerate(cats):
    cat_url = cat['url']
    
    # Checks for breeds
    if breeds := cat.get('breeds'):
      desc = \
        f"\nBreed Name: {','.join(breed['name'] for breed in breeds)}"\
        f"\nBreed Id: {','.join(breed['id'] for breed in breeds)}"
    else:
      desc = ''
    
    # Checks for categories
    if categories := cat.get('categories'):
      category = \
        f"\nCategory Name: {','.join(str(category['name']) for category in categories)}"\
        f"\nCategory Id: {','.join(str(category['id']) for category in categories)}"
    else:
      category = ''
    
    # Appending
    cat_length = len(cats)
    pages.append(Embed('Here is your neko nya!', url = cat_url, color = color)
      .add_image(cat_url)
      .add_footer(f"Page: {x+1}/{cat_length}\nCat Id: {cat['id']} {desc} {category}"))
  
  if not pages:
    pages.append(Embed('GomenNyaSai !!!', 'There seems to be no neko for that.' , color = color))
  
  return pages


# Slash Area
IMAGE_TYPES = {'Png': 'png', 'Jpg': 'jpg', 'Gif': 'gif',}
ORDER_CHOICES = {'Descending': 'desc', 'Ascending': 'asc', 'Random': 'rand',}
CHOICES = {'Category':'category','Breed':'breed'}

# A main slash command
NEKOWO = Floppus.interactions(None, name='neko', description='neko stuff', is_global = True)

# Sub slash commands
@NEKOWO.interactions
async def breed_info(client, event, breed_id: ('str', 'What is the cat id?'),):
  """get the info of the breed"""
  yield
  
  color = get_event_color(event)
  breeds = await get_cat('/breeds/search', {'q':breed_id})
  
  if not breeds:
    await Pagination(client, event, Embed('GomenNyaSai !!!', 'There seems to be no neko for that. Try doing `/neko list breed`' , color = color))
    return
  
  pages = []
  print(breeds)
  breed_length = len(breeds)
  for x, breed in enumerate(breeds):
    pages.append(Embed(breed['name'], breed['description'], color = color, url = breed.get('wikipedia_url'))
      .add_field('Breed Id', breed['id'], True)
      .add_field('Traits'  , breed['temperament'], True)
      .add_footer(f"Page: {x+1}/{breed_length}")
      .add_image(f"https://cdn2.thecatapi.com/images/{breed['reference_image_id']}.jpg")
    )
    
  await Pagination(client, event, pages)


@NEKOWO.interactions
async def gimme(client, event,
    image_type : (IMAGE_TYPES, 'What type of image?') = None,
    limit: ('int', 'How many cats?') = 10,
    page : ('int', 'Jump to page..?') = None,
    order: (ORDER_CHOICES, 'In what order?') = None,
  ):
  """Gives you nekos"""
  yield
  
  params = {}
  
  if image_type is not None:
    params['mime_types'] = image_type
  if limit is not None:
    params['limit'] = limit
  if page is not None:
    params['page'] = page
  if order is not None:
    params['order'] = order
  
  cats  = await get_cat('/images/search', params)
  pages = make_pages(cats, get_event_color(event))
  
  await Pagination(client, event, pages)


@NEKOWO.interactions
async def list_(client, event,
    choice: (CHOICES, 'What do you want to list?'),
    limit: ('int', 'How many cats?') = 10,
    page : ('int', 'Jump to page..?') = None,
    order: (ORDER_CHOICES, 'In what order?') = None,
  ):
  """list the category or breed"""
  yield
  
  params = {}
  
  if limit is not None:
    params['limit'] = limit
  if page is not None:
    params['page'] = page
  if order is not None:
    params['order'] = order
  
  if choice == 'category':
    choice = 'categories'
  else:
    choice = 'breeds'
  
  pages = []
  stuff = await get_cat(f"/{choice}", params)
  
  string = []
  for num, dictionary in enumerate(stuff):
    string.append(f"{(num + 1):02}. __**Name:**__ {dictionary['name']}\n\t\t__**Id:**__ {dictionary['id']}\n")
  
  color = get_event_color(event)
  pages = [(Embed(f"Results for {choice}", details, color).add_footer(f"Page: {num+1}")) for num, details in enumerate(chunkify(string))]
  await Pagination(client, event, pages)


@NEKOWO.interactions
async def search(client, event,
    choice: (CHOICES, 'What do you wanna search for?'),
    id_  : ('str', 'The id of choice'),
    limit: ('int', 'How many cats?') = 10,
    page : ('int', 'Jump to page..?') = None,
    order: (ORDER_CHOICES, 'In what order?') = None,
  ):
  """by category or by breed"""
  yield
  
  params = {}
  params[f"{choice}_ids"] = id_
  
  if limit is not None:
    params['limit'] = limit
  if page is not None:
    params['page'] = page
  if order is not None:
    params['order'] = order
  
  cats  = await get_cat('/images/search', params)
  pages = make_pages(cats, get_event_color(event))
  
  await Pagination(client, event, pages)

