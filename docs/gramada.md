# Grammaire Ada

$€ = \epsilon$

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