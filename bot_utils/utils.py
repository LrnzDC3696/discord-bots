import os
import pathlib
import codecs


def chad_time_delta(delta, pattern):
  """Beautifies your timedelta"""
  d = {'d': delta.days}
  d['h'], rem = divmod(delta.seconds, 3600)
  d['m'], d['s'] = divmod(rem, 60)
  
  return pattern.format(**d)


def get_msg_color(message):
  """Return the color of the user in the guild from the message"""
  return message.author.color_at(message.guild)


def get_event_color(event):
  """Return the color of the user in the guild from the event"""
  return event.user.color_at(event.guild)


def get_code_lines(path, file):
  """Returns the line count of the given file"""
  total = 0
  
  with codecs.open(f"./{pathlib.PurePath(path, file)}", 'r', 'utf-8') as file:
    for line in file:
      line = line.strip()
      
      if len(line) == 0 or line.startswith('#'):
        continue
      
      total += 1
  
  return total


def get_files_and_code_lines_count(start_folder):
  """Return the folder count and over all code lines"""
  codes_count = 0
  files_count = 0
  
  for path, _, files in os.walk(start_folder):
    for file_name in files:
      if file_name.endswith('.py'):
        codes_count += get_code_lines(path, file_name)
        files_count += 1
  
  return files_count, codes_count


#----- Credits -----
#https://github.com/HuyaneMatsu/Koishi/blob/7256ae77c35391e13528211d99e4ae22df91b6a0/bot_utils/interpreter.py#L173
import re

LINE_START  = re.compile('[ \t]*')
BLOCK_START = re.compile('(```|`|)(.*?)?(```|`|)')
PYTHON_RP   = re.compile('(?:python|py|)[ \t]*',re.I)
ENDER_1_RP  = re.compile('[^\\\]`')
ENDER_3_RP  = re.compile('[^\\\]```')

def parse_code_content(content, no_code_output=None):
  """Parse the code from the content"""
  lines = content.splitlines()
  
  if not lines:
    return 'No content was provided', True
    
  line = lines[0]
  starter, center, ender=BLOCK_START.fullmatch(line).groups()
  
  if starter:
    
    if ender:
      
      if starter != ender:
        return '1 code line starter should be same long as it\'s ender.', True
      else:
        lines = [center]
      
    else:
      lang_match = PYTHON_RP.fullmatch(center)
      
      if lang_match is None:
        return 'Invalid langauge', True
      else:
        del lines[0]
        
        if len(starter)==1:
          pattern=ENDER_1_RP
        else: #3
          pattern=ENDER_3_RP
        
        index=0
        ln=len(lines)
        
        while index<ln:
          line=lines[index]
          
          if line.startswith(starter):
            del lines[index:]
            break
          
          matched=pattern.search(line)
          
          if matched is None:
            index=index+1
            continue
          
          line=line[:matched.start()+1]
          lines[index]=line
          index+=1
          
          del lines[index:]
          break
        
        else:
          return 'Code block was never ended.', True
          
  index=len(lines)
  
  while index:
    index=index-1
    line=lines[index]
    start=LINE_START.match(line).end()
    
    if start!=len(line) and line[0]!='#':
      continue
    
    del lines[index]
    
  if not lines:
    return no_code_output, True
    
  return '\n'.join(lines), False
#----- Credits -----
