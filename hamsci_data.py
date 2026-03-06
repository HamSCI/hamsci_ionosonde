import numpy as np
import os
import datetime as dt
import scipy.signal as signal
import pandas as pd

def read_file(file_name, dtype=np.float32):
    data = np.fromfile(file_name, dtype=dtype)
    data = data.reshape(-1, 2)
    return  data[:, 0] + 1j * data[:, 1]


def cross_correlation(signal1, signal2):
    x = np.asarray(signal2)
    y = np.asarray(signal1)

    correlation = signal.correlate(x, y, mode='full')
    lag = np.arange(len(correlation)) - (len(correlation) // 2)  # Adjust for full output
    magnitudes = 20*np.log10(correlation)

    return lag,magnitudes


def calculate_delay(x,y,sample_rate): # determines delay by finding the difference between peaks in the correlation 
    y = np.real(y)
    if len(y)==0:
        return np.nan,np.nan
    peaks = signal.find_peaks(y, distance=300)[0] # finds peaks in correlation

    local_peaks = pd.DataFrame({'x':x[peaks], 'y':y[peaks]}) # data frame ensures time values and magnitude values stay in sync
    local_peaks = local_peaks.sort_values(by='y',ascending=False)

    # identify the first peak. (the direct path)
    directx = local_peaks['x'].values[0]
    directy = local_peaks['y'].values[0]

    # identify the second peak. (the indirect path)
    secondx = local_peaks['x'].values[1]
    secondy = local_peaks['y'].values[1]
    
    delay = (secondx-directx)/sample_rate # gives the delay in seconds

    # determine how closely the return echo correlation peak matches the direct path
    peak1 = np.argwhere(x==directx)[0][0]
    peak2 = np.argwhere(x==secondx)[0][0]
    w1 = -175 # window to compare curves of first and second peaks
    w2 =  175
    curve1 = y[peak1+w1:peak1+w2]-(directy-secondy)
    curve2 = y[peak2+w1:peak2+w2]
    sum_squares_diff = 0
    if len(curve1) == len(curve2):
        diff = curve1-curve2
        for j in diff:
            sum_squares_diff=sum_squares_diff+(j**2)
        root_sum_squares_diff = np.sqrt(sum_squares_diff)
    else:
        root_sum_squares_diff = np.nan
    return delay,root_sum_squares_diff
    

def calculate_virtual_layer_heights(raw_data_directory,start_date,end_date): 
    '''
    :param directory: Parent directory of raw data files
    :param start_date: first date to process. enter date as datetime obj
    :param end_date: last date to process. enter date as datetime obj
    '''

    delta = end_date-start_date
    date_directories = []
    for i in range(delta.days+1):
        day = raw_data_directory+dt.datetime.strftime(start_date+dt.timedelta(days=i),'%Y/%m/%d/')
        if os.path.isdir(day):
            date_directories.append(day)

    fnames = []
    fpaths = []
    for directory in date_directories: # create a list of all files with date range and their file paths
        for file_name in os.listdir(directory):
            file_path = directory+file_name
            date = dt.datetime.strptime(file_name[0:19],'%Y_%m_%d_%H_%M_%S').replace(tzinfo=dt.timezone.utc)#
            if file_name!='no_name' and os.path.getsize(file_path)!=0 and date>start_date: # avoid processing files that are empty or are the transmitted chirp
                fnames.append(file_name)
                fpaths.append(file_path)
    
    blank = np.ndarray(len(fnames)).fill(np.nan) # 
    correlation_data = pd.DataFrame({'names':fnames, # create a dataframe to remain organized while processing
                                    'paths':fpaths,
                                    'utc_times':blank,
                                    'lags':blank,
                                    'mags':blank,
                                    'delays':blank,
                                    'heights':blank,
                                    'root_sum_squares_diff':blank,
                                    'frequencies':blank,
                                    'echo_detected':blank})

    correlation_data['utc_times'] = pd.to_datetime(correlation_data['names'].str[0:19],format='%Y_%m_%d_%H_%M_%S') # psarse utc timestamp from file name
    correlation_data['frequencies'] = correlation_data['names'].str[20:]  # parse frequencies from file name

    sample_chirp = read_file('chirps_and_echoes/chirpA')
    for i in correlation_data.index: # perform the cross correlation on each file
        file_path = correlation_data['paths'][i]
        chirp_echo = read_file(file_path)
        if len(chirp_echo)!=0:
            lag,mag = cross_correlation(sample_chirp, chirp_echo)
            correlation_data.at[i,'lags'] = lag#[0:len(lag)//2]
            correlation_data.at[i,'mags'] = mag#[0:len(lag)//2]
        else:
            correlation_data.at[i,'lags'] = []
            correlation_data.at[i,'mags'] = []

    sample_rate = 195312
    max_root_sum_squares_diff = 500
    min_delay = 0.001 # 150*2/300000
    max_delay = 0.003 # 450*2/300000
    
    for i in correlation_data.index: # calculatae delay for each echo
        delay,root_sum_squares_diff = calculate_delay(correlation_data['lags'][i],correlation_data['mags'][i],sample_rate)
        if root_sum_squares_diff > max_root_sum_squares_diff or root_sum_squares_diff==np.nan: # if return sginal is lost in noise, disregard data point
            correlation_data.loc[i,'delays'] = np.nan
            correlation_data.loc[i,'echo_detected'] = False
        elif delay > max_delay or delay < min_delay: # if "delay" is outside of reasonable range, it is likely noise or mult-ihop
            correlation_data.loc[i,'delays'] = np.nan
            correlation_data.loc[i,'echo_detected'] = False
        else:
            correlation_data.loc[i,'delays'] = delay
            correlation_data.loc[i,'echo_detected'] = True

        correlation_data.loc[i,'root_sum_squares_diff'] = root_sum_squares_diff

    correlation_data['heights'] = (correlation_data['delays'])*(299792.458/2) # convert delay to virtual layer height

    data_output = pd.DataFrame({'utc_times':          correlation_data['utc_times'],
                                'frequencies_Hz':    correlation_data['frequencies'],
                                'virtual_heights_km': correlation_data['heights'],
                                'echo_detected':      correlation_data['echo_detected']})
    return data_output

def update_layer_height_csv(csv_directory,raw_data_directory):
    if len(os.listdir(csv_directory))!=0:
        old_data = pd.read_csv(csv_directory+os.listdir(csv_directory)[-1])
        old_data['utc_times'] = pd.to_datetime(old_data['utc_times'],format='ISO8601',utc=True)
        start_date = (old_data['utc_times'].iloc[-1]).to_pydatetime()
    else:
        start_date = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=int(3)))#.strftime('%Y-%m-%dT%H:%M:%S')
    end_date = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=int(1)))#.strftime('%Y-%m-%dT%H:%M:%S')


    data = calculate_virtual_layer_heights(raw_data_directory,start_date,end_date)
    save_height_data(data,csv_directory)


