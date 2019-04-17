#!/bin/bash
python manage.py database migrate
python manage.py database upgrade
python manage.py scraper --sitemap https://www.theguardian.com/sitemaps/news.xml
python manage.py runserver -h 0.0.0.0 -p 5000
