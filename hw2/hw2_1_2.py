import numpy as np
import matplotlib.pyplot as plt, matplotlib.lines as mlines

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

# plot the max/min and their mean
fig,ax=plt.subplots(ncols=2,nrows=2,sharex='col',sharey='row')
plt.suptitle('Max/Min $T_s$ in every 10-year July',fontsize=14)
for i in range(2):
    for j in range(2):
        daily_max=np.nanmax(data[station[i]][year[j]],axis=1)
        daily_min=np.nanmin(data[station[i]][year[j]],axis=1)
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nMean Max={np.nanmean(daily_max):.2f} ; Mean Min={np.nanmean(daily_min):.2f}',fontsize=11)
        ax[i,j].plot(np.arange(0,310),daily_max,'r')
        ax[i,j].plot(np.arange(0,310),daily_min,'b')
        ax[i,j].set_xticks(np.arange(0,311,31*2),[f'{i//31}'for i in range(0,311,31*2)])
        ax[i,j].set_yticks(np.arange(20,41,5))
        ax[i,j].set_xlim(0,310)
        ax[i,j].set_ylim(20,40)
        ax[1,j].set_xlabel('Year')
        ax[i,0].set_ylabel('Ts [degC]')
        ax[i,j].grid()
handles=[mlines.Line2D([0],[0],color='r'),mlines.Line2D([0],[0],color='b')]
fig.legend(handles=handles,labels=['Max','Min'],ncols=2,loc='lower center')
plt.tight_layout()
plt.savefig('hw2_1_2.png',dpi=450,bbox_inches='tight')
