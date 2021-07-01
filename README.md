# SQLAlchemy Homework - Surfs Up!
In pandas we were given a SQLite file to use for our climate data analysis. Utilizing create_engine we connected to said database, turned tables into classes, saved them as references and created an SQLAlchemy session

We were then tasked with analyzing the last twelve months of precipitation data. Loading the data into our dataframe, we established the query criteria and sorted by date. 
These were then plotted in pandas along with the standard summary statistics
We then siwtched to the station class to calculate total number of stations in the dataset, while also finding the most active station.
These results were then ordered by counts. The most active station was selected and then the lowest, highest and average temperature was retrieved from that station.
Similiarly to the precipitation data above we selected the last 12 months of temperature data and plotted those reults in a histogram. 

We then created a flask route, with 5 routes and a home page listing them
For precipitation we produced the results as a dictionary using date and prcp as the key and value pair
For stations, we returned a json list of stations from the dataset
Temperature observations (TOBS) shows a json list of TOBS for the previous year
Api/v1.0/<start> returns a json list of minimum temp, average temp, and max for given start or start end range.
