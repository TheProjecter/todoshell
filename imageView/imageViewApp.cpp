//---------------------------------------------------------------------------
//
// Name:        imageViewApp.cpp
// Author:      riverbird
// Created:     2009/10/9 22:42:52
// Description: 
//
//---------------------------------------------------------------------------

#include "imageViewApp.h"
#include "imageViewFrm.h"

IMPLEMENT_APP(imageViewFrmApp)

bool imageViewFrmApp::OnInit()
{
    imageViewFrm* frame = new imageViewFrm(NULL);
    SetTopWindow(frame);
    frame->Show();
    return true;
}
 
int imageViewFrmApp::OnExit()
{
	return 0;
}
