grammar Gramada;

fICHIER :	'with Ada.Text_IO ; use Ada.Text_IO ;\nprocedure' IDENT 'is' dECL*'\nbegin' iNSTR+ 'end' iDENTINTER ';';

dECL :	'type' IDENT ('is' d)? ';' | pROCEDURE | fUNC;

d : 'access' IDENT | 'record' cHAMPS+ 'end record ;';

pROCEDURE :	'procedure' IDENT pARAMS? 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT? ';';

fUNC :	'function' IDENT pARAMS? 'return' tYPE 'is' dECL*'\nbegin' iNSTR+ 'end' IDENT?';';

eXPR :	tERM (oP tERM)*;

tERM :	ENTIER | CHAR vALEXPR |	'true' | 'false' | 'null' | 'not' eXPR | '-' eXPR | IDENT '(' eXPR vIRGULEEXPRETOILE ')' | 'new' IDENT ;

vALEXPR :	'val' eXPR | '';

iNSTR : IDENT hELP2 |	'return' eXPR? ';' |	bEGIN |	iF |	fOR |	wHILE;

hELP2 :	':=' eXPR ';' |	'(' eXPR hELP;

hELP3 :	')' hELP |	',' eXPR (','eXPR)* ')' (oP tERM)* IDENT ':=' eXPR ';';

hELP :	('(' eXPR ')')* ';' |	IDENT ':=' eXPR ';' |	(oP tERM)+ IDENT ':=' eXPR ';';

bEGIN :	'begin' iNSTR+ 'end';

iF :	'if' eXPR 'then' iNSTR+ iF_TAIL;

iF_TAIL :	'elsif' eXPR 'then' iNSTR+ iF_TAIL |	('else' iNSTR+)? 'end' 'if';

fOR :	'for' IDENT 'in' 'reverse'? eXPR '...' eXPR'\nloop' iNSTR+ 'end' 'loop' ';';

wHILE :	'while' eXPR 'loop' iNSTR+ 'end loop';

cHAMPS :	IDENT (','IDENT)* ':' tYPE ';';

tYPE :	IDENT |	'access' IDENT ;

pARAMS :	'('pARAM (','pARAM)*')';

pARAM :	IDENT (','IDENT)* ':' mODE? tYPE;

mODE :	'in' 'out'?;

oP :	'and' 'then'? |	'or' 'else'? |	'=' |	'/=' |	'<' |	'<=' |	'>' |	'>=' |	'*' |	'/' |	'rem' |	'+' |	'-';

aCCES :	IDENT |	eXPR'.'IDENT;

iDENTINTER :	IDENT |	'';

IDENT: CHAR(ENTIER | CHAR | '_')*;
ENTIER : [0-9]+;
CHAR : [a-zA-Z];