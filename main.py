import json
import logging
import getpass
import os
from instapy import InstaPy
from instapy.like_util import get_links_for_tag, check_link

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
    links = get_links_for_tag(self.browser, tag, amount, False, False, None, self.logger)
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
      print(user_name)

password = os.environ.get('INSTAGRAM_PASSWORD')
if not password:
  password = getpass.getpass('Password: ')

session = Insta(username='geekrodion', password=password, headless_browser=False)
session.login()
session.logger.setLevel(logging.WARNING)
print(session.get_by_tag('coding', 10))
