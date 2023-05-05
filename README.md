## Research Interest Dashboard

### Purpose
Imagine that you're looking to pursue a Ph.D in computer science,
but you're not sure which field you want to enter. This dashboard
may be able to help. Firstly, given a research interest, or "keyword", the
dashboard returns a chart showing interest levels in the domain,
the top universities for the domain, and the top faculty for the domain.
This is useful for those that have a sort of idea of what topic they would
like to do research in, but aren't sure where. For those who aren't sure what
they want, there exists a chart at the bottom which show the most popular
keywords in a given year.

### Demo

### Installation
Requires Python 3.10, 'pip install -r requirements.txt', and an internet connection.

### Usage
To change a keyword, there is a dropdown at the top left of the first section. To
change year, there is a dropdown at the top left of the bottom section. The middle
section gives you the option to modify a university's name and a faculty's name.
### Design
The application consists of 5 files: main.py, get_coordinates.py, mysql_utils.py,
mongodb_utils.py, neo4j_utils.py. The design pattern was to have main.py do the
frontend work and make calls to the *_utils.py files in order to update or query
databases. get_coordinates.py is called in neo4j_utils.py in order to get
the coordinates of universities to use in the map.
### Implementation
For everything frontend, I used dash and plotly in Python. To speed up specific queries,
there are databases used from Neo4j, MongoDB, and MySQL. These databases are accessed with
the neo4j, pymongo, sqlalchemy, and mysql-connector libraries in python. In order to place
the universities on a map, I used googlesearch-python to search the coordinates in Google
and beautifulsoup4 to parse the results. Since web scraping can be slow, the university ->
coordinates results are stored in the file cache.pickle and the application will only web
scrape if the coordinates are not in the cache. 
### Database Techniques
After running techniques/techniques.sql, the MySQL database gets an index on
keyword.name as well as constraints on faculty.name and university.name. In
addition, mysql_utils.py utilizes prepared statements in the method find_faculty_member.
### Extra-Credit Capabilities
I used external data sourcing in order to find the coordinates of each university,
specifically web scraping Google, and used a cache for these results.
### Contributions
I built this by myself.