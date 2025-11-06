import numpy as np
from scipy import stats

ts=np.loadtxt('TS.txt').reshape(-1,12)
recent=ts[-3:,:].flatten()
past=ts[:3,:].flatten()

d=recent-past
mean_d=np.mean(d)
std_d=np.std(d,ddof=1)

n=recent.shape[0]
alpha=0.05

# paired t-test (related)
critical_t=stats.t.ppf(1-alpha,df=n-1)

t_value,p_value=stats.ttest_rel(recent,past,alternative='greater')
print('paired t-test (1-tailed)')
print(f'significant : {p_value<alpha}')
print(f'\u03B1={alpha} ; critical t values={critical_t:.2f}')
print(f'n={n} ; \u00B5_d={mean_d:.2f} ; s_d={std_d:.2f}')
print(f't-value={t_value:.2f} ; p-value={p_value:.2e}\n')


# unpaired t-test (independent)
_,levene_p=stats.levene(recent,past)
equal_var=(levene_p>alpha)
result=stats.ttest_ind(recent,past,alternative='greater',equal_var=equal_var)
t_value,p_value,dof=result.statistic,result.pvalue,result.df
critical_t=stats.t.ppf(1-alpha,df=dof)
print('unpaired t-test (1-tailed)')
print(f'x_bar1={np.mean(recent):.2f} ; s1={np.std(recent,ddof=1):.2f} ; n1={recent.shape[0]}')
print(f'x_bar2={np.mean(past):.2f} ; s2={np.std(past,ddof=1):.2f} ; n2={past.shape[0]}')
print(f'same variance : {equal_var}')
print(f'significant : {p_value<alpha}')
print(f'\u03B1={alpha} ; critical t values={critical_t:.2f}')
print(f't-value={t_value:.2f} ; p-value={p_value:.2e} ; dof={dof:.2f}')
