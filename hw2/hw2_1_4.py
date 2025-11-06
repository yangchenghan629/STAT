import numpy as np
import matplotlib.pyplot as plt, matplotlib.cm as cm

station=['Taipei','Taitung']
year=['1961_1970','2001_2010']

data={} # dictionary for July Ts

# read data from file
for s in station:
    data[s]={}
    for y in year:
        file=f'data/HW2_{s}_Ts_{y}.txt'
        raw_data=np.loadtxt(file).reshape(24,31*12*10)
        july=np.zeros((310,24))
        for i in range(10):
            july[31*i:31*(i+1),:]=raw_data[:,31*(12*i+6):31*(12*i+7)].T
        data[s][y]=july

# plot the difference between 2 station in same periods
diurnal={}
for s in station:
    diurnal[s]={}
    for y in year:
        diurnal[s][y]=np.nanmean(data[s][y],axis=0)
diff_1960=diurnal['Taipei']['1961_1970']-diurnal['Taitung']['1961_1970']
diff_2000=diurnal['Taipei']['2001_2010']-diurnal['Taitung']['2001_2010']
plt.title('Difference between Taipei and Taitung in same periods\nTaipei-Taitung',fontsize=12)
plt.plot(diff_1960,'b',label='1961~1970')
plt.plot(diff_2000,'r',label='2001~2010')
plt.xticks(np.arange(0,24,2))
plt.xlim(0,23)
plt.ylim(-1.5,2.5)
plt.legend()
plt.grid()
plt.savefig('hw2_1_4.png')