from settings import *
import json

# Initializing our database
db = SQLAlchemy(app)


from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            # for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            for field in [x for x in dir(obj) if x=='id' or  x == 'name']:
                data = obj.__getattribute__(field)
                try:
                    # json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    quota = db.Column(db.Integer, nullable=False)
    machines = db.relationship('Machine' ,backref=db.backref('team', lazy=True))
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    # def __repr__(self):
    #     return '<Team %r>' % self.id

    def json(self):
        t =  {'id': self.id, 'quota': self.quota}
        y = json.dumps(self.machines, cls=AlchemyEncoder)
        t['machines'] = y
        return t
        # 'machines': Machine.json(self.machines)
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
        return [Team.json(team) for team in Team.query.all()] 
    @staticmethod
    def get_team(_id):
        '''function to get team using the id of the movie as parameter'''
        return [Team.json(Team.query.filter_by(id=_id).first())]

    @staticmethod
    def update_team(_id, _quota):
        '''function to update the details of a team using the id, title,
        year and genre as parameters'''
        team_to_update = Team.query.filter_by(id=_id).first()
        team_to_update.quota = _quota
        db.session.commit()
    @staticmethod
    def delete_team(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Team.query.filter_by(id=_id).delete()
        db.session.commit()

    @staticmethod
    def append_machine_to_team_by_id(_id,_machine_id):
        '''function to add team to database using _quota
        as parameters'''
        m = Machine.query.filter_by(id=_machine_id).first()
        team_to_update = Team.query.filter_by(id=_id).first()
        if team_to_update is not None:
            if len(team_to_update.machines) < team_to_update.quota:
                team_to_update.machines.append(m)
                db.session.commit()
                return True
        return False 


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
        return {'id': self.id, 'name': self.name,'team_id': self.team_id}

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
    def update_machine(_id, _name):
        '''function to update the details of a machine using the id, name as parameters'''
        machine_to_update = Machine.query.filter_by(id=_id).first()
        machine_to_update.name = _name
        db.session.commit()

    @staticmethod
    def delete_machine(_id):
        '''function to delete a machine from our database using
           the id of the machine as a parameter'''
        Machine.query.filter_by(id=_id).delete()
        db.session.commit() 
