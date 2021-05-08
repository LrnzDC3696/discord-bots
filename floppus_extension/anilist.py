from hata import Client, Embed, chunkify, Color
from hata.ext.commands import Pagination
from hata.backend.utils import to_json

from bot_utils.shared_data import TEST_GUILD
from bot_utils.utils import get_event_color


Floppus: Client

ANILIST = Floppus.interactions(None, name = 'Anilist', description = 'Animanga stuff', is_global = True)

ANILIST_COLOR = Color.from_html('#3498DB')
ANILIST_URL = 'https://graphql.anilist.co'
ANILIST_LOGO = 'https://anilist.co/img/logo_al.png'

MONTHS = {
  1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
  7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}

class NotFound(Exception):
  pass

class ApiError(Exception):
  pass

def datetify(data):
  """Turns a dict into a datetime styled str in the format of MM, DD, YYY"""
  return f"{MONTHS.get(data['month'], '???')}, {data['day'] or '??'}, {data['year'] or '????'}"

async def post_request(anilist_request, type_):
  """Posts the requests"""
  async with Floppus.http.post(ANILIST_URL, headers = {'content-type': 'application/json'}, data = to_json(anilist_request)) as response:
    stats = response.status
    if stats == 200:
      return (await response.json())['data'][type_]
    elif stats == 404:
      raise NotFound
    elif stats >= 500:
      raise ApiError

def chadify(pages, color = ANILIST_COLOR, url = None):
  """Adds pages and color to the embed to make your embed look chad"""
  page_length = len(pages)
  
  for page_num, embed in enumerate(pages):
    embed.add_footer(f"Anilist | Page: {page_num+1}/{page_length}", ANILIST_LOGO)
    embed.color = color
    if url is not None:
      embed.url = url
  
  return pages


@ANILIST.interactions
async def anime(client, event, title: ('str', 'what is the anime title?')):
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
    'variables': {'search':title, 'type':'ANIME'}
  }
  
  try:
    result = await post_request(anilist_request, 'Media')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find an anime with that title gomen...')
    return
  
  # Assigning to variables the things that will be used more than ones
  lang  = result['title']
  
  title = lang['romaji'] or lang['english'] or lang['native']
  titles = '\n'.join([f"__{key}__: {value}" for key, value in lang.items()])
  
  start_date = datetify(result['startDate'])
  end_date   = datetify(result['endDate'])
  
  cover_img  = result['coverImage']['large']
  banner_image = result['bannerImage']
  
  pages = []
  
  # Front page
  pages.append(Embed(title
    ).add_field('Other Titles', titles , True
    ).add_field('Anime Type'  , result['format'] , True
    ).add_field('Status'      , result['status'] , True
    ).add_field('Dates'       , f"Start Date: {start_date}\nEnd Date: {end_date}" , True
    ).add_field('Season'      , result['season'] or 'Unknown'   , True
    ).add_field('Episodes'    , result['episodes'] or 'Unknown' , True
    ).add_image(banner_image).add_thumbnail(cover_img)
  )
  
  # Description page
  for details in chunkify([result['description']]):
    pages.append(Embed(title, details).add_thumbnail(cover_img))
  
  # Images page
  for image in [cover_img, banner_image]:
    if image:
      pages.append(Embed(title).add_image(image))
  
  await Pagination(client, event, chadify(pages, get_event_color(event), result['siteUrl']))


@ANILIST.interactions
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
  
  try:
    result = await post_request(anilist_request, 'Character')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find a character with that name gomen...')
    return
  
  # Assign
  img = result['image']['large']
  name = result['name']['full']
  
  pages = []
  # Front Page
  pages.append(
    Embed(name
    ).add_field('Age'     , result['age'] or 'Unknown' , True
    ).add_field('Birthday', datetify(result['dateOfBirth']) , True
    ).add_field('Gender'  , result['gender'] or 'Unknown', True
    ).add_thumbnail(img)
  )
  
  # Details
  for details in chunkify([result['description']]):
    pages.append(Embed(name, details).add_thumbnail(img))
  
  # Images
  pages.append(Embed(name).add_image(img))
  
  await Pagination(client, event, chadify(pages, get_event_color(event), result['siteUrl']))


@ANILIST.interactions
async def manga(client, event, title: ('str','what is the manga title?')):
  """Searches anilist for the given manga"""
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
          'volumes '
          'chapters '
          'bannerImage '
          'status(version:2) '
          'description '
          'format ' 
        '} '
      '} '
      ,
    'variables': {'search':title, 'type':'MANGA'}
  }
  
  try:
    result = await post_request(anilist_request, 'Media')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find a manga with that title gomen...')
    return
  
  # Assigning to variable the things that will be used more than ones
  cover_img = result['coverImage']['large']
  banner_image = result['bannerImage']
  
  lang = result['title']
  title = lang['romaji'] or lang['english'] or lang['native']
  titles = '\n'.join([f"__{key}__: {value}" for key, value in lang.items()])
  
  start_date = datetify(result['startDate'] or 'Unknown')
  end_date   = datetify(result['endDate'] or 'Unknown')
  
  pages = []
  
  # Front page
  pages.append(Embed(title
    ).add_field('Titles'    , titles, True
    ).add_field('Manga Type', result['format'], True
    ).add_field('Status'    , result['status'] or 'Unkown', True
    ).add_field('Dates'     , f"Start Date: {start_date}\nEnd Date: {end_date}", True
    ).add_field('Season'    , result['season'] or 'Unknown', True
    ).add_field('Volumes'   , result['volumes'] or 'Unknown', True
    ).add_field('Chapters'  , result['chapters'] or 'Unknown', True
    ).add_image(banner_image).add_thumbnail(cover_img)
  )
  
  # Description page
  for details in chunkify([result['description']]):
    pages.append(Embed(name, details).add_thumbnail(cover_img))
  
  # Images page
  for image in [cover_img, banner_image]:
    if image:
      pages.append(Embed(name).add_image(image))
  
  await Pagination(client, event, chadify(pages, get_event_color(event), result['siteUrl']))


