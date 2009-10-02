import sqlite3
import datetime
import sys
import platform

reload(sys)
sys.setdefaultencoding('utf8')

def convert_utf(s):
    return s.encode('utf8')    

def convert_gbk(s):
    return s.encode('gb2312')

def inred( s ):
    return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

def ingreen( s ):
    return "%s[32;2m%s%s[0m"%(chr(27), s, chr(27))

def inblue( s ):
    return "%s[33;2m%s%s[0m"%(chr(27), s, chr(27))

class MySqlite3:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.c = self.conn.cursor()
    def list(self,args):
        str_head = "|id   |create  date| subject                      |"        
        if cmp(args.find('@'),-1) == 0:
            arg = args
            if cmp(arg,"todo") == 0:
                sql = "select id,create_time,subject from task where status = 0;"
            elif cmp(arg,"all") == 0:
                sql = "select id,create_time,subject from task;"
            elif cmp(arg,"done") == 0:
                str_head = "id | create date | end date | subject |"
                sql = "select id,create_time,subject from task where status = 1;"
            elif cmp(arg,"queue") == 0:
                str_head = "id | queue name |"
                sql = "select id,name from queue;"
            else:
                sql = "select id,create_time,subject from task where status = 0;"
        else:
            arg = args[0:args.find('@')]
            queue = args[args.find('@') + 1:len(args)]
            if cmp(arg,"todo") == 0:
                sql = "select id,create_time,subject from task where status = 0 and queue_id = %s;" % queue
            elif cmp(arg,"all") == 0:
                sql = "select id,create_time,subject from task where queue_id = %s;" % queue
            elif cmp(arg,"done") == 0:
                str_head = "id | create date | end date | subject |"
                sql = "select id,create_time,subject from task where status = 1 and queue_id = %s;"  % queue
            elif cmp(arg,"queue") == 0:
                str_head = "id | queue name |"
                sql = "select id,name from queue;"
            else:
                sql = "select id,create_time,subject from task where status = 0 and queue_id = %s;" % queue
        rec = self.c.execute(sql)
        #print self.c.fetchall()
        print "+=================================================+"
        print str_head
        print "+=================================================+"
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
            if cmp(platform.platform(),"Windows-32bit") == 0:
                sys.stdout.write(str_id + " | ")
                sys.stdout.write(ln[1] + " | ")
                if len(ln) > 2:
                    sys.stdout.write(convert_gbk(ln[2]))
            else:
                sys.stdout.write(ingreen(str_id) + " | ")
                sys.stdout.write(inblue(ln[1]) + " | ")
                if len(ln) > 2:
                    sys.stdout.write(inred(convert_utf(ln[2])))
            sys.stdout.write('\n')
            cnt = cnt + 1
            print '-------------------------------------------------------'
        print "Total number:[%d]" % (cnt)
    def add(self,sub):
        dt_create = str(datetime.date.today())[0:10]
        if cmp(sub[0:5],"queue") == 0:
            sql = "insert into queue values (NULL,'%s');" % (sub[6:])
            str_prompt = "Queue added!"
        else:
            if cmp(sub.find('@'),-1) == 0:
                str_subject = sub
                str_queue = 1
            else:
                str_subject = sub[0:sub.find('@')] 
                str_queue = sub[sub.find('@')+1:len(sub)]
            sql = "insert into task values (NULL,'%s',NULL,'%s',NULL,0,%s);" % (dt_create,str_subject,str_queue)
            str_prompt = "Task added!"
            #print sql
        self.c.execute(sql)
        self.conn.commit()
        print str_prompt
    def done(self,tid):
        dt_end = str(datetime.date.today())[0:10]
        sql = "update task set end_time = '%s' ,status = 1 where id = %s;" % (dt_end,tid)
        #print sql
        self.c.execute(sql)
        self.conn.commit()
        print "Task[%s] just done!" % (tid)
