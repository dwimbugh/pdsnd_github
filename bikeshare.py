import time
import pandas as pd

# Dict for the three city datasets
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) 
    while True:
            city = input('Would you like to see data from Chicago, New York City, or Washington? ').title()
            if city not in ('Chicago', 'New York City', 'Washington'):
                print('\n That\'s not a valid response!')
                continue
            else:
                print('"' + city + '"' + ' it will be!')
                break

    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('Please enter the month as January, Febuary, March, April, May or June for which you would like to see data or enter "all" to see data for all months.\n').title()
            if month not in ('January', 'Febuary', 'March', 'April', 'May', 'June', 'All'):
                print('\n That\'s not a valid response!')
                continue
            else:
                print('"' + month + '"' + ' it will be!')
                break
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Please enter the day of week (e.g Monday, Tuesday, etc.) for which you would like to see data or enter "all" to see data for all days.\n').capitalize()
            if day not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','All'):
                print('\n That\'s not a valid response!')
                continue
            else:
                print('"' + day + '"' + ' it will be!')
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.  Also add
    hour column to final dataframe.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name(locale='English')
    df['Day_of_Week'] = df['Start Time'].dt.day_name(locale='English')
    
    # extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour
        
    # filter by month if applicable
    if month != 'All':  
        
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        
        # filter by day of week to create the new dataframe
        df = df[df['Day_of_Week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if month != 'All':
        print('NOTE: The stat of "Most Common Month" is not shown due to your month filtering selection of:', month)
    
    else:
        # display the most common month
        popular_month =  df['Month'].mode()[0]
        print('Most Popular Month:', popular_month) 
        
    if day != 'All':
        print('NOTE: The stat of "Most Common Day" is not shown due to your day filtering selection of:', day)   

    else:
        # display the most common day of week
        popular_day =  df['Day_of_Week'].mode()[0]
        print('Most Popular Day of Week:', popular_day)

    # display the most common start hour (from 0 to 23)
    popular_hour =  df['Hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station =  df['Start Station'].mode()[0]
    print('Most Popular Start Station:', start_station)

    # display most commonly used end station
    end_station =  df['End Station'].mode()[0]
    print('Most Popular End Station:', end_station)

    # display most frequent combination of start station and end station trip
    df['Combo_Station'] = df['Start Station'] + ' / ' + df['End Station']
    freq_combo = df['Combo_Station'].mode()[0]
    print('Most Frequent Combination of Start and End Stations:', freq_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = df['Trip Duration'].sum()
    print(travel_time, "seconds is the total travel time.")

    # display mean travel time
    avg_time = int(df['Trip Duration'].mean())
    print(avg_time, "seconds is the average travel time.")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types, '\n')

    # Display counts of gender (NYC and Chicago only)
    if city == 'New York City' or city == 'Chicago':
        sex = df['Gender'].value_counts()
        print(sex, '\n')

    # Display earliest, most recent, and most common year of birth (NYC and Chicago only)
        dob = df['Birth Year'].dropna().astype({'Birth Year': 'int32'}) 
    
        oldest_dob = dob.min()
        print(oldest_dob, ' is the earliest birth year.\n')
        
        youngest_dob = dob.max()
        print(youngest_dob, ' is the most recent birth year.\n')
        
        common_dob = dob.mode()[0]
        print(common_dob, ' is the most common birth year.')
        
    else: 
        print('IMPORTANT: There is no gender or date of birth data for the selected data set!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def view_data(df):
    """Displays raw data from dataframe 5 rows at a time."""
    
    raw_data = input('\nWould you like to see first 5 rows of data? Please enter yes or no:\n').title()
   
    if raw_data == ('Yes'):
        row = 0 #starting row of raw data

        while True:
            print(df.iloc[row:row + 5])
            row += 5
            more_data = input('\nWould you like to see next 5 rows of data? Please enter yes or no:\n').title()

            if more_data != ('Yes'):
                print('You typed something other than "yes" - now existing the raw data view!\n')
                break

    else:
        print('You typed something other than "yes" - now existing the raw data view!  Thanks for your time.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nYou typed something other than "yes" - now existing the program! Thanks for your time.\n')
            break


if __name__ == "__main__":
	main()