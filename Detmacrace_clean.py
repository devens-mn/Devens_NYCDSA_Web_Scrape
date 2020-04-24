import pandas as pd
import numpy as np
#import data from file created in webscraping script
sail_data = pd.read_csv('detmacraceresults.csv', names=['Division', 'Year', 'Sail_No',\
    'Boat_name', 'Finish_time', 'Elapsed_Time', 'Corrected_Time', 'Boat_class', 'Division_placing'])

# need to get rid of 'DNS', 'DNF', 'Retired' which are scatter throughout
sail_data2['clen_elps_tm'] = sail_data2['Elapsed_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)

# times are coming in as strings, will need to convert to numeric, go with seconds can't find
# something that allows addition/subtraction between hh:mm:
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

