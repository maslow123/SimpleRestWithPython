from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv') # read CSV
        data = data.to_dict() # convert dataframe to dictionary
        return {'data': data, 'status': 'OK'}, 200

    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('userId', required=True)  # add arguments
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        args = parser.parse_args()  # parse arguments to dictionary

        # handling user already registered
        data = pd.read_csv('users.csv')
        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists"
            }, 401
        # create new dataframe containing new values
        new_data = pd.DataFrame({
            'userId': args['userId'],
            'name': args['name'],
            'city': args['city'],
            'locations': [[]]
        })
        # read our CSV
        data = pd.read_csv('users.csv')
        # add the newly provided values
        data = data.append(new_data, ignore_index=True)
        # save back to CSV
        data.to_csv('users.csv', index=False)

        return {
            'data': data.to_dict()
        }, 200

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            #select our user
            user_data = data[data['userId'] == args['userId']]
            print(f"User Data: {args}")
            # update user's locations
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return \
                {
                    'data': data.to_dict()
                }, 200
        else:
            #otherwise the useId doent't exits
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        args = parser.parse_args()

        # read our CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            # remove data entry matching given userId
            data = data[data['userId'] != args['userId']]

            # save back to CSV
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404
class Locations(Resource):
    pass
api.add_resource(Users, '/users') # is our entry point
api.add_resource(Locations, '/locations') # is our entry point

if __name__ == '__main__':
    app.run() # run our Flask app
