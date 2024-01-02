# LOXLANG
This is an implementation of the Lox Language in Python. The lox language is the language developed in the excellent book [Crafting Interpreters](https://www.craftinginterpreters.com/). 

## Requirements 
Despite hating it I've decided to use `poetry` for dependencies. To install do

`poetry install` 

Optionally append `-vv` to see things scrolling, perhaps this can assure you that poetry is actually doing something.

Activate the environment with `source $(poetry env info -p)/bin/activate`. Deactivate with `deactivate`.


## Grammar
The grammar at the time of writing is 

`program -> declaration | eof;`

`declaration -> var_decl | statement;`

Later we will have separate declarations for functions. For now 

`var_decl -> "var" IDENTIFIER { "=" expression }? ";"`
`statement -> expr_stmt | print_stmt | if_stmt | block; `
`if_stmt -> "(" expression ")" statment "else" statement ")"?`
`block -> "{" declaration* "}"`
`expr_stmt -> expression ";"`
`print_stmt -> "print" expression ";"`


Stratified part of grammar in order of precedence. Note that we choose not to use 
left recursive rules like `factor -> factor ( "/" | "*" ) unary | unary` as the 
parsing technique in the book doesn't work well with left-recursive grammars.

`expression -> assignment`
`assignment -> IDENTIFIER "=" assignment | equality`
`equality -> comparison ( ( "!=" | "==" ) comparison )*`
`comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*`
`term -> factor ( ( "+" | "-" ) factor )*`
`factor -> unary ( ( "/" | "*" ) unary )*`
`unary -> ( "!" | "-" ) unary | primary`

`primary -> "true" | "false" | "nil" | NUMBER | STRING 
            | "(" expression ")" | IDENTIFIER ;`

