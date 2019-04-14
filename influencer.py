import json
import sys

from instagram import execute

def update_state(new_state):
  with open('influencers.json', 'w') as f:
      json.dump(new_state, f, indent=4)

def main(session, config):
  with open('influencers.json') as f:
    state = json.load(f)

  influencer_name = sys.argv[1]
  if influencer_name not in state:
    followers = list(session.grab_followers(influencer_name, 'full'))
    state[influencer_name] = {
      'followers': followers,
      'reached': [],
      'ignored': []
    }
    update_state(state)

  influencer = state[influencer_name]
  users_to_check = list(set(influencer['followers']).difference(set(influencer['reached'] + influencer['ignored'])))
  
  
  stop_loop = False
  
  for index, user in enumerate(users_to_check):
    if stop_loop: break
    print(index, ' : ', user)
    while True:
      action = input('i(ignore), r(reached), s(stop) : ')
      if action in ['i', 'r', 's']:
        if action == 'i':
          state[influencer_name]['ignored'].append(user)
        elif action == 'r':
          state[influencer_name]['reached'].append(user)
        elif action == 's':
          stop_loop = True
          
        break
  print('Reached: ', len(state[influencer_name]['followers']))
  update_state(state)

execute(main)