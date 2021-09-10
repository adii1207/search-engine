from flask import Flask,request
from flask.views import View
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello' : 'world'}

class MyView(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
        if request.method == 'POST':
            print("posted")
app.add_url_rule('/myview', view_func=MyView.as_view('myview'))

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)