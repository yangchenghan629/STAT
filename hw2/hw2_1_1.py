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
        data[s][y]=july.flatten()


# plot line of Ts in every 10 year
fig,ax=plt.subplots(ncols=2,nrows=2,sharex='col',sharey='row',layout='constrained')
plt.suptitle('Hourly $T_s$ in 10-year July',fontsize=14)
for i in range(2):
    for j in range(2):
        daily_mean=np.nanmean(data[station[i]][year[j]])
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nMean={daily_mean:.2f}',fontsize=10)
        ax[i,j].plot(np.arange(0,7440),data[station[i]][year[j]])
        ax[i,j].hlines(xmin=0,xmax=7440,y=daily_mean,color='r')
        ax[i,j].set_xticks(np.arange(0,7441,744*2),[f'{i//744}'for i in np.arange(0,7441,744*2)])
        ax[i,j].set_xlim(0,7440)
        ax[i,0].set_ylabel('Ts [degC]')
        ax[1,j].set_xlabel('Year')
        ax[i,j].grid()
plt.savefig('hw2_1_1_line.png',dpi=450)

# plot histogram of Ts in every 10 year
fig,ax=plt.subplots(ncols=2,nrows=2,sharex='col',sharey='row',layout='constrained')
plt.suptitle('Distribution of 10-year Hourly $T_s$ in July',fontsize=14)
for i in range(2):
    for j in range(2):
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nMean={np.nanmean(data[station[i]][year[j]]):.2f},STD={np.nanstd(data[station[i]][year[j]]):.2f}',fontsize=10)
        ax[i,j].hist(data[station[i]][year[j]],bins=50)
        ax[1,j].set_xlabel('Ts [degC]')
        ax[i,0].set_ylabel('# of Hours')
plt.savefig('hw2_1_1_hist.png',dpi=450)