def save_height_data(data,data_directory):
    start_date = data['utc_times'].iloc[0].date()
    end_date   = data['utc_times'].iloc[-1].date()

    day = start_date
    while day<=end_date:
        new_data = data[data['utc_times'].dt.date==day]
        file_path = data_directory+str(day)+'.csv'
        if os.path.isfile(file_path):
            old_data = pd.read_csv(file_path)
            old_data['utc_times'] = pd.to_datetime(old_data['utc_times'],format='ISO8601')

            new_data = pd.concat([old_data,new_data])
        new_data = new_data.sort_values(by=['utc_times'],ascending=True)
        new_data = new_data.reset_index(drop=True)
        new_data = new_data.drop_duplicates()

        new_data.to_csv(file_path,index=False)
        day=day+dt.timedelta(days=1)

if __name__ == '__main__':
    start_date = dt.datetime(2026,2,6)
    end_date = dt.datetime(2026,2,9)
    # print(calculate_virtual_layer_heights('chirps_and_echoes/',start_date,end_date))
    # print(os.path.getsize('chirps_and_echoes/2026/02/09/2026_02_09_00_00_54_7025002'))
    csv_directory = 'Scranton_data/'
    raw_data_directory = 'chirps_and_echoes/'
    update_layer_height_csv(csv_directory,raw_data_directory)