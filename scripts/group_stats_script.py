#!/usr/bin/python

from collections import defaultdict
import json
import os
import sys

input_dir = '/Users/kajibu/data/lab/gascrape/tmp/profiles/actors-100'
output_file = '/Users/kajibu/data/lab/gascrape/tmp/group_stats.txt'

print_interval = 10000

def get_binary_key(item, key):
  if key not in item or item[key] is None:
    return 'null'
  return 'ok'

def get_hireable_key(item):
  if 'hireable' not in item or item['hireable'] is None:
    return 'null'
  if item['hireable']:
    return 'yes'
  return 'no'

def get_key(item):
  name_key = get_binary_key(item, 'name')
  location_key = get_binary_key(item, 'location')
  email_key = get_binary_key(item, 'email')
  hireable_key = get_hireable_key(item)
  return '|'.join([name_key, location_key, email_key, hireable_key])

adict = defaultdict(int)
count = 0
for dirpath, dirnames, filenames in os.walk(input_dir):
  for filename in filenames:
    if count % print_interval == 0:
      print 'processed %d files' % count
      sys.stdout.flush()
    count += 1
    item = json.load(open(os.path.join(dirpath, filename)))
    adict[get_key(item)] += 1

with open(output_file, 'w') as fp:
  for key, count in adict.iteritems():
    name, location, email, hireable = key.split('|')
    print >> fp, {
        'name': name,
        'location': location,
        'email': email,
        'hireable': hireable,
        'count': count
    }

