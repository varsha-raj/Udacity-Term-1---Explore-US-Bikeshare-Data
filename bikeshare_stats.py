'''
This python file is created to explore bikeshare data for cities that are in csv format and have 
a specific column name format. See filenames chicago, washington or new york as an example.
The code is created to take in raw inputs such as city, time period (month, day or both) to output
summary statistics.
'''
# Modules required
import numpy as np
import pandas as pd
import datetime as dt
import time
import calendar
import seaborn as sns
import matplotlib.pyplot as plt

'''
Define function get city to take the user input and add extension csv.
This function is later used to read data of the city in csv format. 
'''
def get_city():
	city = input('\nHello! Let\'s explore some US bikeshare data!\n'
								 'Would you like to see data for Chicago, New York, or Washington?\n')
	print('Alright! Let\'s go biking in {}!'.format(city))
	if city.lower()=='New York'.lower():
		return city.lower().replace(' ','_') +'_city'+'.csv'
	else:
		return city.lower() + '.csv'

'''
Define function get_time_period to take user's choice of time period filter.
If statement confirms if the user is happy with the filteration choice
'''
def get_time_period():
	time_period = input('\nWould you like to filter the data by "month", "day" or "both".'
												' Type "none" if you cannot make up your mind. '
												'The program will filter by popular month.\n')
	print("You have selected {}. Please make sure there are no errors".format(time_period))
	judgement_call = input('\nAre you happy with this selection. Type \'yes\' or \'no\'.\n')
	if judgement_call.lower() == "yes":
		print("Great! Let\'s continue biking!")
	elif judgement_call.lower() == "no":
		time_period = input('\nWould you like to filter the data by "month", "day", or "both"'
												'Type "none" if you cannot make up your mind.'
												'The program will filter by popular month.\n')
		print("You have selected {}".format(time_period))
	else:
		print("Please type as shown either 'yes' or 'no'. Thank you!")
	return time_period.lower()

'''
Define function to get month.
Month name should be given in "full month names"
'''
def get_month():
	month = input('\nWhich month? January, February, March, April, May, or June?\n')
	return month.lower()

'''
Define function to get day.
Month name should be given in "full day names"
'''
def get_day():
	day = input('\nWhich day? Please type your response as Monday, Tuesday....Sunday.\n')
	return day.lower()

#Outputs start time month with maximum frequency of occurences
def popular_month(city_file):
	popular_mon=city_file.groupby(['Start Time Month']).size().idxmax()
	return popular_mon

#Outputs start time day with maximum frequency of occurences for a given month
def popular_day(city_file):
	popular_day=city_file.groupby(['Start Time Day']).size().idxmax()
	return popular_day

#Outputs start time hour with maximum frequency of occurences for a given day
def popular_hour(city_file):
	popular_hour=city_file.groupby(['Start Time Hour']).size().idxmax()
	return popular_hour

#Outputs summary statistics for trip duration for a given month, day or both
def trip_duration(city_file):
	trip_duration_sum = round(city_file['Trip Duration'].dropna().sum(),1)
	trip_duration_mean = round(city_file['Trip Duration'].dropna().mean(),1)
	return trip_duration_sum, trip_duration_mean

#Outputs popular start and end stations for a given month, day or both
def popular_stations(city_file):
	popular_start_station = city_file.groupby(['Start Station']).size().idxmax()
	popular_end_station = city_file.groupby(['End Station']).size().idxmax()
	return popular_start_station, popular_end_station

#Outputs popular trip for a given month, day or both
def popular_trip(city_file):
	popular_start_end_station = city_file.groupby(['Start Station','End Station']).size().idxmax()
	return popular_start_end_station
	
#Outputs summary statistics for user type for a given month, day or both
def users(city_file):
	popular_usertype=city_file.groupby(['User Type']).size()
	return(popular_usertype)

