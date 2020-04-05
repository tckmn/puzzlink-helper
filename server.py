#!/usr/bin/env python3

PORT = 1234

import http.server
import json
import sqlite3

aliases = list(map(str.split, '''
cave bag corral correl
bosanowa bossanova
skyscrapers building skyscraper
hashi hashikake bridges
heyawake heyawacky
akari lightup
mashu pearl
roma rome
satogaeri sato
slalom suraromu
yajilin yajirin
yajilin-regions yajirin-regions
'''.strip().split('\n')))

def patch(genre):
    for alias in aliases:
        if genre in alias: return alias[0]
    return genre

def tts(t):
    h, m, s = t//3600, (t//60)%60, t%60
    return '{}:{:02}:{:02}'.format(h, m, s) if h > 0 else '{}:{:02}'.format(m, s)

conn = sqlite3.connect('p.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS d (
    genre   TEXT NOT NULL,
    variant TEXT,
    flags   TEXT,
    url     TEXT NOT NULL,
    date    TEXT NOT NULL,
    w       INTEGER NOT NULL,
    h       INTEGER NOT NULL,
    t       INTEGER NOT NULL
)
''')
conn.commit()

class PuzzlinkHelper(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        parts = data['url'].split('/')
        flags, w, h = ([None]+parts[1:3]) if parts[1].isdigit() else parts[1:4]
        c.execute('INSERT INTO d VALUES (?,NULL,?,?,datetime("now","localtime"),?,?,?)',
                (patch(parts[0]), flags, data['url'], w, h, data['t']))
        conn.commit()
        self.send_response(200)
        self.end_headers()
        self.wfile.write('saved time: {}'.format(tts(data['t'])).encode())

http.server.HTTPServer(('', PORT), PuzzlinkHelper).serve_forever()
