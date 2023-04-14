import fastf1
from fastf1.livetiming.data import LiveTimingData
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly import subplots
from datetime import timedelta

fastf1.Cache.enable_cache('C:/Users/tiago/Desktop/Projetos/Python/data-visualization/Formula 1/Cache')

YEAR = 2022
RACE = 'Bahrain'
# ROUND = 1
SESSION = 'R'

event = fastf1.get_event(YEAR, RACE)

print(event.EventName)

session = event.get_session(SESSION)

session.load()

laps = session.laps

alo_laps = laps.pick_driver('ALO')
print(alo_laps)

alo_fast = alo_laps.pick_fastest()
print(alo_fast)

alo_car = alo_fast.get_car_data()
print(alo_car)





# race = []
# for driver, lap_time, lap_number in zip(session.laps.Driver, session.laps.LapTime, session.laps.LapNumber):
#     race.append({'driver':driver,
#                 'lap-time':lap_time,
#                 'lap-number':lap_number})
    

# df = pd.DataFrame(race)

# print(df.head())



# data = [go.Scatter(x=df[df['driver']=='VER']['lap-number'],
#                    y=pd.to_timedelta(df[df['driver']=='VER']['lap-time']),
#                 #    text = [str(timedelta(seconds=df[df['driver']=='VER']['lap-time']))]
#                    )]



# layout = go.Layout(title = 'F1 time per lap',
#                    yaxis=dict(
#                        tickmode='array',
#                        tickvals=[60000000000,88000000000,90000000000,92000000000,105000000000],
#                        ticktext=['1:00:00', '1:28:00','1:30:00', '1:32:00','1:45:00']
#                    ))

# # fig.update_layout(layout)

# fig = go.Figure(data, layout)
# pyo.plot(fig)