import pandas as pd
import numpy as np

#store raw data in variable tedata
tedata = pd.read_csv('twentyeleven.csv')

#### Data Cleaning
#replacing '?' in Description column with np.nan
tedata.Description.replace('?',np.nan, inplace=True)

tedata=tedata.drop_duplicates()

tedata=tedata.dropna(subset=['Description'])

# group and store data in variable 'grouped'
grouped = tedata.groupby('Description').agg(total_sales_vol=('Quantity',np.sum),
                     total_revenue=('revenue',np.sum)).reset_index()


grouped.sort_values(by='total_sales_vol', ascending=False, inplace=True)

grouped.reset_index(drop=True, inplace=True)  # to reset jumbling of row indices

totqty = grouped.total_sales_vol.sum()

# Quantity function defined to get qty percent of each description item for total qty
def qtyfunc(x,y):
    z=(x/y)*100
    return z

# computing qtypct individually for sorted qty.
for i in range(0,grouped.shape[0]):
    #because we hadnt done reset index in grouped, it was throwing key error:0 initially as the key was not found. i.e. the indexes were causing issue
    grouped.loc[i,'qtypct']=qtyfunc(grouped.loc[i,'total_sales_vol'],totqty)

# computing cumuqtypct (cumulative qty %age)
for j in range(0,grouped.shape[0]):
    if (j==0):
        grouped.loc[j,'cumuqtypct']= grouped.loc[j,'qtypct']
       
    else :
        grouped.loc[j,'cumuqtypct']= grouped.loc[j,'qtypct'] + grouped.loc[j-1,'cumuqtypct']
       
       
##### now categorising items based on revenues as per second part of abc
## sort revenue
grouped.sort_values(by = 'total_revenue', ascending = False, inplace=True )
# can also use grouped = grouped.sort_values(by = 'total_revenue', ascending = False) but dont add inplace if youre using this- mistake made by me earlier

## reset row indices
grouped.reset_index(drop=True, inplace=True)

# now grouped ready to apply pct and cumupct
totrev= grouped['total_revenue'].sum()

# revenue percent function definition to get percentage revenue values
def revpct(x,y):
    z = (x/y)*100
    return z

# add revpct column and compute the same
for i in range(0, grouped.shape[0]):
    grouped.loc[i,'revpct'] = revpct(grouped.loc[i,'total_revenue'],totrev)


#add cumurevpct and compute the same
for i in range(0,grouped.shape[0]):
    if(i==0):
        grouped.loc[i,'cumurevpct']=grouped.loc[i,'revpct']
    else:
        grouped.loc[i,'cumurevpct']=grouped.loc[i,'revpct']+grouped.loc[i-1,'cumurevpct']


### add labels a b and c now to both cumuqtypct and cumurevpct

for i in range(0,grouped.shape[0]):
    # cumurevpct segmentation first
    if (grouped.loc[i,'cumurevpct']<70) & (grouped.loc[i,'cumurevpct']>=0):
        grouped.loc[i,'revsegment']='rA'                    
        # cumuqtypct in this block    
        if(grouped.loc[i,'cumuqtypct']<70) & (grouped.loc[i,'cumuqtypct']>=0):
            grouped.loc[i,'qtysegment']='qA'    
           
        elif (grouped.loc[i,'cumuqtypct']>=70) & (grouped.loc[i,'cumuqtypct']<90):    
            grouped.loc[i,'qtysegment']='qB'  
           
        else:
            grouped.loc[i,'qtysegment']='qC'  
                 
    elif (grouped.loc[i,'cumurevpct']>=70) & (grouped.loc[i,'cumurevpct']<90):
        grouped.loc[i,'revsegment']='rB'

        if (grouped.loc[i,'cumuqtypct']<70) & (grouped.loc[i,'cumuqtypct']>=0):
            grouped.loc[i,'qtysegment']='qA'    
           
        elif (grouped.loc[i,'cumuqtypct']>=70) & (grouped.loc[i,'cumuqtypct']<90):    
            grouped.loc[i,'qtysegment']='qB'  
           
        else:
            grouped.loc[i,'qtysegment']='qC'
    else:
        grouped.loc[i,'revsegment']='rC'
        if (grouped.loc[i,'cumuqtypct']<70) & (grouped.loc[i,'cumuqtypct']>=0):
            grouped.loc[i,'qtysegment']='qA'    
           
        elif (grouped.loc[i,'cumuqtypct']>=70) & (grouped.loc[i,'cumuqtypct']<90):    
            grouped.loc[i,'qtysegment']='qB'  
           
        else:
            grouped.loc[i,'qtysegment']='qC'

#concating both rev and qty segments with an '_'
grouped['finalsegment']=grouped['qtysegment'].str.cat(grouped['revsegment'], sep='_')

#print grouped to get the dataframe with ABC segments
