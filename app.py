from flask import Flask, request, Response, jsonify
from dal import *

# creating an instance of the flask app
app = Flask(__name__)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.create_all()

# route to get all teams
@app.route('/teams', methods=['GET'])
def get_teams():
    '''Function to get all the teams in the database'''
    return jsonify({'Teams': Team.get_all_teams()})


# route to get team by id
@app.route('/teams/<int:xid>', methods=['GET'])
def get_team_by_id(xid):
    return_value = Team.get_team(xid)
    return jsonify(return_value)


# route to add new team
@app.route('/teams', methods=['POST'])
def add_team():
    '''Function to add new team to our database'''
    request_data = request.get_json()  # getting data from client
    Team.add_team(request_data["quota"])
    response = Response("Team added", 201, mimetype='application/json')
    return response


# route to update team with PUT method
@app.route('/teams/<int:xid>', methods=['PUT'])
def update_team(xid):
    '''Function to edit team in our database using team id'''
    request_data = request.get_json()
    append = request_data['machine_id']
    if append is None:
        Team.update_team(xid, request_data['quota'])
        response = Response("Team Updated", status=200, mimetype='application/json')
    else:
        # append machine to team Only.
        res = Team.append_machine_to_team_by_id(xid,request_data['machine_id'])
        if res == True:
            response = Response("Machine Successfuly appended to the Team", status=200, mimetype='application/json')
        else:
            response = Response("Failed to appended to the Team", status=200, mimetype='application/json')

    return response


# route to delete team using the DELETE method
@app.route('/teams/<int:xid>', methods=['DELETE'])
def remove_team(xid):
    '''Function to delete team from our database'''
    Team.delete_team(xid)
    response = Response("Team Deleted", status=200, mimetype='application/json')
    return response


#----------------------------------------------------
#----------------------------------------------------

# route to get all machines
@app.route('/machines', methods=['GET'])
def get_machines(


):
    '''Function to get all the machines in the database'''
    return jsonify({'Machines': Machine.get_all_machines()})


# route to get team by id
@app.route('/machines/<int:xid>', methods=['GET'])
def get_machine_by_id(xid):
    return_value = Machine.get_machine(xid)
    return jsonify(return_value)


# route to add new machine
@app.route('/machines', methods=['POST'])
def add_machine():
    '''Function to add new team to our database'''
    request_data = request.get_json()  # getting data from client
    Machine.add_machine(request_data["name"])
    response = Response("Machine added", 201, mimetype='application/json')
    return response


# route to update machine with PUT method
@app.route('/machines/<int:xid>', methods=['PUT'])
def update_machine(xid):
    '''Function to edit machine in our database using team id'''
    request_data = request.get_json()
    Machine.update_machine(xid, request_data['name'])
    response = Response("Machine Updated", status=200, mimetype='application/json')
    return response


# route to delete machine using the DELETE method
@app.route('/machines/<int:xid>', methods=['DELETE'])
def remove_machine(xid):
    '''Function to delete machine from our database'''
    Machine.delete_machine(xid)
    response = Response("Machine Deleted", status=200, mimetype='application/json')
    return response


if __name__ == "__main__":
    app.run(debug=True)
