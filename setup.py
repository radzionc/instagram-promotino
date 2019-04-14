import json

REACHED = []

ANSWERED = []

IGNORED = []

reached = [{ 'username': username, 'tags': [] } for username in REACHED]

state = {
  'reached': reached,
  'ignored': IGNORED,
  'answered': ANSWERED
}

with open('state.json', 'w') as f:
  json.dump(state, f, indent=4)

with open('influencers.json', 'w') as f:
  json.dump({}, f, indent=4)