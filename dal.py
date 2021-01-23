from settings import *
import json

# Initializing our database
db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    quota = db.Column(db.Integer, nullable=False)
    machines = db.relationship('Machine' ,backref=db.backref('team', lazy=True))

    # def __repr__(self):
    #     return '<Team %r>' % self.id

    def json(self):
        return {'id': self.id, 'quota': self.quota, 'machines': json.dumps(self.machines.__dict__)}
        # return {'id': self.id, 'quota': self.quota}


    @staticmethod
    def add_team(_quota):
        '''function to add team to database using _quota
        as parameters'''
        new_team = Team(quota=_quota)
        db.session.add(new_team)  
        db.session.commit() 
    @staticmethod
    def get_all_teams():
        '''function to get all teams in our database'''
        # q = Team.query.all()
        # for team in q:
        #     pass
        # return [Team.json(team) for team in Team.query.all()] 
        return [json.dumps(team) for team in Team.query.all()]
    @staticmethod
    def get_team(_id):
        '''function to get team using the id of the movie as parameter'''
        return [Team.json(Team.query.filter_by(id=_id).first())]

    @staticmethod
    def update_team(_id, _quota):
        '''function to update the details of a team using the id, title,
        year and genre as parameters'''
        movie_to_update = Team.query.filter_by(id=_id).first()
        movie_to_update.quota = _quota
        db.session.commit()
    @staticmethod
    def delete_team(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Team.query.filter_by(id=_id).delete()
        db.session.commit() 

class Machine(db.Model):
    __tablename__ = 'machine'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    team_id =db.Column(db.Integer, db.ForeignKey('team.id') , nullable=True)

    def __repr__(self):
        return '{}'.format(self.name)
        # return {'id': self.id, 'name': self.name}
    #     return '{"Machine: {}"}'.format(self.name)
    #     # return '<Machine %r>' % self.id

    def json(self):
        return {'id': self.id, 'name': self.name, 'team_id':self.team_id}

    @staticmethod
    def add_machine(_name):
        '''function to add machine to database using _name
        as parameters'''
        new_machine = Machine(name=_name)
        # new_machine = Machine(name=_name,team_id = _team_id)
        db.session.add(new_machine)  
        db.session.commit()    
    @staticmethod
    def get_all_machines():
        '''function to get all machines in our database'''
        return [Machine.json(machine) for machine in Machine.query.all()]
    @staticmethod
    def get_machine(_id):
        '''function to get movie using the id of the movie as parameter'''
        m = Machine.query.filter_by(id=_id).first()
        if m == None:
            return {}
        return [Machine.json(m)]
    @staticmethod
    def update_machine(_id, _name,_team_id):
        '''function to update the details of a machine using the id, name as parameters'''
        machine_to_update = Machine.query.filter_by(id=_id).first()
        machine_to_update.name = _name
        machine_to_update.team_id = _team_id
        db.session.commit()

    @staticmethod
    def delete_team(_id):
        '''function to delete a machine from our database using
           the id of the machine as a parameter'''
        Machine.query.filter_by(id=_id).delete()
        db.session.commit() 
