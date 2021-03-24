import time
import pandas as pd
import datetime as dt
#-----------------------------------------------------------------------------------------------
# lists & dict to filter by
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
filters = ['month', 'day', 'both', 'none']
filter_month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']
filter_day = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']

def get_input(input_message, data_avalible):
    """ used to handle invallid inputs """

    output = input(input_message).lower()
    while output not in data_avalible:
        print("invallid input! Please try again.")
        output = input(input_message).lower()

    return output
#-----------------------------------------------------------------------------------------------
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
# get user input for the city desired
    city = get_input("Between (Chicago, New York, Washington),which one would you like to view data for?\n",CITY_DATA)
# ask user how he would want to filter the data for the specified city, 'none' for no filtration
    filter_data = get_input("Great! now how do you want to filter the data: by (month, day, both, none)?\n", filters)
    
    month = 'none'
    day = 'none'
# ask the user to choose the month that he wants to filter by if he wanted to filter by month only
    if filter_data == "month":
        month = get_input("Now please choose a month: [Jan, Feb, Mar, Apr, May, Jun, All] - 'Type abbreviation as listed'\n", filter_month)
# ask the user to choose the day that he wants to filter by if he wanted to filter by day only
    elif filter_data == "day":
        day = get_input("Now please choose a day: [Mon, Tue, Wed, Thu, Fri, Sat, Sun, All] - 'Type abbreviation as listed'\n", filter_day)
# ask the user to choose the month and the day that he wants to filter by if he wanted to filter by both
    elif filter_data == "both":
        month = get_input("Now please choose a month: [Jan, Feb, Mar, Apr, May, Jun, All] - 'Type abbreviation as listed'\n", filter_month)
        day = get_input("And please choose a day: [Mon, Tue, Wed, Thu, Fri, Sat, Sun, All] - 'Type abbreviation as listed'\n", filter_day)
        
    print('-'*40)
    return city, month, day
#-----------------------------------------------------------------------------------------------

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.strftime("%a")
    # filter by month if applicable
    if month != 'none':
        if month != 'all':
        # get the corrisponding month number from dict key-value
            months = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6 }
            month = months[month]
        # filter by month to create the new dataframe
            df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'none':
        if day != 'all':
        # filter by day of week to create the new dataframe
            df = df[df['day of week'] == day.title()]

    return df
#-----------------------------------------------------------------------------------------------

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # corrisponding full month name and full day name dictionaries
    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June' }
    days = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'wednesday', 'Thu':'Thursday', 'Fri':'Friday', 'Sat':'Saturday', 'Sun':'Sunday'}
    # find the most common month
    common_month = df['month'].mode()[0]
    # find the most common day of week
    common_day_of_week = df['day of week'].mode()[0]
    # convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour 
    common_hour = df['hour'].mode()[0]
    while True:
        if (month != "none") and (day != "none"):
        # display most common hour if filtred by month and day
            print('most common start hour is: ', common_hour)
        elif month != "none":
        # display most common hour and day if filtred by month only
            print('most common day of week is: ', days[common_day_of_week])
            print('most common start hour is: ', common_hour)
        elif day != "none":
        # display most common hour and month if filtred by day only
            print('most common month is: ', months[common_month])
            print('most common start hour is: ', common_hour)
        else:
        # display most common hour, month and day if no filter is applied
            print('most common month is: ', months[common_month])
            print('most common day of week is: ', days[common_day_of_week])
            print('most common start hour is: ', common_hour)
        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-----------------------------------------------------------------------------------------------

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('most common start station is: ', common_start_station)
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('most common end station is: ', common_end_station)
    # display most frequent combination of start station and end station trip
    df['start-end combination'] = df['Start Station'] + " - " + df['End Station']
    common_start_end = df['start-end combination'].mode()[0]
    print('most frequent start station-end station trip is: ', common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-----------------------------------------------------------------------------------------------

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time 
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = dt.timedelta(seconds = int(total_travel_time))
    print('Total travel time is: ', total_travel_time)
    # display mean travel time
    mean_tarvel_time = df['Trip Duration'].mean()
    mean_tarvel_time = dt.timedelta(seconds = int(mean_tarvel_time))
    print('Mean of travel time is: ', mean_tarvel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-----------------------------------------------------------------------------------------------

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of user count:')
    print(user_types)
    # display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('Gender count:')
        print(gender)
    else:
        print('Gender count:\nno gender data available.')
    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_b_y = df['Birth Year'].min()
        print('Earliest year of birth:')
        print(int(earliest_b_y))
        recent_b_y = df['Birth Year'].max()
        print('Most recent year of birth:')
        print(int(recent_b_y))
        most_common_b_y = df['Birth Year'].mode()[0]
        print('Most common year of birth:')
        print(int(most_common_b_y))
    else:
        print('Earliest year of birth:\nno data available.')
        print('Most recent year of birth:\nno data available.')
        print('Most common year of birth:\nno data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#-----------------------------------------------------------------------------------------------
def display_data(df):
    """
    Loads first 5 rows of the data and ask user 
    if he wants to display 5 more if required.
    """
    display_rows = 5
    data_to_display = input('Whould you like to view 5 rows of individual trip data? (Enter yes or no).\n').lower()
    while True:
        if data_to_display != 'no':
            data_frame = df.iloc[0:display_rows]
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            print(data_frame)
            display_rows += 5
            data_to_display = input('Whould you like to view 5 more rows of the data?: (yes or no)\n').lower()
        else:
            break
#-----------------------------------------------------------------------------------------------

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
