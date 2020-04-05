#!/usr/bin/env python3

import sqlite3
import itertools
from datetime import datetime

import plotly.graph_objects as go
import plotly.subplots as sp

fst = lambda x: x[0]
snd = lambda x: x[1]
cutoff = 20
xticks = 30
yticks = 10

conn = sqlite3.connect('p.db')
c = conn.cursor()

solves = c.execute('select count(*), date(date) from d group by date(date) order by date').fetchall()

# fig = go.Figure(data=go.Scatter(x=list(map(snd, solves)), y=list(itertools.accumulate(map(fst, solves)))))
# fig.show()

fig = sp.make_subplots(
        rows=2, cols=2,
        subplot_titles=('solves over time', 'solves by genre', 'time spent over time', 'time spent by genre'),
        horizontal_spacing=0.05, vertical_spacing=0.12)

solves = c.execute('select date, row_number() over (order by date) from d order by date').fetchall()
fig.add_trace(go.Scatter(x=list(map(fst, solves)), y=list(map(snd, solves)), showlegend=False), row=1, col=1)
fig.update_xaxes(title_text='date', nticks=xticks, row=1, col=1)
fig.update_yaxes(title_text='solves', nticks=yticks, row=1, col=1)

genres = c.execute('select distinct genre, (select count(*) from d where genre = d1.genre) as ct from d d1 order by ct desc').fetchall()
genres = genres[:cutoff] + [('[others]', sum(map(snd, genres[cutoff:])))]
fig.add_trace(go.Bar(x=list(map(fst, genres)), y=list(map(snd, genres)), showlegend=False), row=1, col=2)
fig.update_xaxes(title_text='genre', row=1, col=2)
fig.update_yaxes(title_text='solves', nticks=yticks, row=1, col=2)

tsolves = c.execute('select date, t/3600.0 from d order by date').fetchall()
fig.add_trace(go.Scatter(x=list(map(fst, tsolves)), y=list(itertools.accumulate(map(snd, tsolves))), showlegend=False), row=2, col=1)
fig.update_xaxes(title_text='date', nticks=xticks, row=2, col=1)
fig.update_yaxes(title_text='time spent (hrs)', nticks=yticks, row=2, col=1)

tgenres = c.execute('select distinct genre, (select sum(t)/3600.0 from d where genre = d1.genre) as ct from d d1 order by ct desc').fetchall()
tgenres = tgenres[:cutoff] + [('[others]', sum(map(snd, tgenres[cutoff:])))]
fig.add_trace(go.Bar(x=list(map(fst, tgenres)), y=list(map(snd, tgenres)), showlegend=False), row=2, col=2)
fig.update_xaxes(title_text='genre', row=2, col=2)
fig.update_yaxes(title_text='time spent (hrs)', nticks=yticks, row=2, col=2)

fig.show()
