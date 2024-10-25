grammar oos;

startRule
        :   classes
        ;

classes
        :   class_def*
            class_main_def
            EOF
        ;

class_def
        :   'class' class_name ( 'inherits' class_name (',' class_name  )*  )? ':'
            declarations
            class_body
        ;

class_main_def
        :   'class' ('main' | 'Main') ':'
            declarations
            main_body
        ;

class_name
        : ID
        ;

declarations
        :   (decl_line (';' decl_line)* ';'';')?
        ;

class_body
        :   (constructor_def ';'';')+
            (method_def ';'';')*
        ;

main_body
        :   method_main_def ';'';'
        ;

decl_line
        :   types ID  (',' ID  )*
        ;

constructor_def
        :   'def' '__init__' parameters ':' class_name
            declarations
            method_body
        ;

method_def
        :   'def' ID parameters ':' ('int' | '-' | class_name)
            declarations
            method_body
        ;

method_main_def
        :   'def' 'main' '(' 'self' ')' ':' '-'
            declarations
            method_body
        ;

types
        :   class_name
        |   'int'
        ;

parameters
        :   '(' parlist ')'
        ;

method_body
        :   declarations
            (statements)?
        ;

return_type
        :   types
        |   '-'
        ;

parlist
        :   'self'
            (',' types ID )*
        ;

statements :   statement (';' statement )*
        ;


statement
        :   assignment_stat
        |   direct_call_stat
        |   if_stat
        |   while_stat
        |   return_stat
        |   input_stat
        |   print_stat
        ;

assignment_stat
        :   ('self.')? ID '=' expression
        |   constructor_call
        ;

direct_call_stat
        :   ('self.')? ID '.' func_call
        |   ('self.')? func_call
        ;

if_stat
        :   'if' '(' condition ')' ':'
            (statements ';' )?
            else_part
            'endif'
        ;

else_part
        :   'else' ':'
            ( statements ';' )?
        |
        ;

while_stat
        :   'while' '(' condition ')' ':'
            ( statements )?
            'endwhile'
        ;

return_stat
        :   'return' ('self' | 'self.'ID | expression)
        ;

input_stat
        :   'input' ('self.')? ID
        ;

print_stat
        :   'print' expression (',' expression)*
        ;

expression
        :   optional_sign term (add_oper term )*
        ;

arguments
        :   '(' arglist ')'
        ;

condition
        :   boolterm
            ('or' boolterm )*
        ;

optional_sign
        :   add_oper
        |
        ;

term
        :   factor  ( mul_oper factor )*
        ;

add_oper
        :   '+'
        |   '-'
        ;

arglist
        :   argitem (',' argitem )*
        |
        ;

boolterm
        :   boolfactor ( 'and' boolfactor )*
        ;

factor
        :   INTEGER
        |   '(' expression ')'
        |   ('self.')? ID
        |   ('self.')? ID '.' func_call
        |   ('self.')? func_call
        |   ID.ID
        |   ID
        ;

mul_oper
        :   '*'
        |   '/'
        ;

argitem
        :   expression
        ;

boolfactor
        :   'not' '[' condition ']'
        |   '[' condition ']'
        |   expression rel_oper expression
        ;

func_call
        :   ID arguments
        ;

constructor_call
        :   class_name
            arguments
        ;

rel_oper
        :  '=='
        |   '<='
        |   '>='
        |   '>'
        |   '<'
        |   '!='
        ;

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------

WS: [ \t\r\n]+ -> skip;
COMMENTS: '#' ~[#]* '#' -> skip;
ID: ID_START (ID_CONTINUE)*;
INTEGER: NON_ZERO_DIGIT (DIGIT)* | '0'+;


fragment ID_START
        : [A-Z]
        | [a-z]
        ;

fragment ID_CONTINUE
        : '_'
        | [A-Z]
        | [a-z]
        | [0-9]
        ;


fragment NON_ZERO_DIGIT
        : [1-9]
        ;

fragment DIGIT
        : [0-9]
        ;


