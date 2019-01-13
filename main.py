import json
import logging
import getpass
import os
import sys
import random
from instapy import InstaPy
from instapy.unfollow_util import follow_user, unfollow_user
from instapy.like_util import get_links_for_tag, check_link, get_tags

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
  'programmer'
]

with open('state.json') as f:
  state = json.load(f)

class Insta(InstaPy):
  def get_by_tag(self, tag, amount):
    links = get_links_for_tag(self.browser, tag, amount, False, True, None, self.logger)
    result = []
    for link in links:
      inappropriate, user_name, is_video, reason, scope = (
        check_link(self.browser,
                    link,
                    self.dont_like,
                    self.mandatory_words,
                    self.mandatory_language,
                    self.is_mandatory_character,
                    self.mandatory_character,
                    self.check_character_set,
                    self.ignore_if_contains,
                    self.logger)
      )
      try:
        tags = get_tags(self.browser, link)
      except:
        tags = []
      result.append({
        "username": user_name,
        "tags": tags
      })

    return result

  def follow_users(self, usernames):
    for username in usernames:
      follow_user(self.browser, "profile", self.username, username, None, self.blacklist, self.logger, self.logfolder)

  def unfollow_users_list(self, usernames):
    for username in usernames:
      unfollow_user(self.browser,
                    "profile",
                    self.username,
                    username,
                    None,
                    None,
                    self.relationship_data,
                    self.logger,
                    self.logfolder)

password = os.environ.get('INSTAGRAM_PASSWORD')
if not password:
  password = getpass.getpass('Password: ')

session = Insta('geekrodion', password)
session.login()
session.logger.setLevel(logging.WARNING)


users_to_follow_number = 20

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
  filtered_pack = [user for user in pack if user['username'] not in no_touch_users]

  no_touch_users += [user['username'] for user in filtered_pack]
  users += [{ 'username': user['username'], 'tags': user['tags'], 'search_tag': tag } for user in filtered_pack]

usernames = [user['username'] for user in users]
session.follow_users(usernames)
stop_loop = False
for user in users:
  if stop_loop: break

  print(user['search_tag'], ': ', user['username'])
  while True:
    action = input('i: ignore, r: reached, s: stop')
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