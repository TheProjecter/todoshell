//---------------------------------------------------------------------------
//
// Name:        imageViewFrm.cpp
// Author:      riverbird
// Created:     2009/10/9 22:42:53
// Description: imageViewFrm class implementation
//
//---------------------------------------------------------------------------

#include "imageViewFrm.h"

//Do not add custom headers between
//Header Include Start and Header Include End
//wxDev-C++ designer will remove them
////Header Include Start
////Header Include End

//----------------------------------------------------------------------------
// imageViewFrm
//----------------------------------------------------------------------------
//Add Custom Events only in the appropriate block.
//Code added in other places will be removed by wxDev-C++
////Event Table Start
BEGIN_EVENT_TABLE(imageViewFrm,wxFrame)
	////Manual Code Start
	////Manual Code End
	
	EVT_CLOSE(imageViewFrm::OnClose)
	EVT_BUTTON(ID_WXBUTTON1,imageViewFrm::btn_addClick)
END_EVENT_TABLE()
////Event Table End

imageViewFrm::imageViewFrm(wxWindow *parent, wxWindowID id, const wxString &title, const wxPoint &position, const wxSize& size, long style)
: wxFrame(parent, id, title, position, size, style)
{
	CreateGUIControls();
}

imageViewFrm::~imageViewFrm()
{
}

void imageViewFrm::CreateGUIControls()
{
	//Do not add custom code between
	//GUI Items Creation Start and GUI Items Creation End
	//wxDev-C++ designer will remove them.
	//Add the custom code before or after the blocks
	////GUI Items Creation Start

	WxPanel1 = new wxPanel(this, ID_WXPANEL1, wxPoint(3, 2), wxSize(457, 455));

	tc_left = new wxTreeCtrl(WxPanel1, ID_WXTREECTRL1, wxPoint(7, 13), wxSize(155, 390), wxTR_HAS_BUTTONS, wxDefaultValidator, wxT("tc_left"));

	edt_text = new wxTextCtrl(WxPanel1, ID_WXEDIT1, wxT(""), wxPoint(12, 414), wxSize(350, 31), 0, wxDefaultValidator, wxT("edt_text"));

	wxArrayString arrayStringFor_ls_main;
	ls_main = new wxCheckListBox(WxPanel1, ID_WXCHECKLISTBOX1, wxPoint(166, 12), wxSize(284, 389), arrayStringFor_ls_main, wxLB_SINGLE, wxDefaultValidator, wxT("ls_main"));

	btn_add = new wxButton(WxPanel1, ID_WXBUTTON1, wxT("Add"), wxPoint(369, 414), wxSize(81, 32), 0, wxDefaultValidator, wxT("btn_add"));

	SetTitle(wxT("imageView"));
	SetIcon(wxNullIcon);
	SetSize(8,8,477,498);
	Center();
	
	////GUI Items Creation End
}

void imageViewFrm::OnClose(wxCloseEvent& event)
{
	Destroy();
}

/*
 * btn_addClick
 */
void imageViewFrm::btn_addClick(wxCommandEvent& event)
{
	// insert your code here
	
}
