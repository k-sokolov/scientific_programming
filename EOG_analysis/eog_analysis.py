import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data.csv', header=0)
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
data.set_index(['timestamp'], inplace=True)

stimuli = pd.read_csv('stimuli.csv', header=0)
stimuli['timestamp'] = pd.to_datetime(stimuli['timestamp'], unit='s')
stimuli.index = stimuli['timestamp']

def get_all_windows(data, stimuli):
    windows_ch0, windows_ch1  = [[] for i in range(len(stimuli))], [[] for i in range(len(stimuli))]
    for i,n in enumerate(stimuli.index):
        for j in data.index:
            if n == j:
                a = data.ch0[j-pd.DateOffset(seconds=0.2):j+pd.DateOffset(seconds=0.6)]
                b = data.ch1[j-pd.DateOffset(seconds=0.2):j+pd.DateOffset(seconds=0.6)]
            
                a.index = (a.index-n).total_seconds()
                b.index = (b.index-n).total_seconds()
                windows_ch0[i] = a
                windows_ch1[i] = b
    return np.asarray(windows_ch0), np.asarray(windows_ch1)
    
windows_ch0, windows_ch1 = get_all_windows(data, stimuli)

def get_peak(window):
    peak = lambda nda: abs(nda[9]- nda[0]) 
    window = window.rolling(5).median()
    peaks = window.rolling(10).apply(peak).idxmax()
    return peaks
    
pics = [4,7,9,21]
plt.figure(figsize=(20,10))
for n,i in enumerate(pics):
    plt.subplot(2,2,n+1)
    windows_ch0[i].plot(color='blue')
    windows_ch1[i].plot(color='orange')
    plt.axvline(get_peak(windows_ch0[i]),linewidth=2, color='r', label='ch0 jump')
    plt.axvline(get_peak(windows_ch1[i]),color='g', label='ch1 jump')
    plt.axvline(0, color='black',  label='stimulus',linewidth=2)
    plt.legend(loc=2, framealpha = 0.7)
    plt.xlabel('time offset [seconds]', fontsize='12')
    plt.ylabel('EOG', fontsize='12')
 
plt.show()