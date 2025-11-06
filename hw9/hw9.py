import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.stats import t
import copy

plt.rcParams['font.family'] = 'monospace'

# read data
ncfile=xr.open_dataset('sst.mon.mean.trefadj.anom.1880to2018.nc').sel(time=slice('1979-1-1','2019-1-1'))
lon=ncfile['lon']
lat=ncfile['lat']
time=ncfile['time']
sst=ncfile['sst']
sst_flatten=sst.values.reshape(time.size,-1)

nino34_file=np.loadtxt('nino34.long.anom.data.txt',usecols=np.arange(1,13),skiprows=109,max_rows=40)
nino34=nino34_file.flatten()

lon2,lat2=np.meshgrid(lon,lat)

# nino3.4 region
region_lon=[190,240]
region_lat=[-5,5]
region=mpatches.Rectangle((region_lon[0],region_lat[0]),width=region_lon[1]-region_lon[0],height=region_lat[1]-region_lat[0],linewidth=1,linestyle='dashed',edgecolor='k',facecolor='none',transform=ccrs.PlateCarree())
text=plt.Text(x=region_lon[0],y=region_lat[1]+2,text='Ni\u00F1o3.4',color='k',fontsize=8,transform=ccrs.PlateCarree())

# regression  X: nino3.4, Y: SST
X=np.vstack((nino34,np.ones(len(nino34)))).T
slope,intercept=np.linalg.lstsq(X,sst_flatten)[0]
# print(slope.shape,intercept.shape,nino34.shape,sst_flatten.shape)
sst_predict=intercept[None,:]+slope[None,:]*nino34[:,None]
slope=slope.reshape(lat.size,lon.size)

# significance test
sse=np.nansum((sst_predict-sst_flatten)**2,axis=0)
stand_err=(np.sqrt((sse/(time.size-2))/np.nansum((nino34-np.nanmean(nino34))**2))).reshape(lat.size,lon.size)
t_value=slope/stand_err
p_value=2*(1-t.cdf(np.abs(t_value),df=(time.size-2)))
significant=np.where(p_value<0.05,1,-1)

# plot significant mask
# plt.figure(figsize=(8,6))
# ax=plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
# ax.coastlines()
# grid=ax.gridlines(linestyle='-',alpha=0.7,draw_labels=True)
# grid.top_labels=False
# grid.left_labels=False
# plt.pcolormesh(lon2,lat2,significant,cmap=mcolors.ListedColormap(['grey','white']),transform=ccrs.PlateCarree())
# ax.add_patch(copy.copy(region))
# ax.add_artist(copy.copy(text))
# cbar=plt.colorbar(orientation='horizontal',ticks=[-1,1])
# cbar.ax.set_xticklabels(['Not Significant','Significant'])
# plt.title('Regression Significant Mask',fontsize=14)
# plt.savefig('regression_mask.png',dpi=450)


# plot regression map
fig,ax=plt.subplots(nrows=2,ncols=1,sharex='col',figsize=(7,6.5),subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
plt.suptitle('Regression Map of Ni\u00F1o3.4 Index to Global SST Anomaly',fontsize=14)
c0=ax[0].pcolormesh(lon2,lat2,slope,cmap='jet',transform=ccrs.PlateCarree(),vmin=-1,vmax=1)
ax[0].add_patch(copy.copy(region))
ax[0].add_artist(copy.copy(text))
ax[0].coastlines()
ax[0].add_feature(cfeature.LAND,facecolor='lightgrey')
ax[0].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
grid0=ax[0].gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid0.top_labels=False
grid0.right_labels=False
ax[0].set_title('a) Original Regression Map',fontsize=12)
# mask out p>0.05
mask=p_value<0.05
masked_slope=np.where(mask,slope,np.nan)
c1=ax[1].pcolormesh(lon2,lat2,masked_slope,cmap='jet',transform=ccrs.PlateCarree(),vmin=-1,vmax=1)
ax[1].add_patch(copy.copy(region))
ax[1].add_artist(copy.copy(text))
plt.colorbar(c1,ax=ax,orientation='vertical',extend='both',ticks=np.linspace(-1,1,11))
ax[1].coastlines()
ax[1].add_feature(cfeature.LAND,facecolor='lightgrey')
ax[1].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
grid1=ax[1].gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid1.top_labels=False
grid1.right_labels=False
ax[1].set_title('b) Masked Regression Map (p<0.05)',fontsize=12)
plt.savefig('regression_map(a,b).png',dpi=450)


# sst anomaly mean, std
fig,ax=plt.subplots(nrows=2,subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)},figsize=(7,6.5))
ax[0].set_title('SST Anomaly Mean over Time',fontsize=14)
ax[0].coastlines()
ax[0].add_feature(cfeature.LAND,facecolor='lightgrey')
ax[0].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
grid=ax[0].gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid.top_labels=False
grid.left_labels=False
c0=ax[0].pcolormesh(lon2,lat2,sst.mean(dim='time'),cmap='RdBu_r',transform=ccrs.PlateCarree(),vmin=-0.2,vmax=0.2)
plt.colorbar(c0,ax=ax[0],extend='both',orientation='horizontal')
ax[0].add_patch(copy.copy(region))
ax[0].add_artist(copy.copy(text))

