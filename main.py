import json
import logging
import getpass
import os
import sys
import random

from instagram import Instagram


with open('state.json') as f:
  state = json.load(f)

with open('config.json') as f:
  config = json.load(f)
  TAGS = config['tags']

username = os.environ.get('INSTAGRAM_USERNAME')
if not username:
  username = getpass.getpass('Username: ')

# get parameters: password and number of peoples to reach
password = os.environ.get('INSTAGRAM_PASSWORD')
if not password:
  password = getpass.getpass('Password: ')

users_to_follow_number = 15r
if len(sys.argv) > 1 and sys.argv[1]:
  users_to_follow_number = int(sys.argv[1])

# initialize session
session = Instagram(username, password)
session.login()
session.logger.setLevel(logging.WARNING)

# prepare tags
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

reached_number = 0
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
        reached_number += 1
      elif action == 's':
        stop_loop = True
        
      break

print('users reached: {0}'.format(reached_number))

try:
  with open('state.json', 'w') as f:
    json.dump(state, f, indent=4)
except:
  print('fail to write json in state.json')
  with open('new_state.json', 'w') as f:
    json.dump(state, f, indent=4)
  print('find new state in new_state.json')
  
session.unfollow_users_list(usernames)
session.browser.close()