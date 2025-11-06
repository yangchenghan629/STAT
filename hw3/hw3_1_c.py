import numpy as np
import matplotlib.pyplot as plt

# read data
ts=np.loadtxt('./TS.txt')

# distribution
total=len(ts)
mean=np.nanmean(ts)
std=np.nanstd(ts)
pos=[mean+i*std for i in range(1,4)]
neg=[mean-i*std for i in range(1,4)]
interval=neg[::-1]+pos
interval.insert(3,mean)

# plot histogram and label the percentage
fig=plt.figure(figsize=(8,6))
plt.title(f'Distribution of $T_s$\n$\\mu={mean:.2f}$ , $\\sigma={std:.2f}$',fontsize=16)
plt.hist(ts,bins=50)
plt.vlines(x=mean,ymin=0,ymax=85,linestyles='dashed',color='r')
plt.text(x=mean-0.7,y=78,s=f'Mean\n{mean:.2f}',color='r',fontsize=12)
# lines of interval edge
for i in range(3):
    plt.vlines(x=pos[i],ymin=0,ymax=85,color='k',alpha=0.4)
    plt.vlines(x=neg[i],ymin=0,ymax=85,color='k',alpha=0.4)
    plt.text(x=pos[i]-0.6,y=78,s=f'+{i+1}$\\sigma$\n{pos[i]:5.2f}',color='k',fontsize=12)
    plt.text(x=neg[i]-0.6,y=78,s=f'-{i+1}$\\sigma$\n{neg[i]:5.2f}',color='k',fontsize=12)
# percentage
for i in range(6):
    percentage=len(ts[(ts>interval[i]) & (ts<interval[i+1])])/total*100
    plt.text(x=(interval[i]+interval[i+1])/2-1,y=70,s=f'{percentage:05.2f}%',fontsize=12)
plt.xticks(np.arange(-4,31,4),fontsize=12)
plt.yticks(np.arange(0,86,10),fontsize=12)
plt.xlim(mean-3.2*std,mean+3.2*std)
plt.ylim(0,85)
plt.xlabel('$T_s$ [degC]',fontsize=12)
plt.ylabel('# of months',fontsize=12)
plt.tight_layout()
plt.savefig('hw3_1_c.png',dpi=450)


plt.clf()
# anomaly distribution
outfile_c=open('outfile_c.txt','w')
season=np.tile(np.nanmean(ts.reshape(-1,12),axis=0),len(ts)//12)
anomaly=ts-season
mean_ano=np.nanmean(anomaly)
std_ano=np.nanstd(anomaly)
pos_ano=[mean_ano+i*std_ano for i in range(1,4)]
neg_ano=[mean_ano-i*std_ano for i in range(1,4)]
interval_ano=neg_ano[::-1]+pos_ano
interval_ano.insert(3,mean_ano)

# plot histogram
fig=plt.figure(figsize=(8,6))
plt.title(f'Distribution of $T_s$ Anomaly\n$\\mu$={mean_ano:.2f} , $\\sigma$={std_ano:.2f}',fontsize=16)
plt.hist(anomaly,bins=50)
plt.vlines(x=mean_ano,ymin=0,ymax=120,linestyles='dashed',color='r')
plt.text(x=mean_ano-0.1,y=110,s=f'Mean\n{mean_ano:.2f}',color='r',fontsize=12)
# lines of interval edge
for i in range(3):
    plt.vlines(x=pos_ano[i],ymin=0,ymax=120,color='k',alpha=0.4)
    plt.vlines(x=neg_ano[i],ymin=0,ymax=120,color='k',alpha=0.4)
    plt.text(x=pos_ano[i]-0.1,y=110,s=f'+{i+1}$\\sigma$\n{pos_ano[i]:5.2f}',color='k',fontsize=12)
    plt.text(x=neg_ano[i]-0.1,y=110,s=f'-{i+1}$\\sigma$\n{neg_ano[i]:5.2f}',color='k',fontsize=12)
# percentage
for i in range(6):
    percentage=len(anomaly[(anomaly>interval_ano[i]) & (anomaly<interval_ano[i+1])])/total*100
    plt.text(x=(interval_ano[i]+interval_ano[i+1])/2-0.1,y=100,s=f'{percentage:05.2f}%',fontsize=12)
plt.xticks(np.arange(-2.5,2.6,0.5),fontsize=12)
plt.yticks(np.arange(0,121,10),fontsize=12)
plt.xlim(mean_ano-3.5*std_ano,mean_ano+3.5*std_ano)
plt.ylim(0,120)
plt.xlabel('anomaly [degC]',fontsize=12)
plt.ylabel('# of months',fontsize=12)
plt.tight_layout()
plt.savefig('hw3_1_c_anomaly.png',dpi=450)

# write out percentage of +-1~3std
for i in range(3):
    percentage=len(anomaly[(anomaly>neg_ano[i])&(anomaly<pos_ano[i])])/total*100
    outfile_c.write(f'mean +- {i+1} STD : {percentage:.2f} %\n')