ax[1].set_title('SST Anomaly STD over Time',fontsize=14)
ax[1].coastlines()
ax[1].add_feature(cfeature.LAND,facecolor='lightgrey')
ax[1].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
grid=ax[1].gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid.top_labels=False
grid.left_labels=False
c1=ax[1].pcolormesh(lon2,lat2,sst.std(dim='time'),cmap='rainbow',transform=ccrs.PlateCarree())
plt.colorbar(c1,ax=ax[1],extend='max',orientation='horizontal')
ax[1].add_patch(copy.copy(region))
ax[1].add_artist(copy.copy(text))
plt.tight_layout()
plt.savefig('sst_anom_mean.png',dpi=450)

# plot standard error
plt.clf()
plt.figure(figsize=(8,6))
ax=plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
plt.pcolormesh(lon2,lat2,stand_err.reshape(lat.size,lon.size),transform=ccrs.PlateCarree(),cmap='jet')
plt.colorbar(orientation='horizontal',extend='max')
ax.coastlines()
ax.add_feature(cfeature.LAND,facecolor='lightgrey')
grid=ax.gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid.top_labels=False
grid.left_labels=False
plt.contourf(lon2, lat2, mask, levels=[-1,0], colors='none', hatches=['////'], transform=ccrs.PlateCarree())
ax.add_patch(copy.copy(region))
ax.add_artist(copy.copy(text))
plt.title(r'Standard Error of $\beta_1$'+'\n(// = NOT significant)',fontsize=14)
plt.savefig('standard error.png',dpi=450)


# R^2
residual=sst_flatten-sst_predict
R2_flatten=1-np.sum(residual**2,axis=0)/np.sum((sst_flatten-np.nanmean(sst_flatten))**2,axis=0)
R2=R2_flatten.reshape(lat.size,lon.size)
R2=np.where(mask,R2,np.nan)
# plot
lon2,lat2=np.meshgrid(lon,lat)
plt.figure(figsize=(7,6.5))
ax=plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
ax.coastlines()
ax.add_feature(cfeature.LAND,facecolor='lightgrey')
ax.add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
grid=ax.gridlines(linestyle='-',alpha=0.7,draw_labels=True)
grid.top_labels=False
grid.left_labels=False
plt.pcolormesh(lon2,lat2,R2,cmap='jet',transform=ccrs.PlateCarree(),vmin=0,vmax=1)
plt.colorbar(orientation='horizontal',ticks=np.linspace(0,1,11))
ax.add_patch(copy.copy(region))
ax.add_artist(copy.copy(text))
plt.title('Masked $R^2$ of Regression NINO3.4 to Global SST Anomaly',fontsize=14)
plt.savefig('R2_map.png',dpi=450)


# season
months_dict={'DJF':[12,1,2],'MAM':[3,4,5],'JJA':[6,7,8],'SON':[9,10,11]}
ssta_seasonal=[('DJF',sst.sel(time=sst['time'].dt.month.isin(months_dict['DJF']))),\
               ('MAM',sst.sel(time=sst['time'].dt.month.isin(months_dict['MAM']))),\
               ('JJA',sst.sel(time=sst['time'].dt.month.isin(months_dict['JJA']))),\
               ('SON',sst.sel(time=sst['time'].dt.month.isin(months_dict['SON'])))]

