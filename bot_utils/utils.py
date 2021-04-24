def colourfunc(message):
  return message.author.color_at(message.guild)

def colourfunc2(event):
  return event.user.color_at(event.guild)
