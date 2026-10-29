grammar lenguaje;

programa
    : main* EOF
    ;

main
    : ID '|:' instruccion* ':|'
    ;

instruccion
    : ID INT
    | '(:)' NOTA=INT
    ;

ID : [a-zA-Z]+ ;
INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;