fig,ax=plt.subplots(figsize=(8,5),nrows=2,ncols=2,sharex='all',sharey='all',subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
for i,(months,ssta) in enumerate(ssta_seasonal):
    # split nino3.4 with season
    if months=='DJF':
        prev_dec=nino34_file[:-1,11] # start with first yr. Dec.
        jan=nino34_file[1:,0] # start with second year Jan.
        feb=nino34_file[1:,1] # start with sec. yr. Feb.
        nino34_seasonal=np.column_stack((prev_dec,jan,feb)).flatten()
        nino34_seasonal=np.concatenate((nino34_file[0,:2],nino34_seasonal,[nino34_file[-1,11]])) # add 1st (Jan,Feb), last (Dec)
    else:
        nino34_seasonal=nino34_file[:,np.array(months_dict[months])-1].flatten()
    
    ssta=ssta.values.reshape(time.size*3//12,-1)
    # least square
    X=np.vstack((nino34_seasonal,np.ones(len(nino34_seasonal)))).T
    slope,intercept=np.linalg.lstsq(X,ssta)[0]
    sst_predict=intercept[None,:]+slope[None,:]*nino34[:,None]
    slope=slope.reshape(lat.size,lon.size)

    # significance test
    sse=np.nansum((sst_predict-sst_flatten)**2,axis=0)
    stand_err=(np.sqrt((sse/(time.size-2))/np.nansum((nino34-np.nanmean(nino34))**2))).reshape(lat.size,lon.size)
    t_value=slope/stand_err
    p_value=2*(1-t.cdf(np.abs(t_value),df=(time.size-2)))
    mask=p_value<0.05
    slope=np.where(mask,slope,np.nan)

    # plot
    c=ax[i//2,i%2].pcolormesh(lon2,lat2,slope,cmap='jet',transform=ccrs.PlateCarree(),vmin=-2,vmax=2)
    ax[i//2,i%2].add_patch(copy.copy(region))
    # ax[i//2,i%2].add_artist(copy.copy(text))
    ax[i//2,i%2].coastlines()
    ax[i//2,i%2].add_feature(cfeature.LAND,facecolor='lightgrey')
    ax[i//2,i%2].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
    grid=ax[i//2,i%2].gridlines(linestyle='-',alpha=0.7,draw_labels=True)
    grid.top_labels=False
    grid.right_labels=False
    ax[i//2,i%2].set_title(months,fontsize=12)

plt.colorbar(c,ax=ax[1,:],extend='both',orientation='horizontal')
plt.suptitle('Masked Regression Map',fontsize=14)
plt.savefig('regression_map_season.png',dpi=450)


# lagged Nino3.4
lag_months=[0,1,2,3,6,9,12,15,18]

plt.clf()
fig,ax=plt.subplots(figsize=(8,6),ncols=3,nrows=3,sharex='all',sharey='all',subplot_kw={'projection':ccrs.PlateCarree(central_longitude=180)})
for i,lag in enumerate(lag_months):
    if lag==0:
        nino34_lag=nino34
        sst_flatten_lag=sst_flatten
    else:
        nino34_lag=nino34[:-lag]
        sst_flatten_lag=sst_flatten[lag:,:]
    X=np.vstack((nino34_lag,np.ones(len(nino34_lag)))).T
    slope,intercept=np.linalg.lstsq(X,sst_flatten_lag)[0]
    sst_predict=intercept[None,:]+slope[None,:]*nino34_lag[:,None]
    slope=slope.reshape(lat.size,lon.size)

    # significance test
    sse=np.nansum((sst_predict-sst_flatten_lag)**2,axis=0)
    stand_err=(np.sqrt((sse/(time.size-lag-2))/np.nansum((nino34-np.nanmean(nino34))**2))).reshape(lat.size,lon.size)
    t_value=slope/stand_err
    p_value=2*(1-t.cdf(np.abs(t_value),df=(time.size-lag-2)))
    mask=p_value<0.05
    slope=np.where(mask,slope,np.nan)

    # plot
    c=ax[i//3,i%3].pcolormesh(lon2,lat2,slope,cmap='jet',transform=ccrs.PlateCarree(),vmin=-2,vmax=2)
    ax[i//3,i%3].coastlines()
    ax[i//3,i%3].add_feature(cfeature.LAND,facecolor='lightgrey')
    ax[i//3,i%3].add_feature(cfeature.LAKES,facecolor='none',edgecolor='k',linewidth=0.4)
    grid=ax[i//3,i%3].gridlines(linestyle='-',alpha=0.7,draw_labels=False)
    grid.top_labels=False
    grid.right_labels=False
    # ax[i//3,i%3].add_patch(copy.copy(region))
    ax[i//3,i%3].set_title(f'lag={lag:02d} months',fontsize=12)

plt.colorbar(c,ax=ax[2,:],extend='both',orientation='horizontal')
plt.suptitle('Lagged Regression of Ni\u00F1o3.4 Index to Global SST',fontsize=14)
plt.savefig('lag_regression_map.png',dpi=450)
