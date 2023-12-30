# LOXLANG
This is an implementation of the Lox Language in Python. The lox language is the language developed in the excellent book [Crafting Interpreters](https://www.craftinginterpreters.com/). 

## Requirements 
Nothing really. Unit tests are all written with the `unittest` module.


## Grammar
The grammar at the time of writing is 


`program -> declaration | eof;`

`declaration -> var_decl | statement;`

Later we will have seperate declarations for functions. For now 

`var_decl -> "var" IDENTIFIER { "=" expression }? ";"`
`statement -> expr_stmt | print_stmt; `
`expr_stmt -> expression ";"`
`print_stmt -> "print" expression ";"`


Stratified part of grammar in order of precedence. Note that we choose not to use 
left recursive rules like `factor -> factor ( "/" | "*" ) unary | unary` as the 
parsing technique in the book doesn't work well with left-recursive grammars.

`expression -> equality`
`equality -> comparison ( ( "!=" | "==" ) comparison )*`
`comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*`
`term -> factor ( ( "+" | "-" ) factor )*`
`factor -> unary ( ( "/" | "*" ) unary )*`
`unary -> ( "!" | "-" ) unary | primary`

`primary -> "true" | "false" | "nil" | NUMBER | STRING 
            | "(" expression ")" | IDENTIFIER ;`

