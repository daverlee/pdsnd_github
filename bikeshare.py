import time
import pandas as pd
#import numpy as np - was not used
# Add random line
# add another line

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("\nWhich city would you like to look at? (Chicago, New York City, Washington)\n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("We do not have that city, please enter one of the following: Chicago, New York City, or Washington")
            continue
        else:
            break

    # Get user input for month (all, january, february, ... , december)
    while True:
        month = input(
            "\nWhich month would you like to filter with? Please type in 'all' or enter a single month:\n").lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'):
            print("Please enter a single month or 'all'")
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "\nWhich day of the week would you like to filter with? Please type in 'all' or single day:\n").lower()
        if day not in ('all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
            print("Please enter 'all' or a single day of the week")
            continue
        else:
            break

    print('-' * 40)
    return city, month, day


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
    # Load the city data into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    df['Start Month'] = df['Start Time'].dt.month
    common_month = df['Start Month'].mode()[0]
    common_month_name = pd.to_datetime(f'2023-{common_month}-01').strftime('%B')
    print("The most common month is", common_month_name)

    # Display the most common day of week
    df['DoW'] = df['Start Time'].dt.dayofweek
    common_day = df['DoW'].mode()[0]
    common_day_name = pd.to_datetime(f'2023-01-{common_day + 1}').strftime('%A')
    print("The most common day of the week is", common_day_name)

    # Display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    common_hour = df['Start Hour'].mode()[0]
    print("\nThe most common start hour is", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    # use the mode function, as mode returns multiple values access the first using the [0]
    station_mode = df['Start Station'].mode()[0]
    print("The most common starting station is ", station_mode)

    # TO DO: display most commonly used end station

    # use the mode function, as mode returns multiple values access the first using the [0]
    end_station_mode = df['End Station'].mode()[0]
    print("The most common ending station is ", end_station_mode)

    # TO DO: display most frequent combination of start station and end station trip

    # First group the stations using the .groupby function
    # then use the size() to count the # of occurances for the combinations
    # then  convert the results back into the Dataframe - naming the column 'station count'
    e2e_stations = df.groupby(['Start Station', 'End Station']).size().reset_index(name='station count')
    e2e_most_common = e2e_stations.nlargest(1, 'station count')
    # now bring together
    most_common_trip = e2e_most_common.iloc[0]
    print("The most frequent combination of start station and end station trip is from {} to {} with {} trips.".format(
        most_common_trip['Start Station'], most_common_trip['End Station'], most_common_trip['station count']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # do this by calculate the sum of times in the data set using the sum
    try:
        # Pull the trip duration
        total_trip_time = df['Trip Duration'].sum()
        print("\nThe total time spend on trips was ", total_trip_time)
    except KeyError:
        print("\nTotal trip time is not available")

    # TO DO: display mean travel time
    try:
        # Pull trip duration from the DataFrame & calculate the mean
        avg_trip_time = df['Trip Duration'].mean()
        print("\nThe average trip duration is  ", avg_trip_time)
    except KeyError:
        print("\nAverage time is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    # this is not available for Washington - so wrap with try & except
    # Use the .value_counts
    try:
        user_types = df['User Type'].value_counts()
        print('User Types:\n', user_types)
    except KeyError:
        print('User Types data is not available')

    # TO DO: Display counts of gender
    # this is not available for Washington
    # Use the .value_counts
    try:
        gender = df['Gender'].value_counts()
        print('Gender Counts are\n', gender)
    except KeyError:
        print('Gender data is not available')

    # TO DO: Display earliest, most recent, and most common year of birth
    # Washington  does not having DOB , look to use try & except

    # For earliest use the .min function
    # now just pull out the year
    # by applying
    try:
        df['Birth Year'] = df['Birth Year'].astype(float)
    except KeyError:
        print("\nBirth Year data is not available")

    # For earliest year of birth, use the .min function
    try:
        early_dob = df['Birth Year'].min()
        print('\nEarliest Year of birth:', int(early_dob))
    except KeyError:
        print("\nEarliest Year of birth not available")

    # For most recent year of birth, use the .max function
    try:
        late_dob = df['Birth Year'].max()
        print('Most recent Year of birth:', int(late_dob))
    except KeyError:
        print("\nMost recent Year of birth information is not available")

    # For most common year of birth, use the .mode function
    try:
        common_year = df['Birth Year'].mode()[0]
        print('Most Common Year of birth:', int(common_year))
    except KeyError:
        print("\nMost Common Year of birth is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()