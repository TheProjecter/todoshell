import sqlite3
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def convert_cn(s):
    return s.encode('utf8')

class MySqlite3:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
    def list(self,arg):
        str_head = "id | create date | subject |"
        if cmp(arg,"todo") == 0:
            sql = "select id,create_time,subject from task where status = 0;"
        elif cmp(arg,"all") == 0:
            sql = "select id,create_time,subject from task;"
        elif cmp(arg,"done") == 0:
            str_head = "id | create date | end date | subject |"
            sql = "select id,create_time,end_time,subject from task where status = 1;"
        rec = self.c.execute(sql)
        #print self.c.fetchall()
        #print 'Total number: %d' % len(self.c.fetchall())
        print str_head
        print "==============================="
        for ln in rec:
            #print convert_cn(ln)
            for itm in ln:
                sys.stdout.write(convert_cn(str(itm)))
                sys.stdout.write(" | ")
            sys.stdout.write('\n')
    def add(self,sub):
        dt_create = str(datetime.date.today())[0:10]
        sql = "insert into task values (NULL,'%s',NULL,'%s',NULL,0);" % (dt_create,sub)
        #print sql
        self.c.execute(sql)
        self.conn.commit()
        print 'Task added!'
    def done(self,tid):
        dt_end = str(datetime.date.today())[0:10]
        sql = "update task set end_time = '%s' ,status = 1 where id = %s;" % (dt_end,tid)
        #print sql
        self.c.execute(sql)
        self.conn.commit()
        print "Task[%s] just done!" % (tid)
