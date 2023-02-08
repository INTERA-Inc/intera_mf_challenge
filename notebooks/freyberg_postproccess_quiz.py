import os

import flopy.modflow
import matplotlib.pyplot as plt
import pandas as pd

def main():
    model_ws = os.path.join('..', 'data', 'Freyberg_transient')

    # mf = flopy.modflow.Modflow('freyberg.nam',model_ws=model_ws,version='mfnwt',verbose=True)
    mf = flopy.modflow.Modflow.load('freyberg.nam',model_ws=model_ws,version='mfnwt',check=False)

    df = pd.DataFrame({'wellid': ['MW1', 'MW2', 'MW5', 'PW6'],
                       'layer': [1, 1, 1, 1],
                       'row': [9, 24, 18, 34],
                       'column': [9, 7, 16, 12],
                       'top_screen':[10,13.5,9.825,-15],
                       'bot_screen':[7.5,10,6.425,-20]})

    hdsobj = flopy.utils.HeadFile(os.path.join(model_ws,'freyberg.hds'))
    start_datetime = pd.to_datetime(mf.modeltime.start_datetime)
    for i, dfrow in df.iterrows():
        l, r, c = dfrow['layer'], dfrow['row'], dfrow['column']
        
        fig, ax = plt.subplots(figsize=(8,6))
        
        ts = hdsobj.get_ts(idx=(l-1,r-1,c-1))
        times = ts[:,0]
        dates = [start_datetime+pd.to_timedelta(day,unit='d') for day in times]
        hds = ts[:,1]

        ax.plot(dates, hds)

        ax.set_title(dfrow['wellid'])
        ax.set_xlim([pd.to_datetime('01/01/2016'),pd.to_datetime('01/01/2018')])
        fig.tight_layout()
        
    plt.show()
    print('heh')


if __name__ == '__main__':
    main()