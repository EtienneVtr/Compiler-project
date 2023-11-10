# Grammaire Ada

Epsilon : €

```
<fichier>   ->  with Ada.Text_IO; use Ada.Text_IO;
                procedure <ident> is <decl>*
                begin <instr>+ end <ident>? ; EOF

<decl>      ->  type <ident> <D>;| <procedure> | <function>
<D>         ->  is <D'> | €
<D'>        ->  access <ident> | record <champs>+ end record;

<procedure> ->  procedure <ident> <params>? is <decl>*
                begin <instr>+ end <ident>?;

<func>      ->  function <ident> <params>? return <type> is <decl>*
                begin <instr>+ end <ident>?;

<expr>      ->  <entier> | <caractère>  | true | false | null 
            |   <accès>  | <E>  | new <ident>
<E>         ->  <expr><op><expr> | not <expr> | -<expr>
            |   <ident> (<expr>+,)  | character ' val (<expr>)

<instr>     ->  <accès> := <expr>; | return <expr>? ;
            |   <ident> <I>; | <begin> | <if> | <for> | <while>
<I>         ->  (<expr>+,) | €

<begin>     ->  begin <instr>+ end;

<if>        ->  if <expr> then <instr>+ <if_tail>
<if_tail>   ->  elsif <expr> then <instr>+ <if_tail>
            |   (else <instr>+)? end if;


<for>       ->  for <ident> in reverse? <expr>...<expr>
                loop <instr>+ end loop;

<while>     ->  while <expr> loop <instr>+ end loop;

<champs>    ->  <ident>+, : <type>;
<type>      ->  <ident> | access <ident>
<params>    ->  (<param>+;)
<param>     ->  <ident>+, : <mode>? <type>
<mode>      ->  in | in out

<op>        ->  = | /= | < | <= | > | >= | + | - | * | / | rem | and | and then | or | or else

<accès>     ->  <ident> | <expr>.<ident>

<ident>     ->  <caractère> | <caractère><ID>
<ID>         ->  <entier><ID> | <charactère><ID> | _<ID> | €
```


# Pour tester avec le site 
Modèle à suivre : grammar ('' is ε):
E -> T E'
E' -> + T E'
E' -> ''
T -> F T'
T' -> * F T'
T' -> ''
F -> ( E )
F -> id
 
________________________________________________________________________________________



FICHIER -> with Ada.Text_IO; use Ada.Text_IO; procedure ident is DECL* begin INSTRUCTION+ end ident? ; EOF

DECL -> type ident D;
DECL -> PROCEDURE
DECL -> FUNCTION

D -> is DPRIME
D -> ''

DPRIME -> access ident 
DPRIME -> record CHAMPS+ end record;

PROCEDURE -> procedure ident PARAMS? is DECL* begin INSTRUCTION+ end ident?;

FUNCTION -> function ident PARAMS? return TYPE is DECL* begin INSTRUCTION+ end ident?;

EXPR -> <entier> 
EXPR -> <caractère> 
EXPR -> true
EXPR -> false
EXPR -> null 
EXPR -> ACCES
EXPR -> E 
EXPR -> new ident

E -> EXPR OP EXPR
E -> not EXPR
E -> -EXPR
E -> ident (EXPR+,)
E -> character ' val (EXPR)

INSTRUCTION -> ACCES := EXPR;
INSTRUCTION -> return EXPR? ;
INSTRUCTION -> ident I;
INSTRUCTION -> BEGIN
INSTRUCTION -> IF 
INSTRUCTION -> FOR
INSTRUCTION -> WHILE

I -> (EXPR+,)
I -> ''

BEGIN -> begin INSTRUCTION+ end;

IF -> if EXPR then INSTRUCTION+ IFTAIL

IFTAIL -> elsif EXPR then INSTRUCTION+ IFTAIL
IFTAIL -> (else INSTRUCTION+)? end if;


FOR -> for ident in reverse? EXPR...EXPR loop INSTRUCTION+ end loop;

WHILE -> while EXPR loop INSTRUCTION+ end loop;

CHAMPS -> ident+, : TYPE;

TYPE -> ident
TYPE -> access ident

PARAMS -> (PARAM+;)

PARAM -> ident+, : MODE? TYPE

MODE -> in
MODE -> in out

OP -> =
OP -> /=
OP -> <
OP -> <=
OP -> > 
OP -> >=
OP -> +
OP -> -
OP -> *
OP -> /
OP -> rem
OP -> and
OP -> and then
OP -> or
OP -> or else

ACCES -> ident
ACCES -> EXPR.ident
