# module for graphics and analysis functions for jupyter notebook
def histo_plot(dataframe_name, input_column):
    '''
    renders histogram of desired quantity: 
    input 1st arg is dataframe must be winsorized data
    input 2nd arg string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    output is histogram
    '''
    #import necessary libraries
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # determine which time is to be plotted
    if input_column == 'Elapsed time':
        label_strng = 'cln_elps_tm_sec'
    elif input_column == 'Adjusted finish time':
        label_strng = 'cln_crrct_tm_sec'
    elif input_column == 'Handicap time':
        label_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid time column selection')

    # make strings from input column for the title of the plot
    xlabel_strng = input_column + ' in seconds'
    title_strng = input_column + ' for yrs 2002-2019'
    # render plot
    plt.hist(dataframe_name[label_strng])
    plt.xlabel(xlabel_strng)
    plt.ylabel('count')
    plt.title(title_strng, fontsize=16)
    pass

def sail_box_plot(dataframe_name, input_column, by_column):
    '''
    renders box plot of desired quantity: 
    input 1st arg is dataframe must be winsorized data
    input 2nd arg string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 3rd arg string factor, "by" column, 'Year', 'Boat class', 'Boat division'
    output is box plot
    '''
    #import necessary libraries
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')
    # determine which time is to be plotted
    if input_column == 'Elapsed time':
        label_strng = 'cln_elps_tm_sec'
    elif input_column == 'Adjusted finish time':
        label_strng = 'cln_crrct_tm_sec'
    elif input_column == 'Handicap time':
        label_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid time column selection')

    # make strings from input column for the title of the plot
    xlabel_strng = input_column + ' in seconds'

    # determine which by_column to use
    if by_column == 'Year':
        by_strng = 'Year'
    elif by_column == 'Boat class':
        by_strng = 'Boat_class'
    elif by_column == 'Boat division':
        by_strng = 'Division_only'
    else:
        raise IOError('Invalid by column selection')
    title_strng = input_column + ' by ' + by_column + ' for yrs 2002-2019'
    # render plot
    dataframe_name.boxplot(by=by_strng, column=label_strng)
    plt.ylabel(xlabel_strng)
    plt.xlabel(by_column)
    plt.title(title_strng, fontsize=16)
    pass

def sail_scttr_plot(dataframe_name, x_column, y_column, by_column=None, lmfit=False):
    '''
    renders scatterplot of desired quantities: 
    input 1st arg is dataframe, must be winsorized data
    input 2nd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 3rd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 4th arg is string input, "by" column, 'Year', 'Boat class', 'Boat division' default is None
    input 5th arg is bool, whether to fit or not.  default is False
    output is scatterplot
    '''
    # import seaborn library
    import seaborn as sns
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # determine which time is abcissa
    if x_column == 'Elapsed time':
        x_strng = 'cln_elps_tm_sec'
    elif x_column == 'Adjusted finish time':
        x_strng = 'cln_crrct_tm_sec'
    elif x_column == 'Handicap time':
        x_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid x time column selection')
    x_label = x_column + ' in seconds'

    # determine which time is ordinate
    if y_column == 'Elapsed time':
        y_strng = 'cln_elps_tm_sec'
    elif y_column == 'Adjusted finish time':
        y_strng = 'cln_crrct_tm_sec'
    elif y_column == 'Handicap time':
        y_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid y time column selection')
    y_label = y_column + ' in seconds'

    # determine which by_column to use
    if by_column == None:
        by_strng = None
    elif by_column == 'Year':
        by_strng = 'Year'
    elif by_column == 'Boat class':
        by_strng = 'Boat_class'
    elif by_column == 'Boat division':
        by_strng = 'Division_only'
    else:
        raise IOError('Invalid by column selection')
    #create title for plot
    title_strng = y_column + ' vs ' + x_column + ' for yrs 2002-2019'

    g = sns.lmplot(x_strng, y_strng, dataframe_name, hue=by_strng,fit_reg = lmfit, palette="Set2")
    g = (g.set_axis_labels(x_label,y_label))
    plt.title(title_strng)
    plt.show(g)
    pass

def sail_anva_byyr(dataframe_name, input_column, Yr1, Yr2, Yr3):
    '''
    input 1st arg is dataframe must be winsorized data
    input 2nd arg string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 3rd, 4th, 5th arg are integers for years of analysis
    output is a printed p-value of the anova test
    '''
    # import stats library
    from scipy import stats

    # determine which time is to analyzed by anova
    if input_column == 'Elapsed time':
        label_strng = 'cln_elps_tm_sec'
    elif input_column == 'Adjusted finish time':
        label_strng = 'cln_crrct_tm_sec'
    elif input_column == 'Handicap time':
        label_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid time column selection')

    if (Yr1 < 2002 or Yr1 > 2019):
        raise IOError('Year must be between 2002 and 2019, inclusive')
    if (Yr2 < 2002 or Yr1 > 2019):
        raise IOError('Year must be between 2002 and 2019, inclusive')
    if (Yr3 < 2002 or Yr1 > 2019):
        raise IOError('Year must be between 2002 and 2019, inclusive')

    a = dataframe_name[dataframe_name['Year']==Yr1][label_strng]
    b = dataframe_name[dataframe_name['Year']==Yr2][label_strng]
    c = dataframe_name[dataframe_name['Year']==Yr3][label_strng]
    print(stats.f_oneway(a, b, c))
    pass

