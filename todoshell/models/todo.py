# coding: utf8
# try something like
import datetime
now = datetime.date.today()
todo=SQLDB("sqlite://todo.db")
db.define_table('queue',
                SQLField('name'))
db.define_table('task',
                SQLField('create_time','date',default=now),
                SQLField('end_time','date',default=now),
                SQLField('subject',length=256),
                SQLField('comment',length=256),
                SQLField('status',default=0),
                SQLField('queue',db.queue),
                
                )
db.queue.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'queue.name')]

db.task.subject.requires=[IS_NOT_EMPTY()]
db.task.create_time.requires=IS_NOT_EMPTY()
db.task.queue.requires=IS_IN_DB(db,'queue.id','queue.name')
db.task.create_time.requires=IS_DATE()
db.task.end_time.requires=IS_DATE()
