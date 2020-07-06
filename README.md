# news-flask
Python Flask web scraping news sites

This flask application exposes some services for my Quarkus NewsStand application.

This flask application is written in Python and performs web-scraping of some news web sites.
Currently working on Haaretz web site as a first POC.

All services are stateless.

In addition, this code base contains some Python utility scripts that are not directly connected.

### The exposed endpoints:

[Hello](http://localhost:5000/hello) - just to manually test that server is up

[start-page](http://localhost:5000/flask/start-page) - Process start page. (currently hard-coded starting from "www.haaretz.co.il")
Returns a list of relative URLs (as JSON)


[scrape-single-page](/flask/scrape-single-page/<string:url>) - Process a single page of one article.
Returns a JSON representation of ArticleDetails.

(ArticleDetails contains just the meta-data of the article, not the full content).