def sail_scttr_plot_sbst(dataframe_name, x_column, y_column, Sbslc1, Sbslc1val, Sbslc2 = None, Sbslc2val = None, by_column=None, lmfit=False):
    '''
    renders scatterplot of desired quantities: 
    input 1st arg is dataframe, must be winsorized data
    input 2nd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 3rd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 4th arg is string input, Subslice column 1: columns of 'Year', 'Boat class', 'Boat division': required
    input 5th arg is string input, Subslice value 1: value from columns of 'Year', 'Boat class', 'Boat division': value required
    input 6th arg is string input, Subslice column 1: columns of 'Year', 'Boat class', 'Boat division': default is None
    input 7th arg is string input, Subslice value 2: value from columns of 'Year', 'Boat class', 'Boat division': default is None
    input 8th arg is string input, "by" column, 'Year', 'Boat class', 'Boat division' default is None but required if Sbslc2 is specified
    input 9th arg is bool, whether to fit or not.  default is False
    output is scatterplot
    '''
    # import seaborn library
    import seaborn as sns
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # determine which time is abcissa
    if x_column == 'Elapsed time':
        x_strng = 'cln_elps_tm_sec'
    elif x_column == 'Adjusted finish time':
        x_strng = 'cln_crrct_tm_sec'
    elif x_column == 'Handicap time':
        x_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid x time column selection')
    x_label = x_column + ' in seconds'

    # determine which time is ordinate
    if y_column == 'Elapsed time':
        y_strng = 'cln_elps_tm_sec'
    elif y_column == 'Adjusted finish time':
        y_strng = 'cln_crrct_tm_sec'
    elif y_column == 'Handicap time':
        y_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid y time column selection')
    y_label = y_column + ' in seconds'

    # determine which by_column to use
    if by_column == None:
        by_strng = None
    elif by_column == 'Year':
        by_strng = 'Year'
    elif by_column == 'Boat class':
        by_strng = 'Boat_class'
    elif by_column == 'Boat division':
        by_strng = 'Division_only'
    else:
        raise IOError('Invalid by column selection')

    # determine which subset1 column to use
    if Sbslc1 == 'Year':
        Sbslc1_strng = 'Year'
    elif Sbslc1 == 'Boat class':
        Sbslc1_strng = 'Boat_class'
    elif Sbslc1 == 'Boat division':
        Sbslc1_strng = 'Division_only'
    else:
        raise IOError('Invalid subset1 column selection')

    # determine which subset2 column to use
    if Sbslc2 not in [None, 'Year','Boat class','Boat division']:
        raise IOError('Invalid subset2 column selection')
    elif Sbslc2 == None:
        Sbslc2_strng = None
    if Sbslc2 == 'Year':
        Sbslc2_strng = 'Year'
    elif Sbslc2 == 'Boat class':
        Sbslc2_strng = 'Boat_class'
    elif Sbslc2 == 'Boat division':
        Sbslc2_strng = 'Division_only'

    #create title for plot
    title_strng = y_column + ' vs ' + x_column + ' for yrs 2002-2019'

    if Sbslc2 == None:
        g = sns.lmplot(x_strng, y_strng, dataframe_name[dataframe_name[Sbslc1_strng]\
            ==Sbslc1val], hue=by_strng, fit_reg = lmfit, palette="Set2")
    else:
        g = sns.lmplot(x_strng, y_strng, dataframe_name[(dataframe_name[Sbslc1_strng]\
                    ==Sbslc1val) & (dataframe_name[Sbslc2_strng]\
                    ==Sbslc2val)], hue=by_strng, fit_reg = lmfit, palette="Set2")

    g = (g.set_axis_labels(x_label,y_label))
    plt.title(title_strng)
    plt.show(g)
    pass

