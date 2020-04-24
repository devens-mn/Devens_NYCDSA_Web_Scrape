# import modules for data manipulation
import pandas as pd
import numpy as np

#read in two data files, 2019 and 2002-2018
sail_data = pd.read_csv('detmacraceresults.csv', names=['Division_course', 'Year', 'Sail_No',\
    'Boat_name', 'Finish_time', 'Elapsed_Time', 'Corrected_Time', 'Boat_class', 'Division_placing'])
sail_data_2019 = pd.read_csv('detmacraceresults_2019.csv', names=['Division_course', 'Year', 'Sail_No',\
    'Boat_name', 'Finish_time', 'Elapsed_Time', 'Corrected_Time', 'Boat_class', 'Division_placing'])

# replace DNF, DNS, Retired with nones for processing
sail_data['cln_elps_tm'] = sail_data['Elapsed_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)
sail_data['cln_crrct_tm'] = sail_data['Corrected_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)
sail_data_2019['cln_elps_tm'] = sail_data_2019['Elapsed_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)
sail_data_2019['cln_crrct_tm'] = sail_data_2019['Corrected_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)

# define function to convert time strings to seconds for analysis
def pdtime_cnvrt(dtafrm, timecolname):
    # new data frame with split value columns 
    new = dtafrm[timecolname].str.split(":", expand = True)
    # columns to overwrite and hold hh,mm,ss strngs
    dtafrm['hh'] = new[0]
    dtafrm['mm'] = new[1]
    dtafrm['ss'] = new[2]
    # create new time column in sec
    outptcolnam = timecolname +'_sec'
    dtafrm[outptcolnam] = pd.to_numeric(dtafrm['hh'], errors='coerce')*3600 +\
        pd.to_numeric(dtafrm['mm'], errors='coerce')*60 +\
        pd.to_numeric(dtafrm['ss'], errors='coerce')
    return dtafrm[outptcolnam]

# use pdtime_cnvrt fxn to calculate correction time in seconds
sail_data['crctn_in_sec'] = pdtime_cnvrt(sail_data, 'cln_elps_tm') - \
    pdtime_cnvrt(sail_data, 'cln_crrct_tm')
sail_data_2019['crctn_in_sec'] = pdtime_cnvrt(sail_data_2019, 'cln_elps_tm') - \
    pdtime_cnvrt(sail_data_2019, 'cln_crrct_tm')

# create new data frames with winsorized correction time data, but keep old data frame to count DNFs
# only found one greater than 20,000sec, and that was due to mistyping on website
sail_data_winsor = sail_data.loc[abs(sail_data['crctn_in_sec']) < 200000]
sail_data_2019_winsor = sail_data_2019.loc[abs(sail_data['crctn_in_sec']) < 200000]

#merge winsorized and original files
merge_sail_winsor = pd.concat([sail_data_2019_winsor, sail_data_winsor], axis = 0)
merge_sail = pd.concat([sail_data_2019, sail_data], axis = 0)

# Divison and course name are merged, break out Division_only to allow analysis by division
merge_sail_winsor['Division_only'] = merge_sail_winsor['Division_course'].str.slice(0,12)
merge_sail['Division_only'] = merge_sail['Division_course'].str.slice(0,12)

merge_sail_winsor.to_csv('merge_sail_winsor.csv')
merge_sail.to_csv('merge_sail.csv')

