#!/usr/bin/python

import argparse
import json
import os
import sys
import time

CURL = '/usr/bin/curl'
# Keep retrying on error with backoff for about a hour.
ERROR_DELAY_SECS = [0, 1, 5, 10, 30] + [60] * 60
PRINT_INTERVAL = 100

def flush(msg):
  print msg
  sys.stdout.flush()

def is_ok(output_file, user):
  resp = json.load(open(output_file, 'r'))
  if 'message' in resp and resp['message'] == 'Not Found':
    return True
  if 'login' in resp and resp['login'].lower() == user.lower():
    return True
  return False

def download_profiles(args):
  base_name = args.user_file[args.user_file.rfind('/')+1:]
  download_dir = '%s/%s' % (args.download_base_dir, base_name)
  if not os.path.isdir(download_dir):
    os.mkdir(download_dir)

  with open(args.user_file, 'r') as fp:
    users = fp.read().splitlines()
  flush('downloading %d user profiles' % len(users))

  for i in range(len(users)):
    if i % PRINT_INTERVAL == 0:
      flush('processing user %d / %d' % (i, len(users)))

    subdir = '%05d' % (i / args.files_per_folder)
    output_dir = '%s/%s' % (download_dir, subdir)
    if not os.path.isdir(output_dir):
      os.mkdir(output_dir)

    output_file = '%s/%s.json' % (output_dir, users[i])
    if os.path.isfile(output_file) and not args.overwrite:
      continue

    cmd = ('%s "https://api.github.com/users/%s?client_id=%s&client_secret=%s"'
           ' -s -o %s' % (CURL, users[i], args.client_id, args.client_secret,
                          output_file))

    ok = False
    for delay_sec in ERROR_DELAY_SECS:
      sleep_sec = args.sleep_sec + delay_sec
      if sleep_sec > 0:
        time.sleep(sleep_sec)

      if os.system(cmd) == 0:
        if is_ok(output_file, users[i]):
          ok = True
          break
    assert ok, 'failed: %s' % cmd

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--user_file', required=True)
  parser.add_argument('--download_base_dir', required=True)
  parser.add_argument('--client_id',
                      default='ceacee89055f4df25d94')
  parser.add_argument('--client_secret',
                      default='357a69320c6aa87498875ec6faf93f366394d54a')
  parser.add_argument('--files_per_folder', type=int, default=1000)
  # Github limit is 5000/hour.
  parser.add_argument('--sleep_sec', type=float, default=0.35)
  parser.add_argument('--overwrite', type=bool, default=False)
  download_profiles(parser.parse_args())

if __name__ == '__main__':
  main()

