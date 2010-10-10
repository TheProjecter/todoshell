program todogui;

{$mode objfpc}{$H+}

uses
  {$IFDEF UNIX}{$IFDEF UseCThreads}
  cthreads,
  {$ENDIF}{$ENDIF}
  Interfaces, // this includes the LCL widgetset
  Forms, main, LResources, SQLDBLaz, about
  { you can add units after this };

{$IFDEF WINDOWS}{$R todogui.rc}{$ENDIF}

begin
    Application.Title:='TodoshellGUI';
  {$I todogui.lrs}
  Application.Initialize;
  Application.CreateForm(Tfrm_main, frm_main);
    Application.CreateForm(Tfrm_about, frm_about);
  Application.Run;
end.

