grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

EQ : '=' ;
PA : '(' ;
PC : ')' ;
LLA : '{' ;
LLC : '}' ;
PYC : ';' ;
COMA : ',' ;

MENOR: '<';
MAYOR: '>';
IGUAL: '==';
DISTINTO: '!=';
AND: '&&';
OR: '||';
MAS : '+';
MENOS : '-';
MULTIPLICACION : '*';
DIVISION : '/';
MODULO : '%';

INT : 'int';
FLOAT: 'float';
DOUBLE:'double' ;
CHAR : 'char';

WHILE : 'while' ;
FOR : 'for';
IF : 'if';
ELSE : 'else';
RETORNO : 'return';

NUMERO : DIGITO+ ;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
WS : [ \t\r\n] -> skip ;
OTRO : . ;

programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
              ;

instruccion : declaracion PYC
            | asignacion PYC
            | retornar PYC
            | if_stmt
            | for_stmt
            | while_stmt
            | prototipo_funcion PYC
            | funcion
            | llamada_funcion PYC
            | bloque
            ;

declaracion : tipo_dato ID definicion lista_var ;

definicion : EQ NUMERO
           |
           ;

lista_var : COMA ID definicion lista_var
          |
          ;

asignacion : ID EQ opal | ID EQ llamada_funcion;

tipo_dato : INT 
          | FLOAT 
          | DOUBLE 
          | CHAR;

bloque : LLA instrucciones LLC;

if_stmt : IF PA opal PC instruccion | IF PA opal PC instruccion else_stmt;

else_stmt : ELSE bloque;

for_stmt : FOR PA asignacion PYC opal PYC ID asignacion PC instruccion;

while_stmt : WHILE PA opal PC instruccion ;

retornar : RETORNO opal;

cmp : MAYOR 
    | MENOR 
    | IGUAL 
    | DISTINTO ;

opal : expresion;

expresion : termino exp | terminol expl;

expl: OR terminol expl
    |;

terminol: factor terml;

terml : AND factor terml
    | ;

exp : MAS   termino exp
    | MENOS termino exp
    |
    ;

termino : factor term | factor cmp expresion;

term : MULTIPLICACION factor term
     | DIVISION  factor term    
     | MODULO  factor term
     |
     ;

factor : NUMERO
       | funcion
       | ID
       | MENOS NUMERO
       | MENOS ID
       | PA expresion PC
       ;

prototipo_funcion : tipo_dato ID PA args PC;

funcion : tipo_dato ID PA args PC bloque ;

llamada_funcion : ID PA expresion PC;

args : tipo_dato ID lista_args
     |;

lista_args : COMA tipo_dato  ID lista_args
            | ;