# function to calculate regressions over all years for Division 1 boats
def yr_rgrss_fxn(dataframe_name, x_column, y_column, sample_no):
    '''
    performs linear regression on input variables of input dataframe
    input 1: data frame on which to perform regression, must be winsorized
    input 2nd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 3rd arg is string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    input 4th arg is integer for number of iterations over which to average r coeff from regression
    output is line plot with r-values between x,y inputs for each race year
    '''
    #import required modules
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')
    from sklearn import preprocessing, svm 
    from sklearn.model_selection import train_test_split 
    from sklearn.linear_model import LinearRegression 
    import numpy as np
    # determine which time is abcissa
    if x_column == 'Elapsed time':
        x_strng = 'cln_elps_tm_sec'
    elif x_column == 'Adjusted finish time':
        x_strng = 'cln_crrct_tm_sec'
    elif x_column == 'Handicap time':
        x_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid x time column selection')
    x_label = x_column + ' in seconds'

    # determine which time is ordinate
    if y_column == 'Elapsed time':
        y_strng = 'cln_elps_tm_sec'
    elif y_column == 'Adjusted finish time':
        y_strng = 'cln_crrct_tm_sec'
    elif y_column == 'Handicap time':
        y_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid y time column selection')

    # initialize list to save correlations by year
    yr_corr = []
    for yr in range(2002,2019):
        rscoresum = 0
        for trl in range(sample_no):
            temp_df = dataframe_name[(dataframe_name['Division_only']=='Division I -')\
                                        & (dataframe_name['Year']== yr)]
            temp_df_binary = temp_df[[x_strng, y_strng]]
            temp_df_binary.columns = [x_strng, y_strng]
            X = np.array(temp_df_binary[x_strng]).reshape(-1, 1) 
            y = np.array(temp_df_binary[y_strng]).reshape(-1, 1) 

            # Dropping any rows with Nan values 
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25) 

            # Splitting the data into training and testing data 
            regr = LinearRegression() 

            regr.fit(X_train, y_train) 
            rscore = regr.score(X_test, y_test)
            rscoresum = rscore + rscoresum
        yr_corr = yr_corr + [(yr, rscoresum/sample_no)]

    x_val = [x[0] for x in yr_corr]
    y_val = [x[1] for x in yr_corr]

    ylblstrng = 'R value (avg of ' + str(sample_no) + ' trials)'
    title_strng = 'Correlation of ' + y_column + ' to ' + x_column + ' Division 1 2002-2018'
    plt.plot(x_val,y_val)
    plt.xlabel('Race year')
    plt.ylabel(ylblstrng)
    plt.title(title_strng, fontsize=16)
    plt.show()
    pass

# function to count number of disqualifications, grouped by year
def disqual_count(dataframe_name, disqual_type):
    '''
    function to count number of disqualifications of each type for each race year.  These are
        counts and the same across all original time columns as pulled
    input 1st arg: dataframe name, MUST NOT BE WINSORIZED
    input 2nd arg: string value of disqual, must be one of: 'DNF' for Did Not Finish, 'DNS' for Did Not Start or 'Retired'
    output is a bar plot
    '''
    #import necessary libraries
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # determine which time is to be plotted
    if disqual_type not in ['DNF', 'DNS', 'Retired']:
        raise IOError('Disqualification type not valid')
    else:
        ylblstrng = 'Boats that ' + disqual_type
        title_strng = 'Detroit-Mackinac boats that ' + disqual_type + ' All divisions 2002-2019' 
        dataframe_name[dataframe_name['Elapsed_Time'] == disqual_type].groupby('Year')['Elapsed_Time'].count().\
        plot.bar(color='b')
        plt.xlabel('Race year')
        plt.ylabel(ylblstrng)
        plt.title(title_strng, fontsize=16)
    pass

# function to calculate time per input column by division by year
def  mean_by_div(dataframe_name, divsn, input_column):
    '''
    function to calculate and plot aggregate fxn of times by year and division
    input 1st arg: dataframe name, must be winsorized data
    input 2nd arg: string divion name in ['Division I -', 'Division II ', 'Division III', 'Division IV ','Division V -']
    input 3rd arg: string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    output is bar plot
    '''
    #import necessary libraries
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # determine which time is to be plotted
    if input_column == 'Elapsed time':
        label_strng = 'cln_elps_tm_sec'
    elif input_column == 'Adjusted finish time':
        label_strng = 'cln_crrct_tm_sec'
    elif input_column == 'Handicap time':
        label_strng = 'crctn_in_sec'
    else:
        raise IOError('Invalid time column selection')

    # determine if divsn is correct
    if divsn not in ['Division I -', 'Division II ', 'Division III', 'Division IV ','Division V -']:
        raise IOError('Invalid division selection')
    else:
        # render plot for aggregate function
        ylblstrng = 'Mean ' + input_column
        title_strng = 'Detroit-Mackinac race ' + ylblstrng +' ' + divsn + ' 2002-2019'
        dataframe_name[dataframe_name['Division_only']==divsn].groupby('Year')[label_strng].mean()\
            .plot.bar(color='b')
        plt.xlabel('Race year')
        plt.ylabel(ylblstrng)
        plt.title(title_strng, fontsize=16)

    pass

# function to calculate time per input column by division by year
def  entry_count(dataframe_name):
    '''
    function to calculate and plot aggregate fxn of times by year and division
    input 1st arg: dataframe name, MUST NOT BE WINSORIZED data
    input 2nd arg: string divion name in ['Division I -', 'Division II ', 'Division III', 'Division IV ','Division V -']
    input 3rd arg: string column name must be variable: 'Elapsed time', 'Adjusted finish time', 'Handicap time'
    output is bar plot
    '''
    #import necessary libraries
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    # render plot for aggregate function
    dataframe_name.groupby('Year')['Elapsed_Time'].count().plot.bar(color='b')
    plt.xlabel('Race year')
    plt.ylabel('Boats finishing')
    plt.title('Detroit-Mackinac entrants 2002-2019', fontsize=16)

    pass



