import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the city for the data you would like to see; Chicago, New York, or Washington: ')
        if city.lower() not in ('chicago', 'new york', 'washington'):
            print('Please re-enter the city')
            continue
        else:
            if city.lower() == 'new york':
                city = 'new york city'
            print('You have selected {}.'.format(city))
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter which month you would like to see data for; All, January, February, March, April, May, June: ')
        if month.lower() not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print('Please re-enter the month')
            continue
        else:
            print('You have selected {}.'.format(month))
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter which day you would like to see data for; All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday: ')
        if day.lower() not in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            print('Please re-enter the day of week')
            continue
        else:
            print('You have selected {}.'.format(day))
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df =  pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.day_name()
    df['num_day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    #print(df)
    return df






def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    months = ['January', 'February', 'March', 'April', 'May', 'June'] # Decided to convert months back last minute
    popular_month = months[df['month'].mode()[0]-1] #Get the most common value of month
    month_table = df.groupby('month').count()[['Start Time']].sort_values(by='Start Time',ascending=False) # Create a table of months and count of start times and order by most popular day

    # TO DO: display the most common day of week
    day_of_week_translator = {0: 'Monday',1: 'Tuesday',2: 'Wednesday',3: 'Thursday',4: 'Friday',5: 'Saturday',6: 'Sunday'} ## create a 'lookup' dictionary for the numeric days
    num_popular_day = df['num_day_of_week'].mode()[0]  #determine the most popular day, numeric
    popular_day = day_of_week_translator[num_popular_day]  # Find the name of the popular day from the lookup dictionary
    day_table = df.groupby('day_of_week').count()[['Start Time']].sort_values(by='Start Time',ascending=False) # Create a table of days and count of start times and order by most popular day
    # Refered to this https://data36.com/pandas-tutorial-2-aggregation-and-grouping/ for some data aggregation material

    most_monthly_trips = month_table.iloc[0]['Start Time'] #Got .iloc from stackoverflow question and https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iloc.html
    most_day_trips = day_table.iloc[0]['Start Time']
    ### Note the methods above won't return both values if there are ties, should add some form of checking or just return the entire mode!

    if len(month_table) == 1 and len(day_table) == 1: #If the length the tables are both 1, we selected a month and day.
        print('\n\nYou selected the month {}, and day {}, so those are most popular!'.format(popular_month,popular_day))
        print('\nThere are {} trips for that day of that month.'.format(most_monthly_trips))

    elif len(month_table) == 1 and len(day_table) != 1: # Month was selected but not the day
        print("You selected the month {} so that's the most popular!.".format(popular_month))
        print('\nThere are {} trips in that month.'.format(most_monthly_trips))
        print('\n\nYou selected all the days, and the most popular day is {}.'.format(popular_day))
        print('\nHere is the count of "Start Time" for all the days (in order of most popular):\n\n',day_table)

    elif len(month_table) != 1 and len(day_table) == 1:  # Day was selected but not the month
        print('You selected all the months, and the most popular is {}.'.format(popular_month))
        print('\nHere is the count of "Start Time" for all the months (in order of most popular):\n\n',month_table)
        print("\n\nYou selected the day {} so that's the most popular!".format(popular_day))
        print('\nThere are {} trips in that day.'.format(most_day_trips))

    else: # Neither month nor day was selected
        print('You selected all the months, and the most popular is {}.'.format(popular_month))
        print('\nHere is the count of "Start Time" for all the months (in order of most popular):\n\n',month_table)
        print('\n\nYou selected all the days, and the most popular day is {}.'.format(popular_day))
        print('\nHere is the count of "Start Time" for all the days (in order of most popular):\n\n',day_table)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour #Create an 'hour' column and convert start time to hour
    popular_hour = (df['hour'].mode()[0])    #Find the most common hour from that col
    hour_table = df.groupby('hour').count()[['Start Time']].sort_values(by='Start Time',ascending=False) #Create a table of hour start times, grouped by hour, descending
    total_trans = int(hour_table['Start Time'].sum()) # Calculate how many transactions there are
    hour_table['Percentage'] = hour_table['Start Time'] / total_trans * 100 #Create a colunm that calculates the percentage of the count of each hour
    most_hour_trips = hour_table.iloc[0]['Start Time']


    print('\n\nThe most popular start hour for the selected month(s)/day(s) is {}'.format(popular_hour))
    print('\nThere are {} trips that occurred at that hour'.format(most_hour_trips))
    print('\nThe percentage of trips for each hour is shown below:\n\n',hour_table['Percentage'])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)






def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_table = df.groupby('Start Station').count()[['Start Time']].sort_values(by='Start Time',ascending=False) #Create a table of counts of start station ordered most frequent to least
    print('\nThe most commonly used start station is',start_station_table.index.values[0]) # Get the first row lable from the table
    print('\nThe Start Station was used',start_station_table.iloc[0]['Start Time'],'times.') # get the first column value in the table

    # TO DO: display most commonly used end station
    end_station_table = df.groupby('End Station').count()[['Start Time']].sort_values(by='Start Time',ascending=False) #Create a table of counts of start station ordered most frequent to least

    print('\nThe most commonly used end station is',end_station_table.index.values[0]) # Get the first row lable from the table
    print('\nThe End Station was used',end_station_table.iloc[0]['Start Time'],'times.') # get the first column value in the table

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' with ' + df['End Station']
    print('\nThe most common combination of start station and end station was',df['start_end_station'].mode()[0])
    print('\nHere is the top ten combinations:\n\n',df['start_end_station'].value_counts()[:10])



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)






