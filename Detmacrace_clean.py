# import numpy and pandas
def clean_fxn(filename):
    '''
    cleans webscraping data
    input is csv file of filename
    output is two dataframes - sail_data and sail_data_winsorized
    '''
    import pandas as pd
    import numpy as np

    # read in csv files
    sail_data = pd.read_csv('detmacraceresults.csv', names=['Division_course', 'Year', \
        'Sail_No','Boat_name', 'Finish_time', 'Elapsed_Time', 'Corrected_Time',\
        'Boat_class', 'Division_placing'])

    #Duplicate elapsed time and corrected time columns without DNS, DNF, Retired for analysis
    sail_data['cln_elps_tm'] = sail_data['Elapsed_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)
    sail_data['cln_crrct_tm'] = sail_data['Corrected_Time'].replace(['DNS', 'DNF', 'Retired'],np.nan)

    #use pdtime_cnvrt fxn to calculate correction time in seconds
    sail_data['crctn_in_sec'] = pdtime_cnvrt(sail_data, 'cln_elps_tm') - \
        pdtime_cnvrt(sail_data, 'cln_crrct_tm')

    #Create new winsorized data files without outliers, found only 1 mistyped over 200,000
    sail_data_winsor = sail_data.loc[abs(sail_data['crctn_in_sec']) < 200000]

    #Divison and course name are merged, break out Division_only to allow analysis by division
    sail_data_winsor['Division_only'] = sail_data_winsor['Division_course'].str.slice(0,12)
    sail_data['Division_only'] = sail_data['Division_course'].str.slice(0,12)
    return sail_data, sail_data_winsor

# #write to csv file to pull back in for graphical analysis
# sail_data_winsor.to_csv('sail_data_winsor.csv', header=False, index=False)
# sail_data.to_csv('sail_data.csv', header=False, index=False)

#Define function to convert time strings to seconds for analysis
def pdtime_cnvrt(dtafrm, timecolname):
    import pandas as pd
    import numpy as np
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
