import time
import pandas as pd

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
    # Gets user input for city (chicago, new york city, washington).
    city = input('\nPlease select one of the available cities: Chicago, New York City, or Washington:\n-> ')

    while True:
        if city.lower() in CITY_DATA:
            print("\nGreat! Thank You!")
            break
        else:
            print('\nOops! It looks like you did not enter the name of an available city.')
            city = input('\nPlease try again (Remember: it can only be Chicago, New York City, or Washington):\n-> ')


    # Gets user input for month (all, january, february, ... , june)

    print('\nYou can also select a month from January to June (both included) to filter your data')

    month = input('Or you can also just include the data for the whole period by typing "all":\n-> ')

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    while True:
        if month.lower() in months or month.lower() == 'all':
            print("\nFantastic!")
            break
        else:
            print('Oh! Something went wrong.')
            month = input('\nPlease try entering a month name or the text "all":\n-> ')

    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('\nLastly, you can select a day of the week (from Monday to Sunday).')
    day = input('Please enter a weekday, or type "all" for data on the entire week:\n-> ')

    while True:
        if day.lower() in days or day.lower() == 'all':
            print("\nAwesome!")
            break
        else:
            print('Oops! Something went wrong')
            day = input('\nPlease try entering a month name or the text "all":\n-> ')

    print('-'*40)

    return city.lower(), month.lower(), day.lower()


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

    # Converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extracts month, day and hour from the Start Time column to create an new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        df = df[df['day'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    mode_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    mode_month = months[mode_month - 1]
    print('\n* The most frequent month to travel is:', mode_month)

    # Displays the most common day of week
    mode_day = df['day'].mode()[0]
    print('\n* The most common day of the week to travel is:', mode_day)

    # Displays the most common start hour
    mode_hour = df['hour'].mode()[0]
    print('\n* The most frequent trip start hour:', mode_hour)

    print("\nThis took %s seconds to process." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    mode_start_st = df['Start Station'].mode()[0]
    print('\n* The most commonly used start station is:', mode_start_st)

    # Displays most commonly used end station
    mode_end_st = df['End Station'].mode()[0]
    print('\n* The most commonly used end station is:', mode_start_st)

    # Displays most frequent combination of start station and end station trip
    comb_start_end_st = df['Start Station'] + ' to ' + df['End Station']
    mode_start_end_st = comb_start_end_st.mode()[0]
    print('\n* The most frequent combination of start station and end station trip is:')
    print('  ', mode_start_end_st)

    print("\nThis took %s seconds to process." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    days, hours, minutes, remaining_seconds = convert_time(total_travel_time)
    print('\n* The total travel time is:')
    print('  {} days, {} hours, {} minutes and {} seconds'.format(days, hours, minutes, remaining_seconds))

    # Displays mean travel time
    mean_travel_time = df['Trip Duration'].mean().astype(int)
    days, hours, minutes, remaining_seconds = convert_time(mean_travel_time)
    print('\n* The mean travel time is:', mean_travel_time)
    print('  {} minutes and {} seconds'.format(minutes, remaining_seconds))

    print("\nThis took %s seconds to process." % (time.time() - start_time))
    print('-'*40)

def convert_time(seconds):
    """Converts seconds to days, hours, minutes, and seconds."""

    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60

    days = (seconds // seconds_in_day)
    hours = (seconds - (days * seconds_in_day)) // seconds_in_hour
    minutes = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    remaining_seconds = (seconds - (days * seconds_in_day) - (hours * seconds_in_hour)) % seconds_in_minute

    return days, hours, minutes, remaining_seconds

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types and distribution

    user_count = df['User Type'].value_counts()
    user_types = len(user_count.tolist())
    print('\n* There are {} types of users and their distribution is as follows: \n'.format(user_types))
    print(user_count)

    # Prints message if city = 'washington', otherwise:
    # Displays counts of gender distribution
    # Displays earliest, most recent, and most common year of birth

    try:
        gender_count = df['Gender'].value_counts()
        gender_types = len(gender_count.tolist())
        print('\n* There are {} types of gender and their distribution is as follows: \n'.format(gender_types))
        print(gender_count)

        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        birth_year_counts = int(df['Birth Year'].mode()[0])

        print('\n* The earliest year of birth is:', earliest_birth_year)
        print('\n* The most recent year of birth is:', most_recent_birth_year)
        print('\n* The most common year of birth is', birth_year_counts)

    except KeyError:
        print('\n***Unfortunately, the database for Washington does not contain gender or birth date information***')

    print("\nThis took %s seconds to process" % (time.time() - start_time))
    print('-'*40)


def main():
    print('\nHello! Let\'s explore some US bikeshare data!')

    city, month, day = get_filters()
    df = load_data(city, month, day)

    print('\nThe data has been filtered as follows:')
    print('\nCity: {} \nMonth: {} \nWeekday: {}'.format(city, month, day).upper())
    print('-'*40)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    print('\n---SCROLL UP TO SEE YOUR DATA---')

    raw_data = input('\nWould you like to see 5 rows of the raw data? Enter "yes" or "no":\n-> ')
    while True:
        if raw_data.lower() == 'yes':
            print('\nFirst 5 rows of raw data and {} columns:\n'.format(len(df.columns)))
            pd.set_option('max_columns', None)
            print(df.head(5))
            print('\n---SCROLL UP TO SEE YOUR DATA---')
            break
        elif raw_data.lower() == 'no':
            break
        else:
            raw_data = input('\nPlease enter "yes" or "no":\n-> ')

    restart = input('\nWould you like to restart? Enter "yes" or "no":\n-> ')
    while True:
        if restart.lower() == 'yes':
            return main()
        elif restart.lower() == 'no':
            break
        else:
            restart = input('\nPlease enter "yes" or "no":\n-> ')

if __name__ == "__main__":
	main()
