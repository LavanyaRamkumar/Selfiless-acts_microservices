import os, json, time


from flask import Flask, request, Response
from pymongo import MongoClient, errors
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)
time.sleep(5) # hack for the mongoDb database to get running
users = MongoClient('mongo', 27017).demo.users


@app.route("/users/<int:userid>", methods=["PUT"])
def add_user(userid):
    """Create user
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
      - name: name
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Creation succeded
    """
    request_params = request.form
    if 'email' not in request_params or 'name' not in request_params:
        return Response('Email and name not present in parameters!', status=404, mimetype='application/json')
    try:
        users.insert_one({
            '_id': userid,
            'email': request_params['email'],
            'name': request_params['name']
        })
    except errors.DuplicateKeyError as e:
        return Response('Duplicate user id!', status=404, mimetype='application/json')

    return Response('', status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["POST"])
def update_user(userid):
    """Update user information
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: false
      - name: name
        in: formData
        type: string
        required: false
    responses:
      200:
        description: Update succeded
    """
    request_params = request.form
    if 'email' not in request_params and 'name' not in request_params:
        return Response('Email or name must be present in parameters!', status=404, mimetype='application/json')
    set = {}
    if 'email' in request_params:
        set['email'] = request_params['email']
    if 'name' in request_params:
        set['name'] = request_params['name']
    users.update_one({'_id': userid}, {'$set': set})

    return Response('', status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["GET"])
def get_user(userid):
    """Example endpoint returning details about a user
    ---
    parameters:
      - name: userid
        in: path
        type: string
        required: true
    definitions:
      User:
        type: object
        properties:
          _id:
            type: int32
          email:
            type: string
          name:
            type: string
    responses:
      200:
        description: User model
        schema:
          $ref: '#/definitions/User'
      404:
        description: User not found
    """
    user = users.find_one({'_id': userid})
    if None == user:
        return Response("", status=404, mimetype='application/json')

    return Response(json.dumps(user), status=200, mimetype='application/json')


@app.route("/users/<int:userid>", methods=["DELETE"])
def delete_user(userid):
    """Delete operation for a user
    ---
    parameters:
      - name: palette
        in: path
        type: string
        required: true
    responses:
      200:
        description: User deleted
    """
    users.delete_one({'_id': userid})

    return Response('', status=200, mimetype='application/json')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)