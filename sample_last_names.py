#!/usr/bin/python

import argparse
import json
import os
import random

# Logic:
# 1) if word count < 2 => not cn
# 2) if word count = 2 => check against list
# 3) if word count > 2 => check last and second last + last against list
def classify(name, names):
  parts = name.split()
  if len(parts) <= 1:
    return False
  last = parts[-1].lower()
  if last in names:
    return True
  if len(parts) == 2:
    return False
  second = parts[-2].lower()
  if '%s %s' % (second, last) in names:
    return True
  return False

def sample(args):
  with open(args.name_file, 'r') as fp:
    names = set(fp.read().splitlines())
  with open(args.positive_file, 'w') as pfp:
    with open(args.negative_file, 'w') as nfp:
      for dirpath, dirnames, filenames in os.walk(args.input_dir):
        for filename in filenames:
          if random.random() > args.rate:
            continue
          item = json.load(open(os.path.join(dirpath, filename)))
          if 'name' not in item or item['name'] is None:
            continue
          name = item['name']
          is_cn = classify(name, names)
          if is_cn:
            print >> pfp, name.encode('utf-8')
          else:
            print >> nfp, name.encode('utf-8')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', required=True)
  parser.add_argument('--name_file', required=True)
  parser.add_argument('--rate', type=float, default=1)
  parser.add_argument('--positive_file', required=True)
  parser.add_argument('--negative_file', required=True)
  sample(parser.parse_args())

if __name__ == '__main__':
  main()

