# coding: utf8
# try something like
def index(): return dict(message="hello from todoshell application")
def tasks():
    #recores=db().select(db.task.ALL,orderby=db.task.id)
    #return dict(records=SQLTABLE(recores))
    records=db(db.task.queue==request.vars.queue).select(orderby=db.task.id)
    form=SQLFORM(db.task,fields=['queue'])
    return dict(form=form,records=records)
    
def show():
    id=request.vars.id
    tasks=db(db.task.id==id).select()
    if not len(tasks): redirect(URL(r=request,f='tasks'))
    return dict(task=tasks[0])

def new_task():
    form=SQLFORM(db.task,fields=['subject','comment',\
        'create_time','queue'])
    if form.accepts(request.vars,session):
        redirect(URL(r=request,f='tasks'))
    return dict(form=form)
