#!/usr/bin/python

import argparse
import json
import os
import random

def sample(args):
  with open(args.output_file, 'w') as fp:
    for dirpath, dirnames, filenames in os.walk(args.input_dir):
      for filename in filenames:
        if random.random() > args.rate:
          continue
        item = json.load(open(os.path.join(dirpath, filename)))
        if args.field not in item or item[args.field] is None:
          print >> fp, 'null'
        else:
          print >> fp, item[args.field].encode('utf-8')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', required=True)
  parser.add_argument('--field', required=True)
  parser.add_argument('--rate', type=float, default=1)
  parser.add_argument('--output_file', required=True)
  sample(parser.parse_args())

if __name__ == '__main__':
  main()

