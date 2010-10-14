unit main;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, sqldb, sqlite3conn, FileUtil, LResources, Forms, Controls,
  Graphics, Dialogs, ExtCtrls, ComCtrls, CheckLst, StdCtrls, Buttons, Menus,about;

type

  { Tfrm_main }

  Tfrm_main = class(TForm)
    btn_add: TBitBtn;
    clb_task: TCheckListBox;
    edt_task: TEdit;
    MainMenu1: TMainMenu;
    MenuItem1: TMenuItem;
    mn_del_queue: TMenuItem;
    mn_modify_queue: TMenuItem;
    mn_add_queue: TMenuItem;
    mn_about: TMenuItem;
    mn_help: TMenuItem;
    mn_file: TMenuItem;
    mn_exit: TMenuItem;
    Panel2: TPanel;
    PopupMenu1: TPopupMenu;
    Splitter1: TSplitter;
    query: TSQLQuery;
    conn: TSQLite3Connection;
    transaction: TSQLTransaction;
    StatusBar1: TStatusBar;
    tv_cate: TTreeView;
    procedure btn_addClick(Sender: TObject);
    procedure clb_taskClickCheck(Sender: TObject);
    procedure edt_taskKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState
        );
    procedure FormShow(Sender: TObject);
    procedure mn_aboutClick(Sender: TObject);
    procedure mn_add_queueClick(Sender: TObject);
    procedure mn_del_queueClick(Sender: TObject);
    procedure mn_exitClick(Sender: TObject);
    procedure mn_fileClick(Sender: TObject);
    procedure mn_modify_queueClick(Sender: TObject);
    procedure PopupMenu1Popup(Sender: TObject);
    procedure tv_cateChange(Sender: TObject; Node: TTreeNode);
    procedure tv_cateClick(Sender: TObject);

    procedure add_task();
  private
    { private declarations }
  public
    { public declarations }
  end; 

var
  frm_main: Tfrm_main;

implementation

{ Tfrm_main }

procedure Tfrm_main.mn_fileClick(Sender: TObject);
begin

end;

procedure Tfrm_main.mn_modify_queueClick(Sender: TObject);
var
queue:string;
old_queue:string;
sql:string;
select_index:Integer;
begin
     old_queue := tv_cate.Selected.Text;
     select_index := tv_cate.Selected.Index;
     queue := InputBox('Modify Queue','Please Input the new queue name:',old_queue);
     // Update database;
     sql := Format('update queue set name = "%s" where name = "%s";',[queue,old_queue]);
     query.Close;
     query.SQL.Text := sql;
     query.ExecSQL;
     transaction.Commit;
     // Update GUI
     tv_cate.Selected.Text:=queue;
     tv_cate.Items[0].Items[1].Items[select_index].Text:=queue;
end;

procedure Tfrm_main.PopupMenu1Popup(Sender: TObject);
begin
    if (tv_cate.Selected.Parent = tv_cate.Items[0].Items[0]) or (tv_cate.Selected.Parent = tv_cate.Items[0].Items[1]) then
       begin
       mn_modify_queue.Enabled := true;
       mn_del_queue.Enabled := true;
       end
    else
        begin
        mn_modify_queue.Enabled := false;
        mn_del_queue.Enabled := false;
        end;
end;

procedure Tfrm_main.tv_cateChange(Sender: TObject; Node: TTreeNode);
var
sql:string;
queue : string;
task:string;
task_id:integer;
str_temp:string;
task_index:integer;
status:integer;
begin
     clb_task.Clear;
     if tv_cate.Items.Count = 0 then
        exit;
     if tv_cate.Items[0].Items[0].Selected then
        begin
        sql := 'select id,subject,status from task where status = 0;';
        end
     else if tv_cate.Items[0].Items[1].Selected then
        begin
        sql := 'select id,subject,status from task where status = 1;';
        end
     else if tv_cate.Items[0].Selected then
        begin
        sql := 'select id,subject,status from task;';
        end
     else
         begin
         if Node = nil then
            exit;
         queue := Node.Text;
         if (Node.Parent.Text = 'TODO') then
            sql := 'select task.id,task.subject,task.status from task,queue where queue.name = "' + queue + '" and task.queue_id = queue.id and task.status = 0;'
         else
            sql := 'select task.id,task.subject,task.status from task,queue where queue.name = "' + queue + '" and task.queue_id = queue.id and task.status = 1;';
         end;

     query.Close;
     query.SQL.Text:=sql;
     query.Open;
     while not query.EOF do
           begin
           task_id := query.FieldByName('id').AsInteger;
           task := query.FieldByName('subject').AsString;
           status := query.FieldByName('status').AsInteger;
           str_temp := IntToStr(task_id) + '.' + task;
           task_index := clb_task.Items.Add(str_temp);
           if (status = 1) then
              begin
              clb_task.Checked[task_index] := true;
              end;
           query.Next;
           end;
end;

procedure Tfrm_main.tv_cateClick(Sender: TObject);
begin
end;

procedure Tfrm_main.mn_exitClick(Sender: TObject);
begin
  self.Close;
  Application.Terminate;
end;

procedure Tfrm_main.FormShow(Sender: TObject);
var
   sql:string;
   n:integer;
   queue:string;
   task:string;
   id:integer;
   str_temp:string;
