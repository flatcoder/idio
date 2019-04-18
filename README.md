# IDEAS for a WEB SCRAPER

A web scraper and sitemap crawler, wrapped up as a web service with an API.  Supports per-domain configurations for extracting and storing content.  Results are accessible via the database itself, an API that is provided or a simple front-end result browser (included to demonstrate API usage).

## Technology Stack

	Docker container.  Allows for development-testing-staging-production like environments.
	Python 3.7.  Reliable, strongly typed, time tested language.
	Python Flask.  Offers up a web server, restful API interface and templating for front-ends.
	Python SQL Alchemy. Offers a database agnostic solution for storing data.
	Beautiful Soup 4. The go-to scraper for Python.

## Installation

Checkout the repo, and then, choose one of the following options:

1. Docker compose.  Recommended.  As simple as running:

		docker-compose up --build

This will result in a number of events happening:

		a) initialise an empty database (stored locally, as "scraper.db")
		b) scrape The Guardian site map
		c) launch the web interface results browser on http://localhost:5202
		d) make the API available on http://localhost:5202/api

Data will persist if you kill or even destroy the container due to the mapping of the database to a local file.  Sub-sequent executions, will quickly migrate and only import new URLs found in the site map (unless you change the options for the site, see below).

2. Docker without compose (not recommended, but "docker run" with parameters matching the compose YML ought to work).

3. Python 3.7 Virtual environment:

		# install
		python3.7 -m venv venv
		source venv/bin/activate
		pip install -r requirements.txt

## Configuration

The scraper is configured against The Guardian by default.  This is fully extensible (and changeable).  You will see the rules in **config.py** that cover what classes are important, what tags to process, what URLs to ignore, how to categorize the URL (...).  This can be done on a "**per-domain**" basis, and configuration allows any number of entries.

## Usage (skip if using docker)

First time:

	# database...
	python manage.py database migrate
	python manage.py database upgrade

Updating:

	# run a scraper on a sitemap...
	python manage.py scraper --sitemap https://www.theguardian.com/sitemaps/news.xml

	# scrape a single URL...
	python manage.py scraper --url https://www.theguardian.com/politics/2018/aug/19/brexit-tory-mps-warn-of-entryism-threat-from-leave-eu-supporters

Every time:

	# the results browser and API...
	python manage.py runserver -h 0.0.0.0 -p 5202

For supported domains we extract the title, article content and images. The scraper handles redirects (e.g., 301) and also captures canonical URLs to help weed out duplicates at a later date (see "Future Improvements" below). Timeouts / Network errors are handled and reported but the emphasis is to "not stop" (i.e., skip to next URL / come back later). Results are stored (SQLite database but supports Postgres, MySQL or other). By default, URLs will not be re-crawled unless specifically instructed to do so in their domain configuration.

### Results Frontend Browser

	http://localhost:5202/

### Results Restful API

Endpoints:

	http://localhost:5202/urls

All endpoints support an optional "perpage" and "page" paramater.  E.g.:

	http://localhost:5202/urls?perpage=5
	http://localhost:5202/urls?perpage=5&page=1

## Future Improvements

Scraper:

    Authentication for sites that need it
    Session handling / Cookie peristence / Caching / Rate limiting
    Extract more meta data + Internal meta data on file types
    Look at other options than BS4 such as Scrapy

Crawler:

	Find and follow links of interest outside of the sitemap, within depth rules
	Improve duplicate handling
		- make a hash of the content
		- find canoncial url duplicates from link rel="..."
	Auto-run on schedule
		- record failures that need revisiting (network issues)
			- redis queue?

API and front end:

	API Auth
	Searching and filtering
	Notifications / Alerts (web sockets) from scrapers

Pipelines:

    Travis CI
    Python unittest
	Web server integration (currently using Flask Dev server)
		- Certainly for production!


Data model:

	Separate and elaborate around "categories", currently just a text column
	Site configurations in the database as opposed to the configuration file
		- avoid local version control conflicts
		- provide a user interface to rules
