#!/usr/bin/python

import argparse
import os

def merge(args):
  files = os.listdir(args.bigquery_dir)
  print 'merging %d files: %s' % (len(files), files)
  actors = set()
  with open(args.output_file, 'w') as ofp:
    for afile in files:
      print 'processing %s' % afile
      with open('%s/%s' % (args.bigquery_dir, afile), 'r') as ifp:
        first = ifp.readline()
        assert first == 'actor\n' or first == 'actor_login\n'
        while True:
          line = ifp.readline()
          if line == '':
            break
          assert line.endswith('\n')
          actor = line[:-1]
          if actor not in actors:
            actors.add(actor)
            print >> ofp, actor
  print 'total: %d actors' % len(actors)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--bigquery_dir', required=True)
  parser.add_argument('--output_file', required=True)
  merge(parser.parse_args())

if __name__ == '__main__':
  main()

