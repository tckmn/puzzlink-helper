#!/usr/bin/env python3

import sqlite3
import os
here = os.path.dirname(os.path.realpath(__file__))

def tts(t):
    h, m, s = t//3600, (t//60)%60, t%60
    return '{}:{:02}:{:02}'.format(h, m, s) if h > 0 else '{}:{:02}'.format(m, s)

conn = sqlite3.connect(here+'/p.db')
c = conn.cursor()

fmt = '{: <15} {: >4} {: >9}'

print('\n'.join(
    fmt.format(genre, ct, tts(tm))
    for (genre, ct, tm) in
    c.execute('select genre, count(*) as ct, sum(t) as tm from d group by genre order by ct, tm').fetchall()))

ttl = c.execute('select count(*), sum(t) from d').fetchone()
print(fmt.format('', ttl[0], tts(ttl[1])))
