import numpy as np
from scipy import stats

alpha=0.05

ts=np.loadtxt('TS.txt').reshape(-1,12)
recent=ts[-3:,:]
past=ts[:3,:]

seasonal=np.tile(np.nanmean(ts,axis=0),recent.shape[0])

recent_ano=recent.flatten()-seasonal
past_ano=past.flatten()-seasonal

_,levene_p=stats.levene(recent_ano,past_ano)
equal_var=(levene_p>alpha)
result=stats.ttest_ind(recent_ano,past_ano,alternative='greater',equal_var=equal_var)
t_value,p_value,dof=result.statistic,result.pvalue,result.df
critical_t=stats.t.ppf(1-alpha,df=dof)
print('unpaired t-test (1-tailed)')
print(f'x_bar1={np.mean(recent_ano):.2f} ; s1={np.std(recent_ano,ddof=1):.2f} ; n1={recent_ano.shape[0]}')
print(f'x_bar2={np.mean(past_ano):.2f} ; s2={np.std(past_ano,ddof=1):.2f} ; n2={past_ano.shape[0]}')
print(f'same variance : {equal_var}')
print(f'significant : {p_value<alpha}')
print(f'\u03B1={alpha} ; critical t values={critical_t:.2f}')
print(f't-value={t_value:.2f} ; p-value={p_value:.2e} ; dof={dof:.2f}')
