import json
from constants import TAGS

with open('state.json') as f:
  state = json.load(f)

reached = state['reached']
answered = state['answered']

print('Reached: {0}'.format(len(reached)))
print('Responded: {0}%'.format(round((len(answered) * 100) / len(reached))))

reached_with_tags = [r for r in reached if len(r['tags']) > 0]
answered_with_tags = [u for u in reached_with_tags if u['username'] in answered]
all_tags_repeated = [u['tags'] for u in answered_with_tags]
all_tags = [tag for tags in all_tags_repeated for tag in tags]
unique_tags = list(set(all_tags))

tags = {}
for ut in unique_tags:
  tags[ut] = len([t for t in all_tags if t == ut])

all_possible_tags = []
for r in reached:
  all_possible_tags += r['tags']

tags_number = {}
for tag in all_possible_tags:
  if tag in tags_number:
    tags_number[tag] += 1
  else:
    tags_number[tag] = 1

for w in sorted(tags, key=tags.get, reverse=True):
  number = tags[w]
  if number < 2: continue
  
  tag = w[1:]
  string = '{0}: {1} {2:4.2f}'.format(tag, number, number /tags_number[w])
  if tag not in TAGS:
    print('\x1b[6;30;42m' + string + '\x1b[0m')
  else:
    print(string)

no_response_tags = set(TAGS) - set([ut[1:] for ut in unique_tags])
print('0 responses: ', ', '.join(no_response_tags))


