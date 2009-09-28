#!/usr/bin/python
import cmd
import string, sys
import lib_sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

def convert_cn(s):
    return s.encode('gb18030')

class CLI(cmd.Cmd):

    def __init__(self,db):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.mysqlite3 = lib_sqlite3.MySqlite3(db)
    def do_list(self,arg):
        self.mysqlite3.list(arg)
    
    def do_add(self,sub):
        self.mysqlite3.add(sub)

    def do_done(self,tid):
        self.mysqlite3.done(tid)

    def do_hello(self, arg):
        print "hello again", arg, "!"

    def help_hello(self):
        print "syntax: hello [message]",
        print "-- prints a hello message"

    def do_quit(self, arg):
        sys.exit(1)
    def do_exit(self, arg):
        sys.exit(1)

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"
    def help_exit(self):
        print "syntax: exit",
        print "-- terminates the application"
    
    # shortcuts
    do_q = do_quit

cli = CLI("todo.db")
cli.cmdloop()
