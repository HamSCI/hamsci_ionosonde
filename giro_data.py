import pandas as pd
import os
import datetime as dt
import numpy as np

defaultFromDate = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=int(7))).strftime('%Y-%m-%dT%H:%M:%S')
defaulttoDate = (dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=int(1))).strftime('%Y-%m-%dT%H:%M:%S')

def get_giro_data(fromDate=defaultFromDate,toDate=defaulttoDate,stationList=['AL945','MHJ45']):
    urlfrom = '&fromDate=' + fromDate
    urlto = '&toDate=' + toDate
    urldates = urlfrom + urlto

    urlpt1 = "https://lgdc.uml.edu/common/DIDBGetValues?ursiCode="
    urlpt2 = "&charName=foF2,hmF2,foE,MUFD,hF2&DMUF=3000"#"&charName=MUFD,hmF2,TEC,foF2,foE,foEs&DMUF=3000"

    df_list = []
    for station in stationList:
        df=pd.read_csv(urlpt1 + station + urlpt2 + urldates,
                comment='#',
                delim_whitespace=True,
                parse_dates=[0],
                names = ['time', 'cs', 'fof2', 'qd1', 'MUFD', 'qd2', 'foE', 'qd3', 'hmF2', 'qd4', 'hF2', 'qd5'])\
                .assign(station_id=station)
        df_list.append(df)

    giro_data=pd.concat(df_list)

    giro_data = giro_data[['station_id', 'time', 'cs', 'fof2', 'MUFD', 'foE', 'hmF2', 'hF2']]

    giro_data.cs = giro_data.cs.astype(str)
    giro_data = giro_data[giro_data.cs.str.contains("No") == False]
    giro_data['time'] = pd.to_datetime(giro_data['time'],format='ISO8601')

    #set --- to nan
    giro_data = giro_data.applymap(lambda x: np.nan if type(x) is str and x == '---' else x)

    giro_data.sort_values(by=['time'], inplace=True)

    return giro_data

def save_giro_data(giro_data,giro_data_directory):
    startdate = giro_data['time'].iloc[0].date()
    enddate   = giro_data['time'].iloc[-1].date()

    day = startdate
    while day<=enddate:
        new_data = giro_data[giro_data['time'].dt.date==day]
        file_path = giro_data_directory+str(day)+'.csv'
        if os.path.isfile(file_path):
            old_data = pd.read_csv(file_path)
            old_data['time'] = pd.to_datetime(old_data['time'],format='ISO8601')

            new_data = pd.concat([old_data,new_data])
        new_data = new_data.sort_values(by=['time'],ascending=True)
        new_data = new_data.reset_index(drop=True)
        new_data = new_data.drop_duplicates()

        new_data.to_csv(file_path,index=False)
        day=day+dt.timedelta(days=1)


def update_giro_data_csv(giro_data_directory,stationList=['AL945','MHJ45']):
    if len(os.listdir(giro_data_directory))!=0:
        old_data = pd.read_csv(giro_data_directory+os.listdir(giro_data_directory)[-1])
        old_data['time'] = pd.to_datetime(old_data['time'],format='ISO8601')
        fromDate = (old_data['time'].iloc[-1]).strftime('%Y-%m-%dT%H:%M:%S')
    else:
        fromDate = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=int(7))).strftime('%Y-%m-%dT%H:%M:%S')
    toDate = (dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=int(1))).strftime('%Y-%m-%dT%H:%M:%S')

    giro_data = get_giro_data(fromDate,toDate,stationList)
    save_giro_data(giro_data,giro_data_directory)

if __name__ == '__main__':
    update_giro_data_csv(giro_data_directory='GIRO_data/',stationList=['AL945','MHJ45'])