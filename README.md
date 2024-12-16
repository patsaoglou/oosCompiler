# OOS Compiler Project
In this repository, I share a compiler project I've made under the Compilers 2 course (Prof. George Manis). This repository demonstrates the workflow 
of using ANTLR (Another Tool for Language Recognition) to define, parse, and process custom languages. The goal is to illustrate the end-to-end process 
of working with ANTLR, from grammar creation to generating outputs based on parsed input. 

A initial grammar file what given to us and we had to implement the listeners 
that are called once a known grammar structure was recognised by the ANTLR generated lexer and parser. The structure was then used by using the recognised tokens to save the necessary 
information into a symbol table structure and generate the final C code once information was enough. 

## How ANTLR works
1. **Defining the Grammar:** begin by writing a grammar file (*.g4) to define the structure and rules of your language. This includes both lexical rules (tokens) and parser rules.
2. **Generating Lexer and Parser:** Use ANTLR to generate the source code for the lexer, parser, and optional tree traversal classes (listeners or visitors) in the programming language of your choice.
3. **Parsing Input:** provide the input to the generated parser. The lexer tokenizes the input, and the parser organizes the tokens into a parse tree according to the grammar rules.
4. **Tree Traversal:** implement custom logic using the generated listener or visitor classes to traverse the parse tree. This step allows you to process the input meaningfully, such as evaluating expressions or transforming code.
5. **Producing the Output:** based on the traversal, generate the final output, which can be a computed result, transformed data, or any custom representation.

## High-Level OOS code logic
OOS folows Python's Object Oriented approach where classes can be defined. Classes can encapsulate field of type 'int' or class objects. At least one constructor must also
be implemented and called at the final code so the object is initialized by reserving the necessary heap space. 

Method can also be implemented within a class where the given class object 'self' must be passed to link the relation between the class and the method but also in order to be able to perform object manipulation. 

Method within a class can also be overloaded if parameter number is different. OOS supports inheritage where a class can inherit fields and methods from the parent class like they are defined within the class.

## OOS Grammar Structure - ANTLR
ANTLR uses context-free grammar to define the structure of the language. A grammar in ANTLR is defined in the .g4 file, which consists of:
1. **Lexer Rules:** defines how to tokenize the input string into meaningful pieces (tokens).

```g4
    WS: [ \t\r\n]+ -> skip;
    COMMENTS: '#' ~[#]* '#' -> skip;
    ID: ID_START (ID_CONTINUE)*;
    INTEGER: NON_ZERO_DIGIT (DIGIT)* | '0'+;
```
2. **Parser Rules:** defines how tokens are grouped into higher-level constructs (syntax trees).

```g4
    statement
        :   assignment_stat
        |   direct_call_stat
        |   if_stat
        |   while_stat
        |   return_stat
        |   input_stat
        |   print_stat
        ;

    direct_call_stat
        :   ('self.')? ID '.' func_call
        |   ('self.')? func_call
        ;
```

## OOS Symbol Table Structure - ANTLR
A symbol table structure had to be implemented to do the necessary checks if the code recognised by the parser was valid. The stucture had to save 
information about the class field definitions, the classes of which it inherites from, the defined constructors and methods. 

The symbol table had to also keep track of the versions of the methods implemented so method overriding was possible. Lastly the symbol table was important for searching if a method or class 
field seen by the parser was defined in a given class or by inherited classes the programmer specified in the declaration. 

The **def search_method_in_inherited_classes(self, method_name, param_num)** defined in the **symbolTable.py** for example was responsible to search for method not found in the class specified in the oos source code (self parameter) to be searched the inherited class structures saved in the **self.inherits_from = []** in the **class_info** class of the symbol table.

The information structure saved by the symbol table can be summarized here:

```sym
    Class name: Shape
    Fields: [x: int, y: int, color: int]
    Inherits from: []
    Methods:
        Method name: Shape
        Fields: [self: Shape, x: int, y: int]
        Parameter num: 3
        Version: 1
        Returns: Shape
        Constructor: True
    
        Method name: Shape
        Fields: [self: Shape, x: int, y: int, color: int]
        Parameter num: 4
        Version: 2
        Returns: Shape
        Constructor: True

    Class name: Square
    Fields: [side: int]
    Inherits from: [Shape]
    Methods:
        Method name: Square
        Fields: [self: Square, side: int]
        Parameter num: 2
        Version: 1
        Returns: Square
        Constructor: True
    
        Method name: get_side
        Fields: [self: Square]
        Parameter num: 1
        Version: 1
        Returns: int
        Constructor: False
```

## From OOS to C source
The final conversion of a given OOS source file to the final C source follows the procedure bellow:
- **Class fields** specified on the OOS source are saved in **typedef struct** of the class name.
```C
typedef struct Shape 
{
	int x, y;
	int color;
} Shape;
```
- **Class Inheritage** was implemented by saving the class struct of the parent class as a field to the child's struct
so field space can be reserved during initialization of the object and the object field can be passed when a parent method is called.
```C
typedef struct Square 
{
	Shape Shape$self;
	int side;
} Square;
```
- **Class Objects** on OOS are **struct pointers** in C and not the actual structs so object references are possible and object assignment can happen. If the 
actual struct was used in the field declaration when a object assignment is happening, then the values of the struct would copy to the other struct and we would not have
the actual reference of the object in C and any changes happening during a method call would not change the initial object.

```OOS
    Circle c;
    Square s;
```

```C
	struct Circle *c = NULL;
	struct Square *s = NULL;
```

- **Class Constructor** uses the **malloc** system call to reserve heap space equal to the size of the struct object and return the virtual address memory space to the object's pointer.

```C
Square* Square$1$init(Square *self$, int side)
{
	if(self$ == NULL)
	{
		self$ = (Square *)malloc(sizeof(Square));
	}

	self$ -> side = side;

	return self$;
}
```

- **Method calls** inherited by parent classes are happening by passing the address of the object declared within the child's struct. In the example below we can see how the **SquareWithCirclesOnCorners**
uses methods declared in the classes that it inherits from:

```C
typedef struct SquareWithCirclesOnCorners 
{
	Square Square$self;
	Circle Circle$self;
} SquareWithCirclesOnCorners;

int area$3(SquareWithCirclesOnCorners *self$)
{
	int int_pi;
	int_pi = 3;
	return get_side$1(&self$ -> Square$self) * get_side$1(&self$ -> Square$self) + 
        3 * int_pi * get_radius$1(&self$ -> Circle$self) * get_radius$1(&self$ -> Circle$self);

}
```

## Improvements and additions
1. The code i've posted cannot support more depth = 1 inheritage since the grammar does not support it and also the search functions
might not return the correct value at the end (compiler it might crash too :-).
2. Since dynamic allocation is used, it is possible to implement automatic deallocation by implenting destructors under the hood that call 
free() with the actual object's pointer. This can happen by the symbol table keeping track of the references in OOS/pointers in C pointing into a given 
structure and invoking the destructor method once no more references/pointers hold the object.

# Disclaimers
This compiler has no point to be used and is nowhere near of correctly compiling code in general. It was made for educational and experimentation purposes to learn
about the ANTLR framework and under semester workload trying to finish within the deadline and delivering optimal result. :-)

