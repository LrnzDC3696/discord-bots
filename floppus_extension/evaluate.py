import json

from bot_utils.utils import get_msg_color, parse_code_content
from hata import Client, Embed, Guild

Floppus : Client

PISTON_BASE_URL = 'https://emkc.org/api/v2/piston/'
TEST_GUILD = Guild.precreate(388267636661682178)

cache = {}

async def store():
  async with Floppus.http.get(PISTON_BASE_URL + 'runtimes') as response:
    for lang in await response.json():
      if lang['language'] == 'python' and lang['version'] > '2':
        cache['python'] = lang['version']
        break

async def main_eval(message, language, code):
  
  if not cache:
    await store()
  
  data = {
    'language': language,
    'version' : cache[language],
    'files'   : [{'content':code}],
  }
  
  async with Floppus.http.post('https://emkc.org/api/v2/piston/execute', data = json.dumps(data)) as response:
    data = await response.json()
    
    return Embed(f"Your eval job has completed with return code {data['run']['code']}",
      f"{data['run']['output'] or '[No Output]'}",
      color = get_msg_color(message))
    .add_author(message.author.avatar_url_as(), message.author.full_name)


@Floppus.commands(aliases = ['e','py','python'])
async def eval_(client, message, code):
  code, is_exception = parse_code_content(code)
  
  if is_exception:
    await client.message_create(message.channel, embed = Embed('Parsing error', code, color = get_msg_color(message)))
    return
  
  with client.keep_typing(message.channel):
    return await main_eval(message, 'python', code)
