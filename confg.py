index_name = "news_headline"
BASE_URL = "http://localhost:5000/"
ELASTIC_URL = "http://localhost:9200"
query = """\
{
    "date": "%s",
    "short_description": "%s",
    "link": "%s",
    "category": "%s",
    "headline": "%s",
    "authors": "%s"
}
"""
