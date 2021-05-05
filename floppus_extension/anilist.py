from hata import Client, Embed, chunkify
from hata.ext.commands import Pagination
from hata.backend.utils import to_json

from bot_utils.shared_data import TEST_GUILD
from bot_utils.utils import get_event_color


Floppus: Client
FLOPPUS = Floppus.interactions(None, name = 'Anilist', description = 'Animanga stuff', guild = TEST_GUILD)

ANILIST_URL = 'https://graphql.anilist.co'
HEADERS = {'content-type': 'application/json'}
MONTHS = {
  1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
  7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

def datetify(data):
  return f"{MONTHS.get(data['month'], '`Unknown Month`')}, {data['day'] or '`Unknown Day`'}, {data['year'] or '`Unknown Year`'}"

async def post_request(anilist_request, type_):
  async with Floppus.http.post(ANILIST_URL, headers = HEADERS, data = to_json(anilist_request)) as response:
    try:
      owo = (await response.json())['data'][type_]
      return owo
    except KeyError:
      return None
    except TypeError:
      return None


@FLOPPUS.interactions
async def anime(client, event, name: ('str', 'what is the anime title?')):
  """Searches anilist for the given anime"""
  yield
  
  anilist_request = {
    'query': \
      'query ($search: String, $type: MediaType) { '
        'Media(search: $search, type: $type, isAdult:false) { '
          'siteUrl '
          'title {romaji english native} '
          'coverImage {large} '
          'startDate {month day year} ' 
          'endDate {month day year} '
          'season '
          'episodes '
          'bannerImage '
          'status(version:2) '
          'description '
          'format ' 
        '} '
      '} '
      ,
    'variables': {'search':name, 'type':'ANIME'}
  }
  
  result = await post_request(anilist_request, 'Media')
  
  if result is None:
    yield 'Character not found'
    return
  
  #assigning to variable the things that will be used more than ones
  color = get_event_color(event)
  try:
    cover_img = result['coverImage']['large']
  except KeyError:
    cover_img = None
  
  lang = result['title']
  if not (title := lang['romaji']):
    if not (title := lang['english']):
      title = lang['native']
  
  titles     = '\n'.join([f"{key}: {value}" for key, value in lang.items()])
  start_date = datetify(result['startDate'] or 'Unknown')
  end_date   = datetify(result['endDate'] or 'Unknown')
  url        = result['siteUrl']
  banner_image = result['bannerImage']
  
  
  pages = []
  
  #front page
  pages.append(Embed(title,
      f"__**Other Titles**__:\n{titles}\n"
      f"\n__**Anime Type**__:\n{result['format']}\n"
      f"\n__**Status**__:\n{result['status'] or 'Unkown'}\n"
      f"\n__**Dates**__:\nStart Date: {start_date}\nEnd Date: {end_date}\n"
      f"\n__**Season**__:\n{result['season'] or 'Unknown'}\n"
      f"\n__**Episodes**__:\n{result['episodes'] or 'Unknown'}\n",
      color = color, url = url,
    ).add_image(banner_image).add_thumbnail(cover_img)
  )
  
  #description page
  for details in chunkify([result['description']]):
    pages.append(Embed(name, details, url = url, color = color).add_thumbnail(cover_img))
  
  #images page
  for image in [cover_img, banner_image]:
    if not image:
      pages.append(Embed(name, url = url, color = color).add_image(image))
  
  #adding page numbers
  for x, embed in enumerate(pages):
    embed.add_footer(f"Page: {x+1}/{len(pages)}")
  
  await Pagination(client, event, pages)


@FLOPPUS.interactions
async def character(client, event, name:('str', 'Who do you want to search for')):
  """Searches anilist for the given character"""
  yield
  
  anilist_request = {
    'query': \
      'query ($search: String) { '
        'Character(search: $search) { '
          'gender '
          'dateOfBirth {month day year} '
          'age '
          'siteUrl '
          'name {full} '
          'image {large} '
          'description '
        '} '
      '} ',
    'variables': {'search' : name}
  }
  
  result = await post_request(anilist_request, 'Character')
  if result is None:
    yield 'Character not found'
    return
  
  try:
    img = result['image']['large']
  except KeyError:
    img = None
  url = result['siteUrl']
  name = result['name']['full']
  color = get_event_color(event)
  
  if birthday := result.get('dateOfBirth', 'Unknown'):
    birthday = datetify(birthday)
  
  pages = []
  pages.append(
    Embed(name,
      f"__**Age**__:\n{result.get('age') or 'Unknown'}\n"
      f"\n__**Birthday**__:\n{birthday}\n"
      f"\n__**Gender**__:\n{result.get('gender') or 'Unknown'}",
      url = url, color = color,
    ).add_thumbnail(img)
  )
  
  for details in chunkify([result['description']]):
    pages.append(Embed(name, details, url = url, color = color).add_thumbnail(img))
  pages.append(Embed(name, url=url, color=color).add_image(img))
  
  for x, embed in enumerate(pages):
    embed.add_footer(f"Page: {x+1}/{len(pages)}")
  
  await Pagination(client, event, pages)
