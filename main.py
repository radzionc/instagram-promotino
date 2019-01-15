import json
import logging
import getpass
import os
import sys
import random

from instagram import Instagram

TAGS = [
  'programming',
  'productivity',
  'uxdesign',
  'pomodorotechnique',
  'studyinghard',
  'softwareengineering',
  'webdesign',
  'uxui',
  'deepwork',
  'coding',
  'programmer',
  'examprep',
  'university'
]

with open('state.json') as f:
  state = json.load(f)

password = os.environ.get('INSTAGRAM_PASSWORD')
if not password:
  password = getpass.getpass('Password: ')

users_to_follow_number = 20
if len(sys.argv) > 1 and sys.argv[1]:
  users_to_follow_number = int(sys.argv[1])

session = Instagram('geekrodion', password)
session.login()
session.logger.setLevel(logging.WARNING)




tags = TAGS.copy()
random.shuffle(tags)

users = []
no_touch_users = state['ignored'] + [user['username'] for user in state['reached']]
for tag in tags:
  print('fetching for #', tag)
  if len(users) >= users_to_follow_number:
    users = users[:users_to_follow_number]
    break
  pack = session.get_by_tag(tag, 10)
  unique_pack = []
  for user in pack:
    usernames = [u['username'] for u in unique_pack]
    if user['username'] not in usernames:
        unique_pack.append(user)

  filtered_pack = [user for user in unique_pack if user['username'] not in no_touch_users]

  users += [{ 'username': user['username'], 'tags': user['tags'], 'search_tag': tag } for user in filtered_pack]

usernames = [user['username'] for user in users]
session.follow_users(usernames)
stop_loop = False
for index, user in enumerate(users):
  if stop_loop: break
  print(index, ' : ', user['search_tag'], ' : ', user['username'])
  while True:
    action = input('i(ignore), r(reached), s(stop) : ')
    if action in ['i', 'r', 's']:
      if action == 'i':
        state['ignored'].append(user['username'])
      elif action == 'r':
        state['reached'].append({
          'username': user['username'],
          'tags': user['tags']
        })
      elif action == 's':
        stop_loop = True
        
      break

with open('state.json', 'w') as f:
  json.dump(state, f, indent=4)
session.unfollow_users_list(usernames)