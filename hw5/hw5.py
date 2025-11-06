import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

n=15
alpha=0.05
t=stats.t.ppf(1-alpha,df=n-1)

# one-tailed T-test
ts=np.loadtxt('TS.txt').reshape(-1,12)
annual_mean=np.nanmean(ts,axis=1)

recent=annual_mean[-n:]
past=annual_mean[0:n]

mean_past=np.nanmean(past)
std_past=np.nanstd(past)

mean_recent=np.nanmean(recent)
std_recent=np.nanstd(recent)

t_recent=(mean_recent-mean_past)/(std_recent/np.sqrt(n))
p_value=1-stats.t.cdf(t_recent,df=n-1)

print('-'*20)
print('one-tailed one sample T test')
print(f'mu={mean_past:.2f}; std={std_past:.2f}\nn ={n:03d}  ; x_bar={mean_recent:.2f} ; s={std_recent:.2f}')
if p_value<alpha:
    print('\nsignificant')
else:
    print('\nNot significant')
print(f'critical\tt-value:{t:.2e} ; alpha  :{alpha:.2e}')
print(f'sample  \tt-value:{t_recent:.2e} ; p-value:{p_value:.2e}')
print('-'*20)


# independent 2-sample test
t_value_indep,p_value_indep=stats.ttest_ind(recent,past,alternative='greater',equal_var=False)
print('independent T test')
print(f'x_bar1={mean_past:.2f}; s1={std_past:.2f}\nx_bar2={mean_recent:.2f}; s2={std_recent:.2f}')
print(f'n ={n:03d}')
if p_value<alpha:
    print('\nsignificant')
else:
    print('\nNot significant')
print(f'critical\tt-value:{t:.2e} ; alpha  :{alpha:.2e}')
print(f'sample  \tt-value:{t_value_indep:.2e} ; p-value:{p_value_indep:.2e}')

