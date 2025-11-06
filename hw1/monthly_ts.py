import numpy as np
import matplotlib.pyplot as plt

ts=np.loadtxt('TS.txt').reshape(-1,12)

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
colors=plt.cm.Spectral(np.linspace(0,1,12))

# plot monthly Ts in 12 plots
plt.clf()
fig,ax=plt.subplots(ncols=4,nrows=3,figsize=(9,6),sharex='all',sharey='all')
plt.suptitle('Histogram of Monthly $T_s$',fontsize=16)
for i in range(12):
    ax[i//4,i%4].hist(ts[:,i],bins=50,color='darkblue')
    ax[i//4,i%4].set_title(months[i],fontsize=12)
    ax[i//4,i%4].set_xticks(np.arange(0,21,5))
    ax[i//4,i%4].set_xlim(0,20)
    ax[i//4,i%4].set_ylim(0,15)
plt.savefig('hw1_a_2_2.png',dpi=300)

# plot monthly Ts in one plot
plt.clf()
plt.figure(figsize=(9,6))
plt.title('Histogram of Monthly $T_s$',fontsize=16)
for i in range(12):
    plt.hist(ts[:,i],bins=20,color=colors[i],label=months[i],alpha=0.8)
plt.legend(ncols=2)
plt.xlabel('$T_s$ [degC]',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.savefig('hw1_a_2_3.png',dpi=300)