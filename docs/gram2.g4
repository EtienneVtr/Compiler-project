FICHIER -> with ada point textio pointvirgule use ada point textio pointvirgule procedure IDENT is DECLETOILE begin INSTRPLUS end IDENTINTER pointvirgule .

DECL -> type IDENT ISDINTEROGATION pointvirgule
    | PROCEDURE 
    | FUNC .

DECLETOILE -> DECL DECLETOILE2
    | .

DECLETOILE2 -> DECL DECLETOILE2
    | .
 
D -> access IDENT 
    | record CHAMPSPLUS end record pointvirgule .

DINTEROGATION -> is D
    | .


PROCEDURE -> procedure IDENT PARAMSINTER is DECLETOILE begin INSTRPLUS end IDENTINTER pointvirgule .

FUNC -> function IDENT PARAMSINTER return TYPE is DECLETOILE begin INSTRPLUS end IDENTINTER pointvirgule .

EXPR -> TERM2 .

OPTERMETOILE -> OP TERM1
    | .

OPTERMETOILE2 -> OP TERM1
    | .

TERM -> int 
    | caractere  
    | true 
    | false 
    | null 
    | not EXPR 
    | moins EXPR 
    | IDENT ( EXPR VIRGULEEXPRETOILE )  
    | caractere val EXPR 
    | new IDENT .

TERM1 -> int OPTERMETOILE2
|    caractere OPTERMETOILE2
|    true OPTERMETOILE2
|    false OPTERMETOILE2
|    null OPTERMETOILE2
|    not EXPR OPTERMETOILE2
|    moins EXPR OPTERMETOILE2
|    IDENT ( EXPR ) VIRGULEEXPRETOILE OPTERMETOILE2
|    caractere val EXPR OPTERMETOILE2
|    new IDENT OPTERMETOILE2 .

TERM2 -> int OPTERMETOILE
|    caractere OPTERMETOILE
|    true OPTERMETOILE
|    false OPTERMETOILE
|    null OPTERMETOILE
|    not EXPR OPTERMETOILE
|    moins EXPR OPTERMETOILE
|    IDENT ( EXPR ) VIRGULEEXPRETOILE OPTERMETOILE
|    caractere val EXPR OPTERMETOILE
|    new IDENT OPTERMETOILE .

VIRGULEEXPRETOILE -> virgule EXPR VIRGULEEXPRETOILE2
    | .

VIRGULEEXPRETOILE2 -> virgule EXPR VIRGULEEXPRETOILE2
    | .
    
INSTR -> ACCES deuxpointsegal EXPR pointvirgule 
    | return EXPRINTER pointvirgule 
    |   IDENT EXPRPARENTHETOILE pointvirgule 
    | BEGIN 
    | IF 
    | FOR 
    | WHILE .

EXPRINTER -> EXPR
    | .

 EXPRPARENTHETOILE -> ( EXPR ) EXPRPARENTHETOILE2
    | .

EXPRPARENTHETOILE2 -> ( EXPR ) EXPRPARENTHETOILE2
    | .

INSTRPLUS -> INSTR INSTRPLUS2 .


INSTRPLUS2 -> INSTR INSTRPLUS2 
    | .

BEGIN -> begin INSTRPLUS end .

IF -> if EXPR then INSTRPLUS IF_TAIL .

IF_TAIL -> elsif EXPR then INSTRPLUS IF_TAIL 
    | INSTRPLUSELSEINTER end if .

INSTRPLUSELSEINTER -> else INSTRPLUS
    | .

FOR -> for IDENT in REVERSEINTER EXPR troispoints EXPR loop INSTRPLUS end loop pointvirgule .

REVERSE -> reverse .

REVERSEINTER -> REVERSE
    | .

WHILE -> while EXPR loop INSTRPLUS end loop .

CHAMPS -> IDENT IDENTVIRGULEETOILE : TYPE pointvirgule pointvirgule .

IDENTVIRGULEETOILE -> virgule IDENT IDENTVIRGULEETOILE2
    | .

IDENTVIRGULEETOILE2 -> vigule IDENT IDENTVIRGULEETOILE2
    | .

CHAMPSPLUS -> CHAMPS CHAMPSPLUS2 .

CHAMPSPLUS2 -> CHAMPS CHAMPSPLUS2
    | .

TYPE -> IDENT 
    | access IDENT .

PARAMS -> ( PARAM PARAMVIRGULEETOILE ) .

PARAMVIRGULEETOILE -> virgule PARAM PARAMVIRGULEETOILE2
    | .

PARAMVIRGULEETOILE2 -> virgule PARAM VIRGULEEXPRETOILE2
    | .

PARAMSINTER -> PARAMS  
    | .

PARAM -> IDENT IDENTVIRGULEETOILE : MODEINTER TYPE .

MODEINTER -> MODE
    | .


MODE -> in 
    | in out .

OP -> equal 
    | different 
    | inferior 
    | inferioregal 
    | superior 
    | superioregal 
    | plus 
    | moins 
    | mult 
    | division 
    | rem 
    | and 
    | and then 
    | or 
    | or else .

ACCES -> IDENT 
    | EXPR point IDENT .

IDENT -> ident .

IDENTINTER -> IDENT
    | .
