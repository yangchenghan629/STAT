import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def R2_score(y_true,y_pred):
    sse=np.sum((y_true-y_pred)**2)
    sst=np.sum((y_true-np.mean(y_true))**2)
    r2=1-(sse/sst)
    return r2

train_data=pd.read_excel('Data_slr_training_hw.xlsx')
test_data=pd.read_excel('Data_slr_verification_hw.xlsx')

time=pd.to_datetime(train_data['Time'],format='%Y%m')

x_train=train_data['Temp.Hengchun'].values
y_train=train_data['Temp.Taipei'].values

x_test=test_data['Temp.Hengchun'].values
y_test=test_data['Temp.Taipei'].values

correl_coef_train=np.corrcoef(x_train,y_train)[0,1]

# plot the scatter plot and box plot of Y
fig,ax=plt.subplots(ncols=2,nrows=1,figsize=(8,6))
fig.suptitle('Scatter and Box Plot of Training Y (Temp.Taipei)',fontsize=14)
ax[0].scatter(x_train,y_train,color='blue',s=[5])
ax[0].set_title(f'Scatter Plot\ncorrelation coefficient: {correl_coef_train:.2f}',fontsize=12)
ax[0].set_xlabel('X: Temp.Hengchun [degC]',fontsize=10)
ax[0].set_ylabel('Y: Temp.Taipei [degC]',fontsize=10)
ax[0].set_xticks(np.arange(18,31,2))
ax[0].set_yticks(np.arange(13,33,2))
ax[0].grid()

ax[1].boxplot([x_train,y_train],vert=True,tick_labels=['X: Hengchun','Y: Taipei'])
ax[1].set_title('Box Plot',fontsize=12)
ax[1].set_ylabel('Temp [degC]',fontsize=10)
plt.tight_layout()
plt.savefig('Y_scatter_box.png',dpi=500)

# least square approximation
x_matrix=np.vstack((x_train,np.ones(len(x_train)))).T
m,c=np.linalg.lstsq(x_matrix,y_train)[0]
# estimate
y_train_pred=m*x_train+c
# R2 score
R2_train=R2_score(y_train,y_train_pred)


# loss function, RMSE
rmse_train=np.sqrt(np.mean((y_train-y_train_pred)**2))
y_test_pred=m*x_test+c
rmse_test=np.sqrt(np.mean((y_test-y_test_pred)**2))

x=[0.4,0.6]
labels=['Training','Test']
plt.figure(figsize=(8,6))
bar=plt.bar(x,[rmse_train,rmse_test],color=['blue','orange'],width=0.1)
plt.xticks(x,labels,fontsize=12)
plt.yticks(np.arange(0,1.7,0.2))
plt.bar_label(bar,[f'{rmse_train:.4f}',f'{rmse_test:.4f}'],fontsize=12)
plt.title('Root Mean Squared Error (RMSE) for Training and Test Data',fontsize=14)
plt.ylabel('RMSE',fontsize=12)
plt.grid(axis='y')
plt.savefig('RMSE.png',dpi=500)

# plot the training results
plt.figure(figsize=(6,6))
plt.scatter(x_train,y_train,color='blue',s=[5],label='Training Data')
plt.plot(x_train,y_train_pred,color='red',label='Fitted Line')
plt.text(x=20,y=22.5,s=f'Y={c:+.2f}{m:+.2f}X',fontsize=12,color='red')
plt.title(f'Training Data and Fitted Line\n$R^2$={R2_train:.4f}',fontsize=14)
plt.xlabel('X: Temp.Hengchun [degC]')
plt.ylabel('Y: Temp.Taipei [degC]')
plt.legend()
plt.grid()
plt.savefig('training_result.png',dpi=500)

# plot histogram of residuals
residual_train=y_train-y_train_pred
residual_test=y_test-y_test_pred
fig,ax=plt.subplots(ncols=2,nrows=1,figsize=(8,6))
fig.suptitle('Histogram of Residuals',fontsize=14)
ax[0].hist(residual_train,bins=30,)
ax[0].set_title(f'Training Data\nmean: {np.nanmean(residual_train):.2f} STD: {np.nanstd(residual_train):.2f}',fontsize=12)
ax[0].set_xlabel('Residuals',fontsize=10)
ax[0].set_ylabel('# of samples',fontsize=10)
ax[0].set_xticks(np.arange(-4,4.1,1))
ax[0].set_yticks(np.arange(0,31,5))
ax[0].set_xlim(-4,4)

ax[1].hist(residual_test,bins=20)
ax[1].set_title(f'Test Data\nmean: {np.nanmean(residual_test):.2f} STD: {np.nanstd(residual_test):.2f}',fontsize=12)
ax[1].set_xlabel('Residuals',fontsize=10)
ax[1].set_ylabel('# of samples',fontsize=10)
ax[1].set_xticks(np.arange(-4,4.1,1))
ax[1].set_yticks(np.arange(0,11,2))
ax[1].set_xlim(-4,4)
plt.savefig('residuals.png',dpi=500)

