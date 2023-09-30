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
INCREMENTO : '++';
DECREMENTO : '--';
MENOR: '<';
MAYOR: '>';
IGUAL: '==';
DISTINTO: '!=';
AND: '&&';
OR: '||';

TDATO : 'int' | 'double' ;
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
            | bloque
            ;

declaracion : TDATO ID definicion lista_var ;

definicion : EQ NUMERO
           |
           ;

lista_var : COMA ID definicion lista_var
          |
          ;

asignacion : ID EQ NUMERO;

bloque : LLA instrucciones LLC ;

retornar : RETORNO ID | RETORNO NUMERO;

if_stmt : IF PA opal PC instruccion | IF PA opal PC instruccion else_stmt;

else_stmt : ELSE bloque;

for_stmt : FOR PA (declaracion | asignacion ) PYC opal PYC ID (INCREMENTO | DECREMENTO) PC instruccion;

while_stmt : WHILE PA opal PC instruccion ;


opal : comp | comp AND opal | comp OR opal;

comp : ID MAYOR NUMERO
    | ID MENOR NUMERO
	| ID IGUAL NUMERO
	| ID DISTINTO NUMERO
    | NUMERO MAYOR NUMERO
	| NUMERO MENOR NUMERO
	| NUMERO IGUAL NUMERO
	| NUMERO DISTINTO NUMERO
    | NUMERO MAYOR ID
	| NUMERO MENOR ID
	| NUMERO IGUAL ID
	| NUMERO DISTINTO ID
	| ID MAYOR ID
	| ID MENOR ID
	| ID IGUAL ID
	| ID DISTINTO ID
	;