def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    total_travel_time_seconds = df['Trip Duration'].sum() #Sum the travel time column, in seconds -- Reference https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_timedelta.html
    total_travel_time = pd.to_timedelta(total_travel_time_seconds, unit='s') #Convert total_travel_time_seconds to hrs/minutes/seconds format
    print('The total travel time for this query is',total_travel_time,'(hh:mm:ss).')

    # TO DO: display mean travel time
    average_travel_time_seconds = df['Trip Duration'].mean() #Average the travel time column, in seconds
    average_travel_time = pd.to_timedelta(average_travel_time_seconds, unit='s') #Convert average_travel_time_seconds to hrs/minutes/seconds format
    print('\nThe average travel time for this query is',average_travel_time,'(hh:mm:ss).')

    # Display the Standard Deviation of the travel time
    std_travel_time_seconds = df['Trip Duration'].std() #standard deviation of the travel time column, in seconds
    std_travel_time = pd.to_timedelta(std_travel_time_seconds, unit='s') #Convert average_travel_time_seconds to hrs/minutes/seconds format
    print('\nThe standard deviation of the travel time for this query is',std_travel_time,'(hh:mm:ss).')

    df['Travel Time'] = pd.to_timedelta(df['Trip Duration'], unit='s')
    df.sort_values(by='Travel Time', ascending=False, inplace=True)
    print('\nHere is the top ten longest trips:\n\n',df['Travel Time'][:10])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)








def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts(dropna=False)
    print('\n The types of users for this search were:\n\n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts(dropna=False)
        print('\n The counts of gender for this search were:\n',gender)
    else:
        print('\nThere is no gender data for this search!\n')



    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        most_common_birth_year = df['Birth Year'].mode()
        earliest_birth_year = df['Birth Year'].min()
        oldest_person_age = int(2017 - earliest_birth_year)
        latest_birth_year = df['Birth Year'].max()
        youngest_person_age = int(2017 - latest_birth_year)
        print('\n The most common birth year for this search was:\n',most_common_birth_year)
        print('\n The earliest birth year for this search was:\n',earliest_birth_year)
        print('\nThat is approximately {} years old!'.format(oldest_person_age))
        print('\n The latest birth year for this search was:\n',latest_birth_year)
        print('\nThat is approximately {} years old!'.format(youngest_person_age))
    else:
        print('\nThere is no age data for this search!\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)




        time_stats(df)
        next_stat = input('\nThose were the time stats. Press enter to continue to station stats!\n')
        station_stats(df)
        next_stat = input('\nThose were the station stats? Press enter to continue to trip duration stats!\n')
        trip_duration_stats(df)
        next_stat = input('\nThose were the trip duration stats? Press enter to continue to user stats!.\n')
        user_stats(df)


        ### Code for user to view individual data begins here
        while True:
            see_data = input('\nWould you like to see individual trip data? Yes or No.\n') #Get input to look at trip data
            x = 0 #Initiate first row of data
            if see_data.lower() not in ('yes', 'no'): #Make sure answer is yes or no
                print('Please type yes or no')
                continue #If not yes or no, ask again
            elif see_data.lower() == 'no': #If no, break loop
                break
            else: #If yes, continue
                while True:
                    try:
                        step = int(input('\nHow many rows would you like to see at once?\n')) #Find out how many rows to show at one time, convert to int!
                        break
                    except ValueError:
                        print('That was not an integer!') #If a non-numeric is entered, ask again
                        continue


                while True:
                    sort = input("\nHow would you like to sort the values? 'Start Time', 'End Time', 'Trip Duration', 'Start Station', or 'End Station' \n") #Get input on how to sort values
                    if sort.lower() not in ('start time', 'end time', 'trip duration', 'start station', 'end station'):
                        print('\nPlease check your selection!\n')
                        continue
                    else:
                        print('\nYou have selected {}.\n'.format(sort.title()))
                        df.sort_values(by=sort.title(), ascending=False, inplace=True)  #Sort df by the entered value
                        break


                print(df[x:x+step]) #Print the first 'x' rows
                if step >= len(df):
                    print('\nThat was the last of the data.\n') #if the step is larger than rows of data, we're alread at the end
                else:
                    print('\nThat was the first {} rows.  There are {} rows remaining.\n'.format(step, len(df) - step))
                while (x + step) < len(df): #Make sure we are not past the length of the df
                    see_more = input('\nPress enter to see more data or type "EXIT" to leave.\n') #Check if user wants to see more rows
                    if see_more.lower() == 'exit': #If they want to leave, set x to a value longer than df so the outer loop is false
                        x = len(df) + 2 #Make X > len(df) to exit higher loop
                        break
                    else:
                        x += step #If they want to continue and are not at end, add the step value and continue to show data
                        print(df[x:x+step])
                        if x + step >= len(df): #Check if the end of the data is reached
                            print('\nThat was the last of the data.\n')
                        else:
                            print('That was rows {} thorugh {}.  There are {} rows remaining.'.format(x+1,x + step,len(df)-(x+step)))
                        continue
            break
            ### Code for user to view individual data ends here


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
