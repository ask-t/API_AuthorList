from flask import Flask,jsonify,abort,request
from flask_restful import Resource, Api
from flask_restful import abort as restful_abort
from werkzeug.exceptions import HTTPException
import db

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'Not found',
                        'message': 'Invalid resource URI'})
    response.status_code = 404
    return response

@app.errorhandler(Exception)
def handle_all_errors(error):
    status_code = 500
    if isinstance(error, HTTPException):
        status_code = error.code
    return jsonify({'message': 'The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.', 'error_code': status_code}), status_code


@app.errorhandler(501)
def not_implemented(e):
    response = jsonify({'status': 501, 'error': 'Not Implemented',
                        'message': 'The requested URI is recognized, but not implemented'})
    response.status_code = 501
    return response

@app.errorhandler(503)
def service_unavailable(e):
    response = jsonify({'status': 503, 'error': 'Service Unavailable',
                        'message': 'The server is currently unavailable (overloaded or down)'})
    response.status_code = 503
    return response

@app.errorhandler(400)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'Bad Request',
                        'message': 'Bad Request'})
    response.status_code = 400
    return response

@app.errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'status': 405, 'error': 'Method not allowed',
                        'message': 'Method not allowed'})
    response.status_code = 405
    return response




class showData(Resource):
    def get(self):
        try:
            d = db.Database()
            rows = d.get_author_data()
            array = []
            for row in rows:
                id = row[0]
                author = row[1]
                birthday = row[2].strftime('%Y-%m-%d')
                body = {
                    "id": id,
                    "author": author,
                    "birthday": birthday
                }
                array.append(body)
            return array
        except Exception as e:
            return handle_all_errors(e)

    def post(self):
        try:
            d = db.Database()
            data = request.get_json()
            author = data.get("author")
            birthday = data.get("birthday")
            if not author or not birthday:
                return jsonify({'message': 'Author or birthday is missing'}), 400
            d.insert_data(author,birthday)
            return data,201
        except Exception as e:
            return handle_all_errors(e)


api.add_resource(showData,"/api/get")

if __name__ == "__main__":
    app.run(debug=True)