#!/usr/bin/env python

"""Normalize queries and count."""

import collections
import re

QUERY_RE = re.compile('^(\d+) (\d+) \((\d+)\): COM_QUERY: (SELECT.*)')
STRING_RE = re.compile("'[\w\-\.]+'")
DATE_RE = re.compile("'\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d\.\d+'")
INT_RE = re.compile("= \d+")
# Must be last
IN_RE = re.compile("IN \(.*'<argument>'\)")
INST_Q_RE = re.compile("SELECT anon_1.instances_created_at AS anon_1_instances_created_at.*FROM..SELECT..*FROM instances")

def parse_file(queries, fname):
    with open(fname, 'r') as f:
        for line in f:
            m = QUERY_RE.match(line)
            if not m:
                continue
            resp_sz, rows, query_sz, query = m.groups()
            query = STRING_RE.sub("'<argument>'", query)
            query = DATE_RE.sub("'<date>'", query)
            query = INT_RE.sub("= <number>", query)
            query = IN_RE.sub("IN (<LIST>)", query)
            query = INST_Q_RE.sub("SELECT <instance_shit> FROM (SELECT <more_instance_shit> FROM instances", query)
            queries[query]['queries'] += 1
            queries[query]['resp_sz'] += int(resp_sz)
            queries[query]['rows'] += int(rows)


queries = collections.defaultdict(lambda: collections.defaultdict(int))

parse_file(queries, 'queries.txt')

for query in queries.keys():
    qryinfo = queries[query]
    print qryinfo['queries'], qryinfo['resp_sz'], qryinfo['rows'], query
