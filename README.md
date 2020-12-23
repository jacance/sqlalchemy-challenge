# Hawaii Climate Analysis


This project analyzes the climate of Honolulu, Hawaii for trip planning.



## Climate Analysis and Exploration

Python and SQLAlchemy are used to do  climate analysis and data exploration of the climate database. All of the following analysis was completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

- Use the provided starter notebook and hawaii.sqlite files to complete climate analysis and data exploration.

- Choose a start date and end date for trip.

- Use SQLAlchemy create_engine to connect to sqlite database.

- Use SQLAlchemy automap_base() to reflect  tables into classes and save a reference to those classes called Station and Measurement.




### Precipitation Analysis


- Design a query to retrieve the last 12 months of precipitation data.

- Select only the date and prcp values.

- Load the query results into a Pandas DataFrame and set the index to the date column.

- Sort the DataFrame values by date.

- Plot the results using the DataFrame plot method.

- Use Pandas to print the summary statistics for the precipitation data.




### Station Analysis

- Design a query to calculate the total number of stations.

- Design a query to find the most active stations.

- List the stations and observation counts in descending order.

- Which station has the highest number of observations?

- Design a query to retrieve the last 12 months of temperature observation data (TOBS).

- Filter by the station with the highest number of observations.

- Plot the results as a histogram with bins=12.




## Climate App

- Design a Flask API based on the queries.

- Use Flask to create your routes.

- List all routes that are available.

- Convert the query results to a dictionary using date as the key and prcp as the value.

- Return the JSON representation of dictionary

- Return a JSON list of stations from the dataset.

- Query the dates and temperature observations of the most active station for the last year of data.

- Return a JSON list of temperature observations (TOBS) for the previous year.

- Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

- When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

- When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.



## Temperature Analysis

- Use given calc_temps function to calculate the min, avg, and max temperatures one year prior to trip date.

- Plot the min, avg, and max temperature from previous query as a bar chart.

- Use the average temperature as the bar height.

- Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).




## Daily Rainfall Average

- Calculate the rainfall per weather station using the previous year's matching dates.

- Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

- Create a list of dates for trip in the format %m-%d, then use the daily_normals function to calculate the normals for each date string and append the results to a list.

- Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

- Use Pandas to plot an area plot for the daily normals.
