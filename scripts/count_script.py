#!/usr/bin/python

import json
import os

download_dir = '/Users/kajibu/data/lab/gascrape/tmp/profiles/actors-100'

keys = ['name', 'company', 'location', 'email', 'hireable']
counts = {
    'total': 0,
    'found': 0,
}
for key in keys:
  counts[key] = 0

dirs1 = os.listdir(download_dir)
for dir1 in dirs1:
  path1 = '%s/%s' % (download_dir, dir1)
  dirs2 = os.listdir(path1)
  for dir2 in dirs2:
    path2 = '%s/%s' % (path1, dir2)
    files = os.listdir(path2)
    for afile in files:
      item = json.load(open('%s/%s' % (path2, afile)))
      counts['total'] += 1
      if 'message' in item and item['message'] == 'Not Found':
        continue
      counts['found'] += 1
      for key in keys:
        if item[key] is not None: counts[key] += 1

print counts

