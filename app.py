from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from elasticsearch import Elasticsearch, exceptions
import confg
import re
from helpers.format_date import format_date

app = Flask(__name__)
api = Api(app)
client = Elasticsearch(confg.ELASTIC_URL)

news_put_args = reqparse.RequestParser()
news_put_args.add_argument("date", type=str, help="pls specify a date for the news", required=True)
news_put_args.add_argument("short_description", type=str, help="a description is required", required=True)
news_put_args.add_argument("link", type=str, help="a link is required", required=True)
news_put_args.add_argument("category", type=str, help="you should specify the category", required=True)
news_put_args.add_argument("headline", type=str, help="write the headline", required=True)
news_put_args.add_argument("authors", type=str, help="who write this new ?", required=True)


@app.route("/")
def index():
    return render_template("index.html")


class News(Resource):

    @staticmethod
    def get(news_id):
        if client.indices.exists(index=confg.index_name):
            print(f"the index {confg.index_name} is found = OK..")
            print(f"Searching for the document {news_id} ...")
            try:
                result = client.get(index=confg.index_name, id=news_id)
                return result["_source"], 200
            except Exception as e:
                if isinstance(e, exceptions.NotFoundError):
                    print("the document not found check your new id")
                else:
                    print("an error occurred", e)
        else:
            raise exceptions.NotFoundError(f"the index {confg.index_name} is not found = ERROR..")

    def put(self, news_id):
        args = news_put_args.parse_args()
        result = self.get(news_id)
        if result is None:
            print("Indexing a new document")
            new_document = re.sub(r"[\s+]", "", confg.query) % (format_date(args["date"]), args["short_description"],
                                                                args["link"], args["category"], args["headline"],
                                                                args["authors"])
            try:
                idx_result = client.index(index=confg.index_name, id=str(news_id), body=new_document)
                return f"the document with the id {news_id} is {idx_result['result']}"
            except Exception as e:
                print("an Error occurred while indexing {}".format(e))
        else:
            return f"this document {news_id} already exists"

    def delete(self, news_id):
        result = self.get(news_id)
        if result is not None:
            print("Deleting the document {}".format(news_id))
            deleted_result = client.delete(index=confg.index_name, id=news_id)
            if deleted_result["result"] == "deleted":
                return f"the document {news_id} is deleted = OK.."
        else:
            raise exceptions.NotFoundError(f"the document {news_id} is not found ! = DOWN..")

    def patch(self, news_id):
        result = self.get(news_id)
        if result is not None:
            updated_fields = request.get_json()
            try:
                updated_result = client.update(index=confg.index_name, id=str(news_id), body={'doc': updated_fields})
                print("the document {} is {}".format(news_id, updated_result["result"]))
            except exceptions.RequestError as e:
                print("An error occurred while updating {}".format(e))
        else:
            raise exceptions.NotFoundError(f"the document {news_id} is not found ! = DOWN..")


api.add_resource(News, "/news/<string:news_id>")

if __name__ == '__main__':
    app.run(debug=True)
