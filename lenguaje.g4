grammar lenguaje;

programa
    : main EOF
    ;

main
    : 'Main' '|:' instruccion* ':|'
    ;

instruccion
    : ID INT
    | '(:)' NOTA=INT
    ;

ID  : [a-zA-Z]+ ;
INT : [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
// Ignorar comentarios de doble barra
COMMENT : '//' ~[\r\n]* -> skip ;