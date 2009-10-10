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
class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        self.create_gui_controls(parent,id,title)
        self.obj_sqlite3 = cls_sqlite3("todo.db")
        self.init_ctrl()
    def create_gui_controls(self,parent,id,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, wx.DefaultPosition,wx.Size(480,540))
        self.pnl_bk = wx.Panel(self, wx.ID_ANY,wx.Point(3,2),wx.Size(457,455))
        self.tc_left = wx.TreeCtrl(self.pnl_bk,ID_TREE, wx.Point(7,12),wx.Size(155,390),wx.TR_HAS_BUTTONS + wx.TR_EXTENDED + wx.TR_LINES_AT_ROOT, wx.DefaultValidator)
        self.ls_main = wx.CheckListBox(self.pnl_bk,ID_LIST,wx.Point(166,12),wx.Size(284,389))
        self.edt_text = wx.TextCtrl(self.pnl_bk,ID_TEXT,"",wx.Point(12,414),wx.Size(350,31),0,wx.DefaultValidator)
        self.btn_add = wx.Button(self.pnl_bk,ID_BTN,"Add",wx.Point(369,414),wx.Size(81,32),0,wx.DefaultValidator)
        #self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A StatusBar in the bottom of the window
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
        self.Show(True)
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
        sql = "select subject from task where status = 0;"
        rec = self.obj_sqlite3.exec_select(sql)
        for itm in rec:
            #self.ls_main.InsertItem(0,itm[0])
            self.ls_main.Append(unicode(itm[0],'utf-8'))
    def On_TreeCtrl_Activated(self,e):
        #print "abc"
        pass
    def On_TreeCtrl_Sel_Changed(self,e):
        #print "bbb"
        itm_parent  = self.tc_left.GetItemParent(e.GetItem())
        str_item = self.tc_left.GetItemText(e.GetItem())
        str_kind = self.tc_left.GetItemText(itm_parent)
        lst_queue = self.obj_sqlite3.get_queues()
        self.ls_main.Clear()
        if cmp(str_kind,"TODO") == 0:
            if cmp("All",str_item) == 0:
                sql = "select subject from task where status = 0;"
            else:
                sql = "select subject from task where status = 0 and queue_id = %s" % str(lst_queue.index(self.tc_left.GetItemText(e.GetItem())) + 1)
            rec = self.obj_sqlite3.exec_select(sql)
            for itm in rec:
                self.ls_main.Append(unicode(itm[0],'utf-8'))
        elif cmp(str_kind,"DONE") == 0:
            if cmp("All",str_item) == 0:
                sql = "select subject from task where status = 1;"
            else:
                sql = "select subject from task where status = 1 and queue_id = %s" % str(lst_queue.index(str_item) + 1)
            rec = self.obj_sqlite3.exec_select(sql)
            for itm in rec:
                self.ls_main.Append(unicode(itm[0],'utf-8'))
        #print self.tc_left.GetItemText(itm_parent) + self.tc_left.GetItemText(e.GetItem())
    def On_Add_Click(self,e):
        #add task
        lst_queue = self.obj_sqlite3.get_queues()
        n_queue = lst_queue.index(self.tc_left.GetItemText(self.tc_left.GetSelection())) + 1
        #print n_queue
        if cmp(0,n_queue) == 0:
            str_queue = '1'
        else:
            str_queue = str(n_queue)
        str_subject = self.edt_text.GetValue()
        dt_create = dt_create = str(datetime.date.today())[0:10]
        sql = "insert into task values (NULL,'%s',NULL,'%s',NULL,0,%s);" % (dt_create,str_subject,str_queue)
        self.obj_sqlite3.exec_update(sql)
        self.edt_text.Clear()
    def On_CheckListBox(self,e):
        itm_checked = self.ls_main.GetItem()
        print 'abc'
    def OnAbout(self,e):
        d= wx.MessageDialog( self, " TodoShell \n"
                            " in wxPython","About TodoShell", wx.OK)
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
