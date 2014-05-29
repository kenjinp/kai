# /!\ THIS SCRIPT IS FOR DELETE DATABASE CONTENT /!\
from app import db, models

i = 0
users = models.User.query.all()
for u in users:
        i+=1
        print  '%r: '%i + u.nickname + '\n'

print '----------/!\-----------\n'
print 'The following will delete the database\n.'
y = raw_input('continue? > ')
if y == 'y':
        for u in users:
                db.session.delete(u)
                print 'deleting: ' + u.nickname
else:
        print'I don\'t understand you.'

db.session.commit()
