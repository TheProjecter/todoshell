#!/usr/bin/python
import cmd
import string, sys
import lib_sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

class CLI(cmd.Cmd):

    def __init__(self,db):
        cmd.Cmd.__init__(self)
        self.prompt = "todo> "
        self.mysqlite3 = lib_sqlite3.MySqlite3(db)
    def do_list(self,arg):
        self.mysqlite3.list(arg)

    def help_list(self):
        print "syntax: list [todo|done|all|queue]"
        print "list todo -- list todo tasks."
        print "list done -- list finish tasks."
        print "list all -- list all tasks."
        print "list queue -- list all queue."
        
    def do_add(self,sub):
        self.mysqlite3.add(sub)

    def help_add(self):
        print "syntax: add [message]"
        print "-- add task to system"
        
    def do_done(self,tid):
        self.mysqlite3.done(tid)

    def help_done(self):
        print "syntax: done [task-id]"
        print "-- finish task by id"
        
    def do_quit(self, arg):
        sys.exit(1)

    def do_exit(self, arg):
        sys.exit(1)

    def do_EOF(self,arg):
        return True

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"

    def help_exit(self):
        print "syntax: exit",
        print "-- terminates the application"
    
    # shortcuts
    do_q = do_quit
    do_ls = do_list
cli = CLI("todo.db")
cli.cmdloop()
