#!/usr/bin/python
# coding:utf-8
import os
import wx
import sqlite3
import datetime

ID_ABOUT=101
ID_EXIT=110
ID_PANEL_BK = 111
ID_TREE = 112
ID_LIST = 113
ID_TEXT = 114
ID_BTN = 115
ID_STATUS_BAR = 116
class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        self.create_gui_controls(parent,id,title)
        self.obj_sqlite3 = cls_sqlite3("todo.db")
        self.init_ctrl()
    def create_gui_controls(self,parent,id,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, wx.DefaultPosition,wx.Size(740,540),wx.DEFAULT_FRAME_STYLE + wx.TAB_TRAVERSAL)
        #self.SetSizeHints( wx.DefaultSize, wx.DefaultSize );
        self.pnl_bk = wx.Panel(self, wx.ID_ANY,wx.Point(2,2),wx.Size(457,455))
        self.boxsizer_bk = wx.BoxSizer(wx.VERTICAL)
        self.boxsizer_top = wx.BoxSizer(wx.HORIZONTAL)
        
        #category
        self.tc_left = wx.TreeCtrl(self.pnl_bk,ID_TREE, wx.Point(7,12),wx.Size(155,390),wx.TR_HAS_BUTTONS + wx.TR_EXTENDED + wx.TR_LINES_AT_ROOT, wx.DefaultValidator)
        self.boxsizer_top.Add(self.tc_left,0,wx.ALL + wx.EXPAND,5)
        
        #task list
        self.ls_main = wx.CheckListBox(self.pnl_bk,ID_LIST,wx.Point(166,12),wx.Size(284,389))
        self.boxsizer_top.Add(self.ls_main,1,wx.ALL + wx.EXPAND,5)
        
        #task comment
        self.edt_comment = wx.TextCtrl(self.pnl_bk,ID_TEXT,"",wx.Point(12,414),wx.Size(250,31),0,wx.DefaultValidator)
        self.boxsizer_top.Add(self.edt_comment,0,wx.ALL + wx.EXPAND,5)
        
        self.boxsizer_bk.Add(self.boxsizer_top,1,wx.EXPAND,5)
        self.boxsizer_btm = wx.BoxSizer(wx.HORIZONTAL)
        
        #task text
        self.edt_text = wx.TextCtrl(self.pnl_bk,ID_TEXT,"",wx.Point(12,414),wx.Size(350,31),wx.TE_PROCESS_ENTER,wx.DefaultValidator)
        self.boxsizer_btm.Add(self.edt_text,1,wx.ALL + wx.EXPAND,5)
        
        #add task button
        self.btn_add = wx.Button(self.pnl_bk,ID_BTN,"Add",wx.Point(369,414),wx.Size(81,32),0,wx.DefaultValidator)
        self.boxsizer_btm.Add(self.btn_add,0,wx.ALL,5)
        
        self.boxsizer_bk.Add(self.boxsizer_btm,0,0,5)
        
        self.pnl_bk.SetSizer(self.boxsizer_bk)
        self.pnl_bk.Layout()
        
        #self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Welcome to Todoshell!")
        # Setting up the menu.
        filemenu= wx.Menu()
        filemenu.Append(ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout) # attach the menu-event ID_ABOUT to the
                                                           # method self.OnAbout
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)   # attach the menu-event ID_EXIT to the
                                                           # method self.OnExit
        wx.EVT_TREE_ITEM_ACTIVATED(self.tc_left, ID_TREE, self.On_TreeCtrl_Activated )
        wx.EVT_TREE_SEL_CHANGED(self.tc_left,ID_TREE, self.On_TreeCtrl_Sel_Changed )
        wx.EVT_BUTTON(self.btn_add,ID_BTN,self.On_Add_Click )
        wx.EVT_CHECKLISTBOX(self.ls_main,ID_LIST, self.On_CheckListBox )
        wx.EVT_TEXT_ENTER(self.edt_text, ID_TEXT, self.On_Text_Enter) 
        self.Show(True)
        self.Centre()
    def init_ctrl(self):
        #init left tree view
        itm_root = self.tc_left.AddRoot("Category")
        lst_queue = self.obj_sqlite3.get_queues()
        itm_todo = self.tc_left.AppendItem(itm_root,"TODO")
        itm_done = self.tc_left.AppendItem(itm_root,"DONE")
        self.tc_left.AppendItem(itm_todo,"All")
        self.tc_left.AppendItem(itm_done,"All")
        for str_queue in lst_queue:
            self.tc_left.AppendItem(itm_todo,str_queue)
            self.tc_left.AppendItem(itm_done,str_queue)
        #init main list box
        self.ls_main.Clear()
        sql = "select id,subject from task where status = 0;"
        rec = self.obj_sqlite3.exec_select(sql)
        for itm in rec:
            #self.ls_main.InsertItem(0,itm[0])
            self.ls_main.Append(str(itm[0]) + "." + unicode(itm[1],'utf-8'))
    def On_TreeCtrl_Activated(self,e):
        #print "abc"
        pass
    def show_list(self):
        self.ls_main.Clear()
        itm_parent  = self.tc_left.GetItemParent(self.tc_left.GetSelection())
        if not itm_parent:
            sql = "select id,subject,status from task;"
            rec = self.obj_sqlite3.exec_select(sql)
            n_itm = 0
            for itm in rec:
                self.ls_main.Append(str(itm[0]) + "." + unicode(itm[1],'utf-8'))
                if cmp(1,itm[2]) == 0:
                    self.ls_main.Check(n_itm,True)
                n_itm = n_itm + 1
            self.statusbar.SetStatusText("任务数量:" + str(self.ls_main.GetCount()))
            return
        str_item = self.tc_left.GetItemText(self.tc_left.GetSelection())
        str_kind = self.tc_left.GetItemText(itm_parent)
        #show todo and done
        if cmp("Category",str_kind) == 0:
            if cmp("TODO",str_item) == 0:
                sql = "select id,subject,status from task where status = 0;"
            else:
                sql = "select id,subject,status from task where status = 1;"
            rec = self.obj_sqlite3.exec_select(sql)
            n_itm = 0
            for itm in rec:
                self.ls_main.Append(str(itm[0]) + "." + unicode(itm[1],'utf-8'))
                if cmp(1,itm[2]) == 0:
                    self.ls_main.Check(n_itm,True)
                    n_itm = n_itm + 1
            self.statusbar.SetStatusText("任务数量:" + str(self.ls_main.GetCount()))
            return
        lst_queue = self.obj_sqlite3.get_queues()
        #show subsubject
        if cmp(str_kind,"TODO") == 0:
            if cmp("All",str_item) == 0:
                sql = "select id,subject,status from task where status = 0;"
            else:
                sql = "select id,subject,status from task where status = 0 and queue_id = %s" % str(lst_queue.index(str_item) + 1)
            rec = self.obj_sqlite3.exec_select(sql)
            n_itm = 0
            for itm in rec:
                self.ls_main.Append(str(itm[0]) + "." + unicode(itm[1],'utf-8'))
                if cmp(1,itm[2]) == 0:
                    self.ls_main.Check(n_itm,True)
                    n_itm = n_itm + 1
        elif cmp(str_kind,"DONE") == 0:
            if cmp("All",str_item) == 0:
                sql = "select id,subject,status from task where status = 1;"
            else:
                sql = "select id,subject,status from task where status = 1 and queue_id = %s" % str(lst_queue.index(str_item) + 1)
            rec = self.obj_sqlite3.exec_select(sql)
            n_itm = 0
            for itm in rec:
                self.ls_main.Append(str(itm[0]) + "." + unicode(itm[1],'utf-8'))
                if cmp(1,itm[2]) == 0:
                    self.ls_main.Check(n_itm,True)
                    n_itm = n_itm + 1
        #print self.tc_left.GetItemText(itm_parent) + self.tc_left.GetItemText(e.GetItem())
        self.statusbar.SetStatusText("任务数量:" + str(self.ls_main.GetCount()))
    def On_TreeCtrl_Sel_Changed(self,e):
        self.show_list()
    def add_task(self,str_task):
        #add task
        lst_queue = self.obj_sqlite3.get_queues()
        n_queue = lst_queue.index(self.tc_left.GetItemText(self.tc_left.GetSelection())) + 1
        #print n_queue
        if cmp(0,n_queue) == 0:
            str_queue = '1'
        else:
            str_queue = str(n_queue)
        str_subject = str_task
        dt_create = dt_create = str(datetime.date.today())[0:10]
        sql = "insert into task values (NULL,'%s',NULL,'%s',NULL,0,%s);" % (dt_create,str_subject,str_queue)
        self.obj_sqlite3.exec_update(sql)
        self.edt_text.Clear()
        self.show_list()
    def On_Add_Click(self,e):
        #add task
        str_task = self.edt_text.GetValue()
        self.add_task(str_task)
    def On_Text_Enter(self,e):
        str_task = self.edt_text.GetValue()
        self.add_task(str_task)
    def On_CheckListBox(self,e):
        #print self.ls_main.IsChecked(e.GetSelection())
        dt_end = str(datetime.date.today())[0:10]
        str_sel = self.ls_main.GetString(e.GetSelection())
        str_sel = str_sel[0:str_sel.find('.')]
        if self.ls_main.IsChecked(e.GetSelection()):
            sql = "update task set end_time = '%s', status = 1 where id = %s;" % (dt_end,str_sel)
        else:
            sql = "update task set end_time = '%s', status = 0 where id = %s;" % ("",str_sel)
        self.obj_sqlite3.exec_update(sql)
        self.show_list()
    def OnAbout(self,e):
        d= wx.MessageDialog( self, " TodoShell \n"
                            "2009.1","About TodoShell", wx.OK)
                            # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
    def OnExit(self,e):
        self.Close(True)  # Close the frame.

class cls_sqlite3():
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.conn.text_factory = str
        self.c = self.conn.cursor()
    def exec_select(self,sql):
        rec = self.c.execute(sql)
        return rec
    def exec_update(self,sql):
        try:
            rec = self.c.execute(sql)
            self.conn.commit()
        except Exception,e:
            print str(e)
    def get_queues(self):
        sql = "select name from queue;"
        rec = self.c.execute(sql)
        lst_ret = list()
        for itm in rec:
            lst_ret.append(itm[0])
        return lst_ret
    def get_all_task(self):
        sql = "select subject,status,comment from task;"
        rec = self.c.execute(sql)
        return rec
    def close(self):
        self.c.close()

app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Todoshell GUI")
app.MainLoop()