#Outputs summary statistics for gender type for a given month, day or both
def gender(city_file):
	popular_gender=city_file.groupby(['Gender']).size()
	return(popular_gender)

#Outputs birth years for oldset and youngest person using bikeshare for a given month, day or both
def birth_years(city_file):
	popular_birth_years = tuple(city_file.dropna().sort_values('Birth Year', ascending=True).loc[:,'Birth Year'].iloc[[0,-1]])
	return popular_birth_years

#Function that takes in input statement to display entire dataset in chunks of 5
def display_data():
	display = input('\nWould you like to view individual trip data?'
										'Type \'yes\' or \'no\'.\n')
	return display.lower()
		

'''
This is the main function that takes in all the above sub-functions to print out statistics
based on the time period chosen by the user.
This function also creates additional columns for the dataset that are used based on time period chosen 
by the user.
Note that if none is chosen, the program picks most popular month as a time filter and provides stats
However, if both is picked, User chooses both month and day and stats are given for the day within the month user picks. 
If month is chosen by the user, then program throws all stats for popular day within month and other stats for that month.
Similarly, if day is chosen by user, then program throws popular hour and other stats for that day.
Additionally, this function also uses the entire city dataset to create a month-day heat map
Credit:Following webapages were used as an assistance to create the heatmap:
https://www.quantinsti.com/blog/creating-heatmap-using-python-seaborn/
https://stackoverflow.com/questions/12286607/python-making-heatmap-from-dataframe
'''
def statistics():
	city = get_city()
	try:
		city_file = pd.read_csv(city)
		city_file.iloc[:, 1:3] = city_file.iloc[:,1:3].apply(pd.to_datetime, errors='coerce')
		city_file['Start Time Month']=city_file['Start Time'].dt.month
		city_file['Start Time Month'] = city_file['Start Time Month'].apply(lambda x: calendar.month_name[x])
		city_file['Start Time Day']=city_file['Start Time'].dt.weekday_name#.str.lower()
		city_file['Start Time Hour']=city_file['Start Time'].dt.hour
		plot_file = city_file.groupby(['Start Time Month','Start Time Day']).size().reset_index(name='Total')
		plot_file = plot_file.pivot(index='Start Time Day', columns='Start Time Month', values= 'Total').rename_axis(None)
		plot_file=plot_file[['January', 'February','March','April','May','June']].reindex(['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday'])
		fig, ax = plt.subplots(figsize=(12,7))
		title = "Month-Day Heat Map using Start Time Month for year 2017"
		plt.title(title)
		ttl=ax.title
		ttl.set_position([0.5,1.05])
		sns.set(font_scale=2)
		sns.heatmap(plot_file, annot= False, cmap='RdYlGn_r', fmt="",ax=ax)
	except FileNotFoundError:
		print("WAIT...This file does not exist. Let us restart! Please retype the correct city to avoid further errors!")
		statistics()


	time_period = get_time_period()
	if time_period not in ('month', 'day', 'none','both'):
		print("An error was found. Please check your input.")
		time_period = get_time_period()

	if time_period not in ('month', 'day', 'none','both'):
		print("You are making repeated errors. Terminating program")
		raise SystemExit

	if time_period == 'none':
		start_time = time.time()
		city_file=city_file[city_file['Start Time Month'].str.lower()==popular_month(city_file).lower()]
		print('Calculating the first statistic...')
		print('POPULAR START TIME MONTH: {}'.format(popular_month(city_file)))
		print('That took %s seconds.' % (time.time() - start_time))
		print('Calculating the next statistic...')


	if time_period == 'month':
		while True:
			try:
				month_val= get_month()
				start_time=time.time()
				if month_val in ('january', 'february', 'march', 'april','may','june'):
					city_file=city_file[city_file['Start Time Month'].str.lower()==month_val]
					print('Calculating the first statistic...')
					print('POPULAR START TIME DAY: {}'.format(popular_day(city_file)))
					print('That took %s seconds.' % (time.time() - start_time))
					print('Calculating the next statistic...')
					break
				else:
					raise(Exception)
			except Exception as error:
				print("Wrong input. Please try again! You'll probably need a cup of coffee this time!")
					
	if time_period == 'day':
		while True:
			try:	
				day_val=get_day()
				start_time=time.time()
				if day_val in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
					city_file=city_file[city_file['Start Time Day'].str.lower()==day_val]
					print('Calculating the first statistic...')
					print('POPULAR START TIME HOUR: {}'.format(popular_hour(city_file)))
					print('That took %s seconds.' % (time.time() - start_time))
					print('Calculating the next statistic...')
					break
				else:
					raise(Exception)
			except Exception as error:
				print("Wrong input. Please try again! You'll probably need a cup of coffee this time!")
	
	if time_period == 'both':
		while True:
			try:
				month_val = get_month()	
				day_val=get_day()
				start_time=time.time()
				if month_val in ('january', 'february', 'march', 'april','may','june') and day_val in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'):
					city_file=city_file[city_file['Start Time Day'].str.lower()==day_val]
					print('Calculating the first statistic...')
					print('POPULAR START TIME HOUR: {}'.format(popular_hour(city_file)))
					print('That took %s seconds.' % (time.time() - start_time))
					print('Calculating the next statistic...')
					break
				else:
					raise(Exception)
			except Exception as error:
				print("Wrong input. Please try again! You'll probably need a cup of coffee this time!")


		
	start_time=time.time()
	print('TOTAL TRIP DURATION (sec): %.1f ; AVG TRIP DURATION (sec): %.1f' %trip_duration(city_file))
	print('That took %s seconds.' % (time.time() - start_time))
	print('Calculating the next statistic...')

	start_time=time.time()
	print('START STATION: %s ; END STATION: %s' %popular_stations(city_file))
	print("That took %s seconds." % (time.time() - start_time))
	print("Calculating the next statistic...")

	start_time=time.time()
	print('POPULAR TRIP: ')
	print(popular_trip(city_file))
	print("That took %s seconds." % (time.time() - start_time))
	print("Calculating the next statistic...")

	start_time=time.time()
	print('USER TYPE INFORMATION:')
	print(users(city_file))
	print("That took %s seconds." % (time.time() - start_time))
	print("Calculating the next statistic...")

	start_time=time.time()
	try:
		print('GENDER INFORMATION:')
		print(gender(city_file))

	except KeyError:
		print('No gender information available')
		print("That took %s seconds." % (time.time() - start_time))
		print("Calculating the next statistic...")

	start_time=time.time()
	try:
		print('EARLIEST BIRTH YEAR: %d ; RECENT BIRTH YEAR: %d' %birth_years(city_file))
		if birth_years(city_file)[0] <= 1928:
			print("Birth Year {0:.0f} is above 90 years of age. I guess age is just a number. Ride like a Champ!".format(birth_years(city_file)[0]))
			if birth_years(city_file)[1] >= 2002:
				print("Birth Year {0:.0f} is too young to ride.".format(birth_years(city_file)[1]))
	except KeyError:
		print('No birth year information available')
		print("That took %s seconds." % (time.time() - start_time))
		

	N=0
	city_file = pd.read_csv(city)
	while len(city_file) >= N:
		if display_data() =='yes':
			print('Displaying data for the city without applying any filter...Display is limited to 5 rows each time "yes" is hit.')
			N=N+5
			print(city_file.iloc[N-5:N])
		else:
			break

	plot_display = input('\nView heat map for most/least popular days for any given START TIME MONTH? Type \'yes\' or \'no\'.\n')
	if plot_display.lower() == 'yes':
		plt.show()


	restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
	if restart.lower() == 'yes':
		statistics()
	else:
		raise SystemExit

if __name__ == "__main__":
	statistics()









		


			









			 


		





		