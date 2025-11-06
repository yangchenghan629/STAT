import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

ts=np.loadtxt('TS.txt')
ts_seasonal=np.tile(np.nanmean(ts.reshape(-1,12),axis=0),ts.shape[0]//12)
ts_anomaly=ts-ts_seasonal

# plot histogram of Ts with small interval
plt.figure(figsize=(9,6))
plt.title('Histogram of $T_s$',fontsize=16)
plt.hist(ts,bins=10,color='darkblue',edgecolor='k',linewidth=1)
plt.xlabel('$T_s$ [degC]',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.xticks(np.arange(0,21,5),fontsize=12)
plt.yticks(np.arange(0,251,50),fontsize=12)
plt.savefig('hw1_a_1.png',dpi=300)

# plot histogram of Ts with large interval
plt.clf()
plt.figure(figsize=(9,6))
plt.title('Histogram of $T_s$',fontsize=16)
plt.hist(ts,bins=50,color='darkblue',edgecolor='k',linewidth=1)
plt.xlabel('$T_s$ [degC]',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.xticks(np.arange(0,21,5),fontsize=12)
plt.yticks(np.arange(0,81,10),fontsize=12)
plt.savefig('hw1_a_2.png',dpi=300)

# plot histogram of Ts anomaly
plt.clf()
plt.figure(figsize=(9,6))
plt.title('Histogram of $T_s$ Anomaly',fontsize=16)
plt.hist(ts_anomaly,bins=50,color='darkblue',edgecolor='k',linewidth=1)
plt.xlabel('$T_s$ anomaly [degC]',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.xticks(np.arange(-1.5,1.6,0.5),fontsize=12)
plt.yticks(np.arange(0,101,20),fontsize=12)
plt.savefig('hw1_a_3.png',dpi=300)
