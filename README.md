# Fynk

## Grammer
```
factor -> INT | FLOAT | STRING | BOOL | IDENTIFIER | '(' expr ')' | increment | decrement
term -> factor *('*' | '/') factor)*
expr -> term (('+' | '-') term)*

expr_stmt -> expr ';'

increment -> IDENTIFIER '++' | '++' IDENTIFIER
decrement -> IDENTIFIER '--' | '--' IDENTIFIER

increment_stmt -> increment ';'
decrement_stmt -> decrement ';'

assignment -> IDENTIFIER '=' expr
assignment_stmt -> assignment ';

eq -> expr '==' expr
eq_stmt -> eq ';'

ieq -> expr '!=' expr
ieq_stmt -> ieq ';'
```