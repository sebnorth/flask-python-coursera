from models import Project
from dane import pobierz_dane

titleList = pobierz_dane('tytuly.csv')
db.create_all()
for title in titleList:
	db.session.add(Project(title = title))
db.session.commit()
