import numpy as np
import matplotlib.pyplot as plt

# read data
ts=np.loadtxt('./TS.txt')

outfile=open('outfile.txt','w')

# 3.1.a
mean=np.mean(ts)
std=np.std(ts)
outfile.write('3.1.a\n')
outfile.write(f'Mean = {mean:.2f}\nSTD = {std:.2f}\n')

# 3.1.b
outfile.write('\n3.1.b\n')
for i in range(1,4):
    outfile.write(f'mean + {i}*STD = {mean+i*std:.2f}\n')
    outfile.write(f'mean - {i}*STD = {mean-i*std:.2f}\n')

# 3.1.c
outfile.write('\n3.1.c\n')

total=len(ts)
for i in range(1,4):
    lower=mean-i*std
    upper=mean+i*std
    inner=len(ts[(ts>lower) & (ts<upper)])
    percentage=inner/total
    outfile.write(f'mean +- 1*STD = {percentage*100:.2f}%\n')