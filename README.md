

## Requirements 
Despite hating it I've decided to use `poetry` for dependencies. To install do

`poetry install` 

Optionally append `-vv` to see things scrolling, perhaps this can assure you that poetry 
is actually doing something. Activate the environment with 

`source $(poetry env info -p)/bin/activate`. 

Activating puts the symbol `deactivate` in the shell which deactivates the environment.

Note that you may need to export a null keyring to get poetry to install stuff without
hassling you about creating `kdewallet` or similar. To do this run

`export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring`

I thought this may have been patched out (to be honest I didn't keep up with this issue)
but in poetry `1.7.1` I still have to do this sometimes.


## Grammar

### Statements
The statement grammar at the time of writing is 

-`program -> declaration | eof;`
-`declaration -> class_decl | func_decl | var_decl | statement;`
-`class_decl -> "class" IDENTIFIER ( "<" IDENTIFIER )?  "{" function* "}";`
-`func_decl -> "func" function;`
-`function -> IDENTIFIER "(" parameters? ")" block;`
-`parameters -> IDENTIFIER ( "," IDENTIFIER* ")";`
-`var_decl -> "var" IDENTIFIER { "=" expression }? ";"`
-`statement -> expr_stmt | for_stmt | if_stmt | print_stmt | return_stmt | while_stmt | block; `
-`expr_stmt -> expression ";"`
-`for_stmt -> "(" ( var_decl | expr_stmt | ";" ) expression? ";" expression ";" ")" statement;`  (Desugared to while loop)
-`if_stmt -> "(" expression ")" statment "else" statement ")"?;`
-`return_stmt -> "return" expression? ";"`
-`print_stmt -> "print" expression ";"`
-`while_stmt -> "while" "(" expression ")" statement;`
-`block -> "{" declaration* "};"`


### Stratified part of grammar in order of precedence. 

Note that we choose not to use 
left recursive rules like `factor -> factor ( "/" | "*" ) unary | unary` as the 
parsing technique in the book doesn't work well with left-recursive grammars.

Short-circuit logic is implemented in the grammar as a low-precedence production.

Function calls are implemented in the grammar as a high-precedence operator `()` 
that matches a `primary` expression followed by zero or more function calls.

- `expression -> assignment;`
- `assignment -> ( call "." )? IDENTIFIER "=" assignment | logic_or;`
- `logic_or -> logic_and ( "or" logic_and )*;`
- `logic_and -> equality ( "and" equality )*;`
- `equality -> comparison ( ( "!=" | "==" ) comparison )*;`
- `comparison -> term ( ( ">" | ">=" | "<" | "<=" ) term )*;`
- `term -> factor ( ( "+" | "-" ) factor )*;`
- `factor -> unary ( ( "/" | "*" ) unary )*;`
- `unary -> ( "!" | "-" ) unary | call;`
- `call -> primary ( "(" arguments? ")" | "." IDENTIFIER )*;`
- 
- `primary -> "true" | "false" | "nil" | NUMBER | STRING 
            | IDENTIFIER | "(" expression ")" 
            | "super" "." IDENTIFIER ;`


Function arguments have the grammar 

- `arguments -> expression ( "," expression )*;`


## TODOs:
- Implement `break` statement. Syntax for `break` is the keyword "`break`" followed by "`;`". 
- The `break` keyword causes execution to jump to the end of the nearest enclosing loop.
- Implement static methods on classes. Do this by adding the `class` keyword to the start of a class method. Hint: make `LoxClass` extend `LoxInstance`.
