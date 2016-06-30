from . import db

class Project(db.Model):
    __tablename__ = 'myriceprojects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String, nullable=False)
    titleshort = db.Column(db.String(128), nullable=False)
    
    def __unicode__(self):
        return self.title

class Project2(db.Model):
    __tablename__ = 'myriceprojects2'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String, nullable=False)
    titleshort = db.Column(db.String(128), nullable=False)
    
    def __unicode__(self):
        return self.title

class Project3(db.Model):
    __tablename__ = 'myriceprojects3'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String, nullable=False)
    titleshort = db.Column(db.String(128), nullable=False)
    
    def __unicode__(self):
        return self.title
