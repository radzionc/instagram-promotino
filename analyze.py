import json
from constants import TAGS

with open('state.json') as f:
  state = json.load(f)

reached = state['reached']
answered = state['answered']

print('Reached: {0}'.format(len(reached)))
print('Responded: {0}%'.format(round(len(answered) / len(reached) * 100)))

reached_with_tags = [r for r in reached if len(r['tags']) > 0]
answered_with_tags = [u for u in reached_with_tags if u['username'] in answered]
all_tags = [u['tags'] for u in answered_with_tags]
unique_tags = [tag for tags in all_tags for tag in tags]

