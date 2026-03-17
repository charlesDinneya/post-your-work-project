import time
from pathlib import Path

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def is_valid_input(i) -> bool:
    try:
        i = str(i)
        return not i.isnumeric()
    except ValueError as e:
        return False

def is_valid_city(city: str) -> bool:
    if city.lower() not in CITY_DATA.keys():
        return False
    else:
        return Path(CITY_DATA[city.lower()]).exists()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city: str
    month: str
    day: str

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Please enter city (Example chicago): "))
        if is_valid_input(city):
            city = city.lower()
            if not is_valid_city(city):
                print(f"City not found!!. Valid cities => {", ".join(CITY_DATA.keys())}")
            else:
                break
        else:
            print("Invalid Input. Enter a valid string")

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please enter month (Example january): ")
        month = month.lower()
        if is_valid_input(month):
            break
        else:
            print("Invalid Input. Enter a valid string")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please enter day of the week (Example monday): ")
        if is_valid_input(day):
            break
        else:
            print("Invalid Input. Enter a valid string")

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

    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df["day"] = df['Start Time'].dt.day_name().str.lower()
    if month != "all":
        df = df[df['month'] == month.lower()]

    if day != "all":
        df = df[df['day'] == day.lower()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"The most common month is {most_common_month}")

    # TO DO: display the most common day of week
    most_common_day = df['day'].mode()[0]
    print(f"The most common day is {most_common_day}")

    # TO DO: display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"The most common start hour is {most_common_start_hour} Uhr")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is {most_commonly_used_start_station}")

    # TO DO: display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is {most_commonly_used_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combination_for_stations = \
        df.groupby(["Start Station", "End Station"]).size().reset_index(name="count").sort_values(by="count", ascending=False)['count']
    print(f"The most frequent combination for start and end station is {most_frequent_combination_for_stations}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df["travel_time"] = df["End Time"] - df["Start Time"]

    # TO DO: display total travel time
    total_travel_time = df["travel_time"].sum()
    print(f"The total travel time is {total_travel_time}")

    # TO DO: display mean travel time
    mean_travel_time = df["travel_time"].mean()
    print(f"The mean travel time is {mean_travel_time}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(f"The count of user types is {user_type_count}")

    # TO DO: Display counts of gender
    gender_count = df['Gender'].value_counts()
    print(f"The count of genders is {gender_count}")

    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_birth_year = int(df["Birth Year"].min())
    most_recent_birth_year = int(df["Birth Year"].max())
    common_birth_year = df["Birth Year"].mode()[0]

    print(f"The earliest birth year is {earliest_birth_year}")
    print(f"The most recent birth year is {most_recent_birth_year}")
    print(f"The most common birth year is {common_birth_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df, n: int = 5):

    # User Prompt for raw data display
    n_df = df.head(n)
    current_index = 0
    while True:
        if current_index <= 4 and current_index <= len(n_df) - 1:
            raw_data_reply = input("Would you like to see raw data for this city?. (Enter 'yes' or 'no'): ")
            if is_valid_input(raw_data_reply):
                raw_data_reply = raw_data_reply.lower()
                if raw_data_reply == 'yes' or raw_data_reply == 'no':

                    if raw_data_reply == 'yes':
                        print(n_df.loc[current_index])
                        current_index = current_index + 1
                    else:
                        break
                else:
                    print("Invalid reply. Enter 'yes' or 'no'")
            else:
                print("Invalid reply. Enter 'yes' or 'no'")
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df) > 0:
            display_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print("\nYour selections returned an empty dataset.")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            break

# Entry point to the script
if __name__ == "__main__":
    main()
