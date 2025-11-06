import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

ts=np.loadtxt('TS.txt')
ts_seasonal=np.tile(np.nanmean(ts.reshape(-1,12),axis=0),ts.shape[0]//12)
ts_anomaly=ts-ts_seasonal

anomaly_mean,anomaly_std=np.mean(ts_anomaly),np.std(ts_anomaly)

standard=(ts_anomaly-anomaly_mean)/anomaly_std
pdf=norm.pdf(np.linspace(-1.5,1.5,200),anomaly_mean,anomaly_std)
standard_pdf=norm.pdf(np.linspace(-4,4,200),0,1)

plt.figure(figsize=(9,6))
plt.title(f'Histogram of $T_s$ Anomaly and Normal Distribution\n$\\mu$ : {anomaly_mean:.2f}, $\\sigma$ : {anomaly_std:.2f}',fontsize=16)
count,bins,_=plt.hist(ts_anomaly,bins=50,color='darkblue',edgecolor='k',linewidth=0.7)
dx=bins[1]-bins[0]
plt.plot(np.linspace(-1.5,1.5,200),pdf*ts_anomaly.shape[0]*dx,'r-',label='normal distribution')
plt.xlim(-1.5,1.5)
plt.ylim(0,100)
plt.legend()
plt.xlabel('$T_s$ anomaly [degC]',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.savefig('hw1_a_3_2.png',dpi=300)

plt.clf()
plt.figure(figsize=(9,6))
plt.title('standard normal distribution of anomaly of Ts')
count,bins,_=plt.hist(standard,bins=50,color='darkblue',edgecolor='k',linewidth=0.7)
dx=bins[1]-bins[0]
plt.plot(np.linspace(-4,4,200),standard_pdf*standard.shape[0]*dx,'r-',label='normal distribution')
plt.xlim(-4,4)
plt.ylim(0,100)
plt.legend()
plt.xlabel('$T_s$ std ',fontsize=14)
plt.ylabel('# of months',fontsize=14)
plt.savefig('standard.png',dpi=300)
