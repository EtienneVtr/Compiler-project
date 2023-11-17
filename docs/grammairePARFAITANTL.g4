fICHIER -> 'with Ada.Text_IO ';' use Ada.text_IO ';'\nprocedure' iDENT 'is' dECLETOILE 'begin' iNSTRPLUS 'end' iDENTINTER ';' .

dECL -> 'type' iDENT dINTEROGATION ';'
    | pROCEDURE 
    | fUNC .

dECLETOILE -> dECL dECLETOILE
    | .

d -> 'access' iDENT 
    | 'record' cHAMPS cHAMPSPLUS 'end record' ';' .

dINTEROGATION -> is d
    | .

pROCEDURE -> pROCEDURE iDENT pARAMSINTER is dECLETOILE begin iNSTR iNSTRPLUS end iDENTINTER ';' .

fUNC -> function iDENT pARAMSINTER return tYPE is dECLETOILE begin iNSTR iNSTRPLUS end iDENTINTER ';' .

eXPR -> tERM oPTERMETOILE .

oPTERMETOILE -> oP tERM oPTERMETOILE
    | .

tERM -> int 
    | caractere vALEXPR
    | true 
    | false 
    | null 
    | not eXPR 
    | moins eXPR 
    | iDENT ( eXPR vIRGULEEXPRETOILE )  
    | new iDENT .


vALEXPR -> val eXPR
| .


vIRGULEEXPRETOILE -> virgule eXPR vIRGULEEXPRETOILE
    | .

    
iNSTR -> aCCES deuxpointsegal eXPR ';' 
    | return eXPRINTER ';' 
    | iDENT eXPRPARENTHETOILE ';' 
    | bEGIN 
    | iF 
    | fOR 
    | wHILE .
    

eXPRINTER -> eXPR
    | .

eXPRPARENTHETOILE -> ( eXPR ) eXPRPARENTHETOILE
    | .

iNSTRPLUS -> iNSTR iNSTRPLUS 
    | .

bEGIN -> begin iNSTR iNSTRPLUS end .

iF -> if eXPR then iNSTR iNSTRPLUS iF_TAIL .

iF_TAIL -> elsif eXPR then iNSTR iNSTRPLUS iF_TAIL 
    | iNSTRPLUSELSEINTER end if .

iNSTRPLUSELSEINTER -> else iNSTR iNSTRPLUS
    | .

fOR -> for iDENT in rEVERSEINTER eXPR troispoints eXPR loop iNSTR iNSTRPLUS end loop ';' .

rEVERSE -> reverse .

rEVERSEINTER -> rEVERSE
    | .

wHILE -> while eXPR loop iNSTR iNSTRPLUS end loop .

cHAMPS -> iDENT iDENTVIRGULEETOILE : tYPE ';'  .

iDENTVIRGULEETOILE -> virgule iDENT iDENTVIRGULEETOILE
    | .

cHAMPSPLUS -> cHAMPS cHAMPSPLUS
    | .

tYPE -> iDENT 
    | access iDENT .

pARAMS -> ( pARAM pARAMVIRGULEETOILE ) .

pARAMVIRGULEETOILE -> virgule pARAM pARAMVIRGULEETOILE
    | .

pARAMSINTER -> pARAMS  
    | .

pARAM -> iDENT iDENTVIRGULEETOILE : mODEINTER tYPE .

mODEINTER -> mODE
    | .

mODE -> in oUT .

oUT -> out
| .

oP -> and tHEN
    | or eLSE
    | equal 
    | different 
    | inferior 
    | inferioregal 
    | superior 
    | superioregal 
    | mult 
    | division
    | rem 
    | plus 
    | moins .

tHEN -> then
| .

eLSE -> else
| .


aCCES ->  iDENT 
    | eXPR point iDENT .


iDENT -> ident .

iDENTINTER -> iDENT
    | .
