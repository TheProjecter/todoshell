import sqlite3
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def convert_cn(s):
    return s.encode('utf8')

def inred( s ):
    return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

def ingreen( s ):
    return "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))

def inblue( s ):
    return "%s[33;2m%s%s[0m"%(chr(27), s, chr(27))

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
            sql = "select id,create_time,subject from task where status = 1;"
        else:
            sql = "select id,create_time,subject from task where status = 0;"
        rec = self.c.execute(sql)
        #print self.c.fetchall()
        
        print str_head
        print "==============================="
        cnt = 0
        for ln in rec:
            #print convert_cn(ln)
            str_id = str(ln[0])
            if len(str_id) == 1:
                str_id = "%s    " % str_id
            elif len(str_id) == 2:
                str_id = "%s   " % str_id
            elif len(str_id) == 3:
                str_id = "%s  " % str_id
            elif len(str_id) == 4:
                str_id = "%s " % str_id
            sys.stdout.write(ingreen(str_id) + " | ")
            sys.stdout.write(inblue(ln[1]) + " | ")
            sys.stdout.write(inred(convert_cn(ln[2])))
            sys.stdout.write('\n')
            cnt = cnt + 1
            print '-------------------------------------------------------'
        print "==============================="
        print "Total number:[%d]" % (cnt)
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
