import json
import os
import logging
import getpass

from instapy import InstaPy
from instapy.unfollow_util import follow_user, unfollow_user
from instapy.like_util import get_links_for_tag, check_link, get_tags, like_image


class Instagram(InstaPy):
  def get_by_tag(self, tag, amount, no_touch_usernames=[]):
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
      if user_name in no_touch_usernames: continue
      try:
        like_image(self.browser, user_name, self.blacklist, self.logger, self.logfolder)
      except:
        print('fail_to_like_post')

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
      try:
        follow_user(self.browser, "profile", self.username, username, None, self.blacklist, self.logger, self.logfolder)
      except:
        print('fail to follow @{0}'.format(username))

  def unfollow_users_list(self, usernames):
    for username in usernames:
      try:
        unfollow_user(self.browser,
                      "profile",
                      self.username,
                      username,
                      None,
                      None,
                      self.relationship_data,
                      self.logger,
                      self.logfolder)
      except:
        print('fail to follow @{0}'.format(username))

def execute(func):
  with open('config.json') as f:
    config = json.load(f)

  username = os.environ.get('INSTAGRAM_USERNAME')
  if not username:
    username = getpass.getpass('Username: ')

  # get parameters: password and number of peoples to reach
  password = os.environ.get('INSTAGRAM_PASSWORD')
  if not password:
    password = getpass.getpass('Password: ')

  session = Instagram(username, password)
  session.login()
  session.logger.setLevel(logging.WARNING)

  func(session, config)

  session.browser.close()