begin
     // treeview init;
     conn.DatabaseName:= '..\\..\\todo.db';
     try
        conn.Open;
     except
        ShowMessage('Open database [..\\..\\todo.db] failed.');
        self.Close;
     end;
     if (conn.Connected) then
        begin
        sql := 'select id,name from queue;';
        query.Close;
        query.SQL.Text:= sql;
        query.Open;

        for n:=0 to query.RecordCount -1 do
            begin
            queue := query.FieldByName('name').AsString;
            tv_cate.Items.AddChild(tv_cate.Items[0].Items[0],queue);
            tv_cate.Items.AddChild(tv_cate.Items[0].Items[1],queue);
            query.Next;
            end;
        end;
     tv_cate.Items[0].Items[0].Selected:=true;
     tv_cate.Items[0].Expanded:=true;

     //check list box init
     clb_task.Clear;
     sql := 'select id,subject from task where status = 0;';
     query.Close;
     query.SQL.Text := sql;
     query.Open;
     while not query.EOF do
           begin
           id := query.FieldByName('id').AsInteger;
           task := query.FieldByName('subject').AsString;
           str_temp := IntToStr(id) + '.' + task;
           clb_task.Items.Add(str_temp);
           query.Next;
           end;
end;

procedure Tfrm_main.mn_aboutClick(Sender: TObject);
var
frm_about:Tfrm_about;
begin
     frm_about := Tfrm_about.Create(Self);
     try
        frm_about.ShowModal;
     finally
        frm_about.Free;
     end;
end;

procedure Tfrm_main.mn_add_queueClick(Sender: TObject);
var
   queue:string;
   sql:string;
begin
    queue := InputBox('Add Queue','Please input new queue name:','');
    if Length(queue) = 0 then
       exit;
    // database written.
    sql := Format('insert into queue values(NULL,"%s");',[queue]);
    query.Close;
    query.SQL.Text := sql;
    query.ExecSQL;
    transaction.Commit;
    // update Gui
    tv_cate.Items.AddChild(tv_cate.Items[0].Items[0],queue);
    tv_cate.Items.AddChild(tv_cate.Items[0].Items[1],queue);
end;

procedure Tfrm_main.mn_del_queueClick(Sender: TObject);
var
dlg_result:Integer;
queue:string;
sql:string;
msg:string;
select_index:Integer;
begin
     queue := tv_cate.Selected.Text;
     select_index := tv_cate.Selected.Index;
     msg := Format('When delete queue[%s], all of its task will delete, please confirm:',[queue]);
     sql := Format('delete from queue where name = "%s";',[queue]);
     dlg_result := MessageDlg(msg,mtConfirmation,[mbYes,mbNo],0);
     if dlg_result = mrYes then
        begin
        // delete task of this queue
        sql := Format('delete from task where task.queue_id = (select id from queue where name = "%s");',[queue]);
        query.Close;
        query.SQL.Text := sql;
        query.ExecSQL;
        transaction.Commit;
        // update db
        query.Close;
        query.SQL.Text:=sql;
        query.ExecSQL;
        transaction.Commit;
        // update gui
        tv_cate.Selected.Delete;
        tv_cate.Items[0].Items[1].Items[select_index].Delete;
        end;
end;

procedure Tfrm_main.btn_addClick(Sender: TObject);
begin
    add_task();
end;

procedure Tfrm_main.clb_taskClickCheck(Sender: TObject);
var
item_index:integer;
sql:string;
task_id:integer;
str_temp:string;
begin
     // Update task status into database;
     //ShowMessage(IntToStr(clb_task.ItemIndex));
     item_index := clb_task.ItemIndex;
     if item_index = -1 then
        item_index := 0;
     str_temp := clb_task.Items[item_index];
     task_id := Pos('.',str_temp);
     str_temp := LeftStr(str_temp,task_id - 1);
     task_id := StrToInt(str_temp);
    if clb_task.Checked[item_index] = true then
       begin
       sql := Format('update task set status = 1 where id = %d;',[task_id]);
       end
    else
       sql := Format('update task set status = 0 where id = %d;',[task_id]);
       query.Close;
       query.SQL.Text:= sql;
       query.ExecSQL;
       transaction.Commit;

    // Update listbox status


end;


procedure Tfrm_main.edt_taskKeyDown(Sender: TObject; var Key: Word;
    Shift: TShiftState);
begin
    if Key = 13 then
       begin
       add_task();
       end;
end;

procedure Tfrm_main.add_task();
var
sql:string;
current_time : string;
queue_id : integer;
subject : string;
begin
     //Save data to database;
     current_time := DateTimeToStr(Now());
     subject := edt_task.Text;
     if tv_cate.Items[0].Selected then
        queue_id := 0
     else if (tv_cate.Items[0].Items[0].Selected) then
        queue_id := 0
     else if tv_cate.Items[0].Items[1].Selected then
        queue_id := 0
     else
         queue_id := (tv_cate.Selected.Index) + 1;
     sql := Format('insert into task values (NULL,"%s","","%s","",0,%d);',[current_time,subject,queue_id]);
     query.Close;
     query.SQL.Text:=sql;
     query.ExecSQL;
     transaction.Commit;
     //Add to list box
     clb_task.Items.Add(subject);
end;

initialization
  {$I main.lrs}

end.

