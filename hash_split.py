#!/usr/bin/python

import argparse
import hashlib

def prepare_output(output_dir, k, base_name):
  return [open('%s/%s-%d' % (output_dir, base_name, i), 'w')
          for i in range(k)]

def hash_split(args):
  fps = prepare_output(args.output_dir, args.k,
                       args.input_file[args.input_file.rfind('/')+1:])
  with open(args.input_file, 'r') as fp:
    while True:
      line = fp.readline()
      if line == '':
        break
      assert line.endswith('\n')
      line = line[:-1]
      h = int(hashlib.sha1(line).hexdigest(), 16) % args.k
      print >> fps[h], line
  for fp in fps:
    fp.close()

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_file', required=True)
  parser.add_argument('--output_dir', required=True)
  parser.add_argument('--k', type=int, required=True)
  hash_split(parser.parse_args())

if __name__ == '__main__':
  main()

