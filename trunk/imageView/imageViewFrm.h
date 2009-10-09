//---------------------------------------------------------------------------
//
// Name:        imageViewFrm.h
// Author:      riverbird
// Created:     2009/10/9 22:42:53
// Description: imageViewFrm class declaration
//
//---------------------------------------------------------------------------

#ifndef __IMAGEVIEWFRM_h__
#define __IMAGEVIEWFRM_h__

#ifdef __BORLANDC__
	#pragma hdrstop
#endif

#ifndef WX_PRECOMP
	#include <wx/wx.h>
	#include <wx/frame.h>
#else
	#include <wx/wxprec.h>
#endif

//Do not add custom headers between 
//Header Include Start and Header Include End.
//wxDev-C++ designer will remove them. Add custom headers after the block.
////Header Include Start
#include <wx/button.h>
#include <wx/checklst.h>
#include <wx/textctrl.h>
#include <wx/treectrl.h>
#include <wx/panel.h>
////Header Include End

////Dialog Style Start
#undef imageViewFrm_STYLE
#define imageViewFrm_STYLE wxCAPTION | wxSYSTEM_MENU | wxMINIMIZE_BOX | wxMAXIMIZE_BOX | wxCLOSE_BOX
////Dialog Style End

class imageViewFrm : public wxFrame
{
	private:
		DECLARE_EVENT_TABLE();
		
	public:
		imageViewFrm(wxWindow *parent, wxWindowID id = 1, const wxString &title = wxT("imageView"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxDefaultSize, long style = imageViewFrm_STYLE);
		virtual ~imageViewFrm();
		void btn_addClick(wxCommandEvent& event);
		
	private:
		//Do not add custom control declarations between
		//GUI Control Declaration Start and GUI Control Declaration End.
		//wxDev-C++ will remove them. Add custom code after the block.
		////GUI Control Declaration Start
		wxButton *btn_add;
		wxCheckListBox *ls_main;
		wxTextCtrl *edt_text;
		wxTreeCtrl *tc_left;
		wxPanel *WxPanel1;
		////GUI Control Declaration End
		
	private:
		//Note: if you receive any error with these enum IDs, then you need to
		//change your old form code that are based on the #define control IDs.
		//#defines may replace a numeric value for the enum names.
		//Try copy and pasting the below block in your old form header files.
		enum
		{
			////GUI Enum Control ID Start
			ID_WXBUTTON1 = 1031,
			ID_WXCHECKLISTBOX1 = 1030,
			ID_WXEDIT1 = 1029,
			ID_WXTREECTRL1 = 1028,
			ID_WXPANEL1 = 1027,
			////GUI Enum Control ID End
			ID_DUMMY_VALUE_ //don't remove this value unless you have other enum values
		};
		
	private:
		void OnClose(wxCloseEvent& event);
		void CreateGUIControls();
};

#endif