@ANILIST.interactions
async def staff(client, event, name:('str', 'What is the staff name?')):
  """Searched anilist for the given staff"""
  yield
  
  anilist_request = {
    'query' : \
      'query ($search: String) { '
        'Staff(search: $search) { '
          'name {full} '
          'languageV2 '
          'image {large} '
          'description '
          'gender '
          'age '
          'siteUrl '
          'favourites '
          'characters {nodes {name{full} image{large} siteUrl}}'
        '} '
      '} ',
    'variables' : {'search':name}
  }
  
  try:
    result = await post_request(anilist_request, 'Staff')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find the staff with that name gomen...')
    return
  
  # Assign
  name = result['name']['full']
  image = result['image']['large']
  url = result['siteUrl']
  
  # Front Page
  pages = []
  pages.append(Embed(name, url = url
    ).add_field('Primary Language', result['languageV2'], True
    ).add_field('Age'    , result['age'], True
    ).add_field('Gender' , result['gender'], True
    ).add_field('Favourite By', f"{result['favourites']} Users", True
    ).add_field('Related Characters', 'at next page/s', True
    ).add_thumbnail(image)
  )
  
  pages.append(Embed(name, f"**Description**:\n{result['description']}\n"))
  
  # Characters
  characters = result['characters']['nodes']
  for character in characters:
    pages.append(Embed(character['name']['full'], url = character['siteUrl']
    ).add_image(character['image']['large']).add_author(image, name)
  )
  
  # Image
  pages.append(Embed(name, url = url).add_image(image))
  
  await Pagination(client, event, chadify(pages, get_event_color(event)))


@ANILIST.interactions
async def studio(client, event, name:('str', 'What is the studio name?')):
  """Searches anilist for the given studio"""
  yield
  
  anilist_request = {
    'query': \
      'query ($search: String) { '
        'Studio(search: $search) { '
          'name '
          'siteUrl '
          'favourites '
          'media (isMain: true, sort: TITLE_ENGLISH) {nodes {title {romaji} siteUrl coverImage {large}}} '
        '} '
      '} ',
    'variables': {'search' : name}
  }
  
  try:
    result = await post_request(anilist_request, 'Studio')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find a studio with that name gomen...')
    return
  
  # Assign
  name = result['name']
  
  # Pages
  pages = []
  pages.append(Embed(name, url = result['siteUrl']
    ).add_field('Favourite by', f"{result['favourites']} Users"
    ).add_field('Related Anime', f"\nAnimes Made by {name} at next page"
    )
  )
  
  # -Anime
  animes = result['media']['nodes']
  for anime in animes:
    pages.append(Embed(anime['title']['romaji'], url = anime['siteUrl']).add_image(anime['coverImage']['large']))
  
  await Pagination(client, event, chadify(pages, get_event_color(event)))


@ANILIST.interactions
async def user(client, event, name: ('str','What it the user name?')):
  """Searches anilist for the given user"""
  yield
  
  anilist_request = {
    'query': \
      'query ($search: String) { '
        'User(search: $search) { '
          'name '
          'about '
          'avatar {large} '
          'bannerImage '
          'siteUrl '
          'statistics { '
            'anime {count minutesWatched episodesWatched}'
            'manga {count chaptersRead} '
          '} '
        '} '
      '} ',
    'variables': {'search' : name}
  }
  
  try:
    result = await post_request(anilist_request, 'User')
  except ApiError:
    yield Embed('Oops...', 'There seems to be a problem with the api right now try again later!')
    return
  except NotFound:
    yield Embed('Not Found', 'I cannot find a user with that name gomen...')
    return
  
  # Assign
  name = result['name']
  banner_image = result['bannerImage']
  avatar = result['avatar']['large']
  
  info_dict = result['statistics']
  # -Anime
  ani_dict = info_dict['anime']
  anime_count = ani_dict['count']
  anime_watch = ani_dict['episodesWatched']
  days_watched = f"{(ani_dict['minutesWatched'] / (60*24)):.2f}"
  # -Manga
  manga_dict = info_dict['manga']
  manga_count = manga_dict['count']
  manga_reads = manga_dict['chaptersRead']
  
  # Pages
  pages = []
  pages.append(Embed(name
    ).add_field('About', result['about'] or 'Nothing', True
    ).add_field('Anime Stats', \
      f"__No. of anime watched__: {anime_count}\n"
      f"__No. of episodes watched__: {anime_watch}\n"
      f"__No. of days watching anime__: {days_watched}\n", True
    ).add_field('Manga Stats', \
      f"__No. of manga reads__: {manga_count}\n"
      f"__No. of chapters reads__: {manga_reads}\n", True
    ).add_thumbnail(avatar).add_image(banner_image)
  )
  
  # Images
  for image in [avatar, banner_image]:
    if image:
      pages.append(Embed(name).add_image(image))
  
  await Pagination(client, event, chadify(pages, get_event_color(event), result['siteUrl']))
