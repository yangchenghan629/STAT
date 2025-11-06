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

# plot line of DTR
fig,ax=plt.subplots(ncols=2,nrows=2,sharex='col',sharey='row')
plt.suptitle('DTR in every 10-year July',fontsize=14)
for i in range(2):
    for j in range(2):
        daily_max=np.nanmax(data[station[i]][year[j]],axis=1)
        daily_min=np.nanmin(data[station[i]][year[j]],axis=1)
        DTR=daily_max-daily_min
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nMean={np.nanmean(DTR):.2f}',fontsize=12)
        ax[i,j].plot(DTR)
        ax[i,j].hlines(xmin=0,xmax=310,y=np.nanmean(DTR),color='r')
        ax[i,j].set_xticks(np.arange(0,311,31*2),[f'{i//31}'for i in range(0,311,31*2)])
        ax[i,j].set_yticks(np.arange(0,16,5))
        ax[i,j].set_xlim(0,310)
        ax[i,j].set_ylim(0,15)
        ax[1,j].set_xlabel('Year',fontsize=10)
        ax[i,0].set_ylabel('DTR [degC]',fontsize=10)
        ax[i,j].grid()
plt.tight_layout()
plt.savefig('hw2_1_3.png',dpi=450)

# plot histogram of DTR
fig,ax=plt.subplots(ncols=2,nrows=2,sharex='col')
plt.suptitle('Histogram of DTR anomaly',fontsize=14)
for i in range(2):
    for j in range(2):
        daily_max=np.nanmax(data[station[i]][year[j]],axis=1)
        daily_min=np.nanmin(data[station[i]][year[j]],axis=1)
        DTR=daily_max-daily_min
        DTR_mean=np.nanmean(DTR)
        DTR_var=np.nanvar(DTR)
        anomaly=DTR-DTR_mean
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nMean={DTR_mean:.2f},Var={DTR_var:.2f}',fontsize=12)
        ax[i,j].hist(anomaly,bins=50)
        ax[i,j].set_xlabel('DTR')
        ax[i,j].set_ylabel('# of days')
        ax[i,j].set_ylim(0,40)
plt.tight_layout()
plt.savefig('hw2_1_3_hist.png',dpi=450)

# daily var and DTR
plt.clf()
daily_dtr=[]
daily_var=[]
for s in station:
    for y in year:
        daily_dtr.append(np.nanmax(data[s][y],axis=1)-np.nanmin(data[s][y],axis=1))
        daily_var.append(np.nanvar(data[s][y],axis=1))       
daily_dtr=np.concatenate(daily_dtr)
daily_var=np.concatenate(daily_var)
coef=np.corrcoef(daily_dtr[~np.isnan(daily_dtr)],daily_var[~np.isnan(daily_var)])
plt.title(f'DTR and daily Variance\nR={coef[0,1]:.2f}',fontsize=14)
plt.scatter(daily_dtr,daily_var,s=[5])
plt.grid()
plt.xlabel('DTR [degC]',fontsize=12)
plt.ylabel('Variance [$(degC)^2$]')
plt.savefig('hw2_1_3_scatter.png',dpi=450)


plt.clf()
fig,ax=plt.subplots(ncols=2,nrows=2)
plt.suptitle('DTR and daily Variance',fontsize=14)
for i in range(2):
    for j in range(2):
        dtr=np.nanmax(data[station[i]][year[j]],axis=1)-np.nanmin(data[s][y],axis=1)
        var=np.nanvar(data[station[i]][year[j]],axis=1)
        coef=np.corrcoef(dtr[~np.isnan(dtr)],var[~np.isnan(var)])
        ax[i,j].set_title(f'{station[i]}_{year[j]}\nR={coef[0,1]:.2f}',fontsize=10)
        ax[i,j].scatter(daily_dtr,daily_var,s=[5])
        plt.grid()
        ax[1,j].set_xlabel('DTR [degC]')
        ax[i,0].set_ylabel('Variance [$(degC)^2$]')
plt.tight_layout()
plt.savefig('2stat2periods.png',dpi=450)