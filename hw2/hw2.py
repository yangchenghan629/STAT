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


outfile=open('./HW2_results.txt','w')
# 2.1.1
# calculate mean and write out the results
outfile.write('2.1.1\n')
for s in station:
    for y in year:
        avg=np.nanmean(data[s][y].flatten())
        outfile.write(f'{s:<10}{y:<12}Mean : {avg:5.2f}\n')

# 2.1.2
# find daily max/min and calculate mean max/min
outfile.write('\n2.1.2\n')
for s in station:
    for y in year:
        daily_max=np.nanmax(data[s][y],axis=1)
        daily_min=np.nanmin(data[s][y],axis=1)
        mean_max=np.nanmean(daily_max)
        mean_min=np.nanmean(daily_min)
        outfile.write(f'{s:<10}{y:<12}Mean Max : {mean_max:5.2f}\n')
        outfile.write(f'{s:<10}{y:<12}Mean Min : {mean_min:5.2f}\n')

# 2.1.3
# find daily max/min and calculate mean DTR
outfile.write('\n2.1.3\n')
for s in station:
    for y in year:
        daily_max=np.nanmax(data[s][y],axis=1)
        daily_min=np.nanmin(data[s][y],axis=1)
        DTR=daily_max-daily_min
        mean_DTR=np.nanmean(DTR)
        outfile.write(f'{s:<10}{y:<12}Mean DTR : {mean_DTR:5.2f}\n')

# calculate variance of hourly Ts
for s in station:
    for y in year:
        var=np.nanvar(data[s][y])
        outfile.write(f'{s:<10}{y:<12}Variance : {var:5.2f}\n')
outfile.close()

# 2.1.4
# plot the average diurnal cycle
plt.figure(figsize=(8,6))
plt.title('Average Diurnal Cycle',fontsize=16)
for s in station:
    for y in year:
        diurnal=np.nanmean(data[s][y],axis=0)
        plt.plot(diurnal,label=f'{s}_{y}')
plt.grid()
plt.legend()
plt.xticks(np.arange(0,24,3))
plt.xlim(0,23)
plt.xlabel('Hour',fontsize=14)
plt.ylabel('Ts [degC]',fontsize=14)
plt.savefig('hw2_diurnal_cycle.png',dpi=450)


# hh,dd=np.meshgrid((np.arange(data['Taitung']['1961_1970'].shape[0])),np.arange(data['Taitung']['1961_1970'].shape[1]))
# fig,ax=plt.subplots(nrows=2,ncols=2,layout='constrained')
# for i in range(2):
#     for j in range(2):
#         ax[i,j].set_title(f'{station[i]}_{year[j]}',fontsize=10)
#         c=ax[i,j].pcolormesh(hh,dd,data[station[i]][year[j]].T,cmap=cm.coolwarm)
#         ax[i,j].set_yticks(np.arange(0,311,31))
#         bar=plt.colorbar(c,ax=ax[i,j],ticks=[10,15,20,25,30,35])
# plt.savefig('test.png')