# LOXLANG
This is an implementation of the Lox Language in Python. The lox language is the language developed in the excellent book [Crafting Interpreters](https://www.craftinginterpreters.com/). 

## Requirements 
Despite hating it I've decided to use `poetry` for dependencies. To install do

`poetry install` 

Optionally append `-vv` to see things scrolling, perhaps this can assure you that poetry is actually doing something.

Activate the environment with `source $(poetry env info -p)/bin/activate`. Deactivate with `deactivate`.


## Grammar

### Statements
The statement grammar at the time of writing is 

`program -> declaration | eof;`
`declaration -> var_decl | statement;`
`var_decl -> "var" IDENTIFIER { "=" expression }? ";"`
`statement -> expr_stmt | for_stmt | if_stmt | print_stmt | while_stmt | block; `
`expr_stmt -> expression ";"`
`for_stmt -> "(" ( var_decl | expr_stmt | ";" ) expression? ";" expression ";" ")" statement;`  (Desugared to while loop)
`if_stmt -> "(" expression ")" statment "else" statement ")"?`
`print_stmt -> "print" expression ";"`
`while_stmt -> "while" "(" expression ")" statement`
`block -> "{" declaration* "}"`


### Stratified part of grammar in order of precedence. 

Note that we choose not to use 
left recursive rules like `factor -> factor ( "/" | "*" ) unary | unary` as the 
parsing technique in the book doesn't work well with left-recursive grammars.

Short-circuit logic is implemented in the grammar as a low-precedence production.

`expression -> assignment`
`assignment -> IDENTIFIER "=" assignment | logic_or`
`logic_or -> logic_and ( "or" logic_and )*`
`logic_and -> equality ( "and" equality )*`
`equality -> comparison ( ( "!=" | "==" ) comparison )*`
`comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*`
`term -> factor ( ( "+" | "-" ) factor )*`
`factor -> unary ( ( "/" | "*" ) unary )*`
`unary -> ( "!" | "-" ) unary | primary`

`primary -> "true" | "false" | "nil" | NUMBER | STRING 
            | "(" expression ")" | IDENTIFIER ;`


## TODOs:
- Implement `break` statement. Syntax for `break` is the keyword "`break`" followed by "`;`". 
- The `break` keyword causes execution to jump to the end of the nearest enclosing loop.
