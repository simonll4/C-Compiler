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
MENORIGUAL: '<=';
MAYORIGUAL: '>=';
AND: '&&';
OR: '||';
MAS : '+';
MENOS : '-';
MULTIPLICACION : '*';
DIVISION : '/';
MODULO : '%';

INT : 'int';
DOUBLE:'double' ;

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

lista_var : COMA ID definicion lista_var
          |
          ;

definicion : EQ opal
           |
           ;

asignacion : ID EQ opal;

tipo_dato : INT 
          | DOUBLE
          ;

bloque : LLA instrucciones LLC;

if_stmt : IF PA opal PC instruccion | IF PA opal PC instruccion else_stmt;

else_stmt : ELSE bloque
          ;

for_stmt : FOR PA asignacion PYC opal PYC asignacion PC instruccion;

while_stmt : WHILE PA opal PC instruccion ;

retornar : RETORNO opal;

opal : expresionl;

expresionl : terminol expl;

expl : OR terminol expl
     |;

terminol : expresion terml | expresion cmp expresion terml;

terml : AND expresionl terml
      |;

expresion : termino exp;

exp : MAS   termino exp
    | MENOS termino exp
    |
    ;

termino : factor term ;

term : MULTIPLICACION factor term
     | DIVISION  factor term    
     | MODULO  factor term
     |
     ;

factor : ID
       | NUMERO
       | llamada_funcion
       | MENOS NUMERO
       | MENOS ID
       | PA expresionl PC
       ;

prototipo_funcion : tipo_dato ID PA args_recibido PC;

funcion : tipo_dato ID PA args_recibido PC bloque ;

args_recibido : tipo_dato ID lista_args_recibido
              |;

lista_args_recibido : COMA tipo_dato  ID lista_args_recibido
            | ;

llamada_funcion : ID PA args_enviado PC;

args_enviado : expresion lista_args_enviado
             |;

lista_args_enviado: COMA expresion lista_args_enviado
                  |;

cmp : MAYOR 
    | MENOR 
    | IGUAL
    | MENORIGUAL
    | MAYORIGUAL 
    | DISTINTO ;