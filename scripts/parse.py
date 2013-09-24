#!/usr/bin/env python

"""Normalize queries and count."""

import collections
import re
import sys

QUERY_RE = re.compile('^(\d+) (\d+) \((\d+)\): COM_QUERY: (SELECT.*)')
SELECT_CRAP_RE = re.compile("SELECT .*? FROM")
STRING_RE = re.compile("'[\w\-\.]+'")
DATE_RE = re.compile("'\d\d\d\d\-\d\d\-\d\d \d\d:\d\d:\d\d(\.\d+)*'")
INT_RE = re.compile("= \d+")
MAC_RE = re.compile("mac = '(\w\w:){5}\w\w'")
# Must be last
IN_RE = re.compile("IN \(.*'<argument>'\)")
MULTI_JOIN_RE = re.compile("LEFT OUTER JOIN (\S+)")
JOIN_RE = re.compile("LEFT OUTER JOIN.*(LIMIT|WHERE|\)|$)")

def parse_joins(q_str):
    m = MULTI_JOIN_RE.findall(q_str)
    if not m:
        return q_str
    join_str = "JOIN %s" % str(sorted(m))
    return JOIN_RE.sub(join_str, q_str)

def parse_file(queries, fname):
    with open(fname, 'r') as f:
        for line in f:
            m = QUERY_RE.match(line)
            if not m:
                continue
            resp_sz, rows, query_sz, query = m.groups()

            # Convert "SELECT <crap> FROM"
            query = SELECT_CRAP_RE.sub("SELECT <crap> FROM", query)
            query = STRING_RE.sub("'<argument>'", query)
            query = DATE_RE.sub("'<date>'", query)
            query = INT_RE.sub("= <number>", query)
            query = MAC_RE.sub("= <macaddr>", query)
            query = IN_RE.sub("IN (<LIST>)", query)
            query = parse_joins(query)
            queries[query]['queries'] += 1
            queries[query]['resp_sz'] += int(resp_sz)
            queries[query]['rows'] += int(rows)


queries = collections.defaultdict(lambda: collections.defaultdict(int))

parse_file(queries, sys.argv[1])

for query in queries.keys():
    qryinfo = queries[query]
    print qryinfo['queries'], qryinfo['resp_sz'], qryinfo['rows'], query
