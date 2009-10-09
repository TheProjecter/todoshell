//---------------------------------------------------------------------------
//
// Name:        imageViewApp.h
// Author:      riverbird
// Created:     2009/10/9 22:42:52
// Description: 
//
//---------------------------------------------------------------------------

#ifndef __IMAGEVIEWFRMApp_h__
#define __IMAGEVIEWFRMApp_h__

#ifdef __BORLANDC__
	#pragma hdrstop
#endif

#ifndef WX_PRECOMP
	#include <wx/wx.h>
#else
	#include <wx/wxprec.h>
#endif

class imageViewFrmApp : public wxApp
{
	public:
		bool OnInit();
		int OnExit();
};

#endif
