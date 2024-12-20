from oosListener import oosListener
from oosParser import oosParser
from symbolTable import *


class oosListenerImplementation(oosListener):

    def __init__(self):
        self.class_entries = {}

        self.global_method_versions = {}

        self.output = []
        self.known_classes = []
        self.last_class_struct = None
        self.last_method_def = None
        self.last_method_obj = None
        self.in_constructor = False
        self.parenthesis_stack = []
        self.last_assignment_type = None #  this is used so i can check if assignement is same type as declaration
        self.in_struct = False
        
        #   used for expression
        self.expression_stack = []
        self.function_stack = []

        self.function_obj_stack = []

        self.current_expression = ""
        self.current_function = ""
        self.boolfactor_count = 0
        self.boolterm_count = 0

        self.print_expression_list = None
        self.in_relop = False
        self.in_boolterm = False

        self.id_list = []
        self.types_list = []
        self.last_type= None

        self.parlist = []
        self.actual_pars = []

        self.tabs = 0

        self.function_call_param_num = 0 
        self.function_call_param_num_stack = []
        self.function_class_stack = []

    def search_actual_class_method(self, class_name, method_name, param_num):
        class_obj = self.get_class_obj(class_name)
        ver_class = class_obj.search_method(method_name, param_num)

        return ver_class
        

    def tabbing(self):
        return self.tabs * "\t"

    def indent(self):
        self.tabs = self.tabs + 1

    def deindent(self):
        self.tabs = self.tabs - 1

    def add_class(self, class_name):
        new = class_info(class_name)
        if isinstance(new, class_info):
            self.class_entries[new.name] = new
        return new
    
    def add_field_to_class(self, class_name, field_name, field_type):
        class_obj = self.class_entries.get(class_name)
        if (class_obj):
            class_obj.add_field(field_name, field_type)
        else:
            print("adding field to class that does not exist.")
            exit(0)

    def add_field_to_class_method(self, class_name, method_obf, field_name, field_type, is_param = False):
        class_obj = self.class_entries.get(class_name)
        
        if (class_obj):
            class_obj.add_field_to_method(method_obf, field_name, field_type, is_param)
        else:
            print("add_field_to_class_method to class that does not exist.")
            exit(0)

    def add_method_to_class(self, class_name, method_name, is_constructor = False, return_type =None):
        class_obj = self.class_entries.get(class_name)
        method = class_obj.add_method(method_name, is_constructor, return_type, self.global_method_versions)
        self.last_method_obj = method[1]
        return method[0]

    def get_class_obj(self, class_name):
        class_obj = self.class_entries.get(class_name)
        
        if class_obj is None:
            print(f"Class with class name '{class_name}' is not defined")
            exit(0)
        
        return class_obj

    def has_class_field(self, class_name, field_name):
        class_obj = self.get_class_obj(class_name)
        
        if (class_obj):
            bool_class = class_obj.has_field(field_name)
            if (bool_class[0]):
                return bool_class
            else:
                
                print(f"Class '{class_name}' does not have field '{field_name}' declared")
                exit(0)
    
    def get_class_field_type(self, class_name, field_name):
        return self.get_class_obj(class_name).get_field_type(field_name)
    
    def get_method_field_type(self, field_name):
        return self.last_method_obj.get_field_type(field_name)

    # returns type of the id and class object of the the declaration used to get .
    def chech_if_id_declared(self, id, is_self = False):
        if self.last_class_struct == "main" or is_self:
            bool_class = self.has_class_field(self.last_class_struct, id)
            if bool_class[0] == True:
                
                return [self.get_class_field_type(bool_class[1].name, id), bool_class[1]]
            else:
                print(f"Field with name '{id}': int not declared in scope of {self.last_method_obj.get_name()}")
                exit(0)
        elif self.last_method_obj.has_field(id) == True:
            return [self.get_method_field_type(id), None]
        else:
            print(f"Field with name '{id}': int not declared in scope of {self.last_method_obj.get_name()}")
            exit(0)
            
    def check_if_overide_methods_valid(self, class_name, method_object):
        class_obj = self.get_class_obj(class_name)
    
        class_obj.check_if_overide_methods_valid( method_object)        


    #  get C sources and Symbolic table file
    def get_oos_compiled(self):
        compiled_content = "".join(self.output)
        
        with open(f"out.c", "w") as file:
            file.write(compiled_content)
        
        return compiled_content
    
    def get_symb_structure(self):        
        symb_str = ""
        
        for class_name, class_entry in self.class_entries.items():
            symb_structure = class_entry.__str__()

            symb_str += symb_structure

            symb_str += "\n\n" + 50*"+" + "\n\n" 

        with open(f"out.sym", "w") as file:
            file.write(symb_str)
        
        return symb_str

    # --------------------------------------------

    def enterStartRule(self, ctx:oosParser.StartRuleContext):
        # adding necessary C includes
        self.output.append(f"#include <stdio.h>\n")
        self.output.append(f"#include <stdlib.h>\n")

    # --------------------------------------------

    def enterClass_def(self, ctx:oosParser.Class_defContext):
        class_name = ctx.class_name(0).ID().getText()
        self.last_class_struct = class_name

        self.output.append(f"\ntypedef struct {self.last_class_struct} \n{{")
        self.in_struct = True
        self.indent()
        self.known_classes.append(f"{self.last_class_struct}")
        self.output.append("\n")
        new_class = self.add_class(class_name)

        if ctx.getChildCount() > 2 and ctx.getChild(2).getText() == "inherits":
            for class_name in ctx.class_name()[1::]:
                name = class_name.getText()
                
                
                
                if name in self.known_classes[:-1]:
                    new_class.add_inheritage_class(self.get_class_obj(name))
                    self.output.append(f"\t{name} {name}$self;\n")
                else:
                    print(f"Class '{name}' not declared to be inherited from class '{self.known_classes[-1]}'. Line {ctx.start.line}")
                    exit(0)

        

    def exitClass_def(self, ctx:oosParser.Class_defContext):
        self.last_method_def = None

    # --------------------------------------------

    def enterClass_body(self, ctx:oosParser.Class_bodyContext):
        self.output.append(f"}} {self.last_class_struct};\n")
        self.in_struct = False
        self.deindent()
    # --------------------------------------------

    def enterDeclarations(self, ctx:oosParser.DeclarationsContext):
       pass

    # Exit a parse tree produced by oosParser#declarations.
    def exitDeclarations(self, ctx:oosParser.DeclarationsContext):
        pass

    
    # --------------------------------------------

    def enterDecl_line(self, ctx:oosParser.Decl_lineContext):
        if ctx.ID():
            for id in ctx.ID():
                self.id_list.append(f"{id.getText()}")

    def exitDecl_line(self, ctx:oosParser.Decl_lineContext):
       
        decl_type = self.types_list.pop()
        
        if decl_type != "int":
            self.output.append(f"{self.tabbing()}struct {decl_type} ")
            for id in self.id_list:
                if self.last_method_def is None or self.known_classes[-1] == "main":
                    self.add_field_to_class(self.last_class_struct, id, decl_type)
                else:
                    self.add_field_to_class_method(self.last_class_struct, self.last_method_obj, id, decl_type)
            # switct to pointers cause it is an object
            if self.in_struct==True:
                self.id_list[:] = [f"*{id}" for id in self.id_list]
            else:
                 self.id_list[:] = [f"*{id} = NULL" for id in self.id_list]
            self.output.append(f"{", ".join(self.id_list )}")
            self.output.append(";\n")
        else:
            self.output.append(f"{self.tabbing()}{decl_type} ")
            for id in self.id_list:
               
                if self.last_method_def is None or self.known_classes[-1] == "main":
                    self.add_field_to_class(self.last_class_struct, id, decl_type)
                    
                else:
                    self.add_field_to_class_method(self.last_class_struct, self.last_method_obj, id, decl_type)
            self.output.append(f"{", ".join(self.id_list)}")

            self.output.append(";\n")

        self.id_list = []

    # --------------------------------------------
   
    def enterTypes(self, ctx:oosParser.TypesContext):
        if ctx.class_name():
            if (ctx.class_name().ID().getText() in self.known_classes):
                self.types_list.append(f"{ctx.class_name().ID().getText()}")
            else:
                print(f"Cannot find class '{ctx.class_name().ID().getText()}'")
                exit(0)
        elif ctx.getText() == "int":
            self.types_list.append(f"int")
           
    def exitTypes(self, ctx:oosParser.TypesContext):
        pass

    # --------------------------------------------

    def enterConstructor_def(self, ctx:oosParser.Constructor_defContext):
        constructor_class_name = ctx.class_name().ID().getText()
        
        if constructor_class_name in self.known_classes:
            method_name = self.add_method_to_class(constructor_class_name, constructor_class_name, True)
            
            self.last_method_def = method_name
            self.output.append(f"\n{constructor_class_name}* {self.last_method_obj.get_method_with_version()}$init({constructor_class_name} *self$")
        
        self.indent()

        self.in_constructor = True
        

    def exitConstructor_def(self, ctx:oosParser.Constructor_defContext):
        self.check_if_overide_methods_valid(self.known_classes[-1], self.last_method_obj)
        self.last_method_def = None
        self.output.append(f"\n}}\n")
        self.in_constructor = False

        self.deindent()

   
    def enterParlist(self, ctx:oosParser.ParlistContext):
        if ctx.ID():
            for id in ctx.ID():
                self.parlist.append(f"{id.getText()}")

    # Exit a parse tree produced by oosParser#parlist.
    def exitParlist(self, ctx:oosParser.ParlistContext):

        for idx in range(len(self.types_list)):
            if self.types_list[idx] != "int":   
                self.add_field_to_class_method(self.known_classes[-1], self.last_method_obj, self.parlist[idx], self.types_list[idx], True)
                self.output.append(f", {self.types_list[idx]} *{self.parlist[idx]}")
            else:
                self.add_field_to_class_method(self.known_classes[-1], self.last_method_obj, self.parlist[idx], "int", True)
                self.output.append(f", {self.types_list[idx]} {self.parlist[idx]}")
          
        self.parlist = []
        self.types_list = []

        self.output.append(f")\n{{\n")
       
        # defining dynamic memory allocation for new object if in constructor. used this because it is generating malloc even on norma functions
        if self.in_constructor:
          
            self.output.append(f"{self.tabbing()}if(self$ == NULL)\n")

            self.output.append(f"{self.tabbing()}")
            self.indent()
            self.output.append(f"{{\n{self.tabbing()}self$ = ({self.last_class_struct} *)malloc(sizeof({self.last_class_struct}));\n")
            self.deindent()
            self.output.append(f"{self.tabbing()}}}\n\n")
            

    # --------------------------------------------

    def enterMethod_def(self, ctx:oosParser.Method_defContext):
        method_name = ctx.ID().getText()
        self.last_method_def = method_name
        ret = ctx.getChild(4).getText()

        return_type = ""
        
        self.indent()

        # Check for the return type
        if "int" in ret:
            return_type = "int"
        elif "-" in ret:
            return_type = "void"
        elif ctx.class_name() is not None:
            class_name = ctx.class_name().getText()
            self.get_class_obj(class_name) # check if class is defined
            return_type = class_name

        self.add_method_to_class(self.known_classes[-1], method_name, False, return_type)
        if "int" not in return_type and "void" not in return_type:
            return_type = return_type +"*"

        self.output.append(f"\n{return_type} {self.last_method_obj.get_method_with_version()}({self.known_classes[-1]} *self$")

        self.last_method_def = method_name

    def exitMethod_def(self, ctx:oosParser.Method_defContext):
        self.check_if_overide_methods_valid(self.known_classes[-1], self.last_method_obj)
        self.deindent()
        self.output.append(f"\n}}\n")

    # --------------------------------------------    

    def enterClass_main_def(self, ctx:oosParser.Method_main_defContext):
        self.last_class_struct = "main"
        self.known_classes.append("main")
        self.add_class("main")

        self.output.append(f"\nint main(void)\n{{\n")
        
        self.indent()
        

    def exitClass_main_def(self, ctx:oosParser.Method_main_defContext):
        self.output.append(f"\n\n\treturn 0;\n}}")
        
    # --------------------------------------------    

    def enterStatement(self, ctx:oosParser.StatementContext):
        pass    

    # Exit a parse tree produced by oosParser#statement.
    def exitStatement(self, ctx:oosParser.StatementContext):
        if (ctx.getChildCount()):
            self.output.append(f"\n")           
    # --------------------------------------------    

    def enterReturn_stat(self, ctx:oosParser.Return_statContext):
        self.output.append(f"{self.tabbing()}return ")
        
        if ctx.expression():
            self.last_assignment_type = self.last_method_obj.get_return_type()
        elif ctx.getChildCount() == 2 and ctx.getChild(1).getText() == "self":
            self.output.append(f"self$")
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() == "self.":
            id = ctx.ID().getText()
            type_class = self.chech_if_id_declared(id, True)
            if (type_class[0] != self.last_method_obj.get_return_type()):
                print(f"On '{self.last_method_obj.get_name()}' : returns '{self.last_method_obj.get_return_type()}', returning incompatible type '{type}'. Line {ctx.start.line}")
                exit()
            if type_class[1].name != self.known_classes[-1]:
                id = f"{type_class[1].name}$self.{id}"
            self.output.append(f"self$ -> {id}")


    def exitReturn_stat(self, ctx:oosParser.Return_statContext):
        self.output.append(f";")

    # --------------------------------------------    

    def enterAssignment_stat(self, ctx:oosParser.Assignment_statContext):     
        if "self." in ctx.getText().split('=')[0] and self.last_class_struct != "main":
            class_self, assign = ctx.getText().split('.',1)
            field, val = assign.split('=')
            bool_class = self.has_class_field(self.known_classes[-1], field)

            if (bool_class[0]):
                type_class = self.chech_if_id_declared(field, True)
                self.last_assignment_type = type_class[0]
                if type_class[1].name != self.known_classes[-1]:
                    field = f"{type_class[1].name}$self.{field}"

                self.function_obj_stack.append((f"self$ -> {field}", self.last_assignment_type))  # hold that just in case it is consturctor or call in the function
                self.output.append(f"{self.tabbing()}self$ -> {field} = ")
        elif ctx.ID:
            id = str(ctx.ID())
            self.output.append(f"{self.tabbing()}")
            self.last_assignment_type = self.chech_if_id_declared(id)[0]
            self.function_obj_stack.append((id, self.last_assignment_type)) # hold that in case it is a constructor call
            self.output.append(f"{id} = ")
   
        
    def exitAssignment_stat(self, ctx:oosParser.Assignment_statContext):
        self.output.append(f";")
        self.last_assignment_type = None
        self.function_obj_stack = []
    # --------------------------------------------    

    def enterExpression(self, ctx:oosParser.ExpressionContext):
        self.expression_stack.append("")

 
    def exitExpression(self, ctx:oosParser.ExpressionContext):
        completed_expression = self.expression_stack.pop()
        if self.expression_stack:
            
            self.expression_stack[-1] += completed_expression
        else:
           
            self.current_expression = completed_expression
            if self.print_expression_list == None:
                self.output.append(self.current_expression)
            else:
                self.print_expression_list.append(self.current_expression)
            
    # --------------------------------------------    
    
    def enterFactor(self, ctx:oosParser.FactorContext):
    
        current_expr = self.expression_stack[-1] if self.expression_stack else ""
       
        # Integer
        if ctx.INTEGER():

            if (self.last_assignment_type != "int" and len(self.function_stack) == 0 and self.print_expression_list == None and self.in_relop == False):
                
                print(f"Assigning or returning '{ctx.getText()}', type int to field type '{self.last_assignment_type}'. Line {ctx.start.line}")
                exit(0)
            current_expr += f"{ctx.getText()}"
       
        # (expression)
        elif ctx.expression():
            
            current_expr += f"("
        
        # self.id
        elif ctx.getChildCount() == 2 and ctx.getChild(0).getText() == "self." and ctx.ID():
            
            field = str(ctx.getChild(1).getText())
            
            if (self.has_class_field(self.known_classes[-1], field)[0] and self.last_class_struct != "main"):
                tmp_class = self.has_class_field( self.known_classes[-1], field)[1]
                    
                if tmp_class.name != self.known_classes[-1]:
                    field = f"{tmp_class.name}$self.{field}"
                current_expr += f"self$ -> {field}"
            else:
                current_expr += f"{field}"

        # id
        elif ctx.getChildCount() == 1 and ctx.ID():
            
            id_type = self.chech_if_id_declared(ctx.ID(0).getText())[0]
            if len(self.function_stack) > 0 or id_type == self.last_assignment_type or self.print_expression_list != None or self.in_relop == True:
                current_expr += f"{str(ctx.ID(0))}"
            else:
                print(f"Assigning or returning '{ctx.getText()}', type '{id_type}' to field type '{self.last_assignment_type}'. Line {ctx.start.line}")
                exit(0)
        
        # id.function
        elif ctx.getChildCount() >= 3 and ctx.getChild(1).getText() == '.' and ctx.ID and ctx.func_call():
            id = str(ctx.getChild(0).getText())
            type = self.chech_if_id_declared(id)[0]
            self.function_obj_stack.append((id, type))
            
        # self.functioncall
        elif ctx.getChildCount() == 2 and ctx.func_call() and ctx.getChild(0).getText() == "self.":
            self.function_obj_stack.append(("self", self.known_classes[-1]))

        # self.id.function
        elif ctx.getChildCount() == 4 and ctx.getChild(0).getText() == "self." and ctx.getChild(2).getText() == "." and ctx.ID() and ctx.func_call():
            id = str(ctx.getChild(1).getText())
            bool_class = self.has_class_field(self.known_classes[-1], id)
            type_class = self.chech_if_id_declared(id, True)
            
            if (bool_class[0]):    
                if type_class[1].name != self.known_classes[-1]:
                    id = f"{type_class[1].name}$self.{id}"
                else:
                    self.function_obj_stack.append((f"self$ -> {id}", type_class[0]))  # hold that just in case it is consturctor or call in the function

        # contructor call
        elif ctx.func_call() and ctx.getChildCount() == 1:
            pass
           
        
        # id.id
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() == '.':
            class_id = ctx.getChild(0).getText() 
            field_id = ctx.getChild(2).getText() 

            class_id_type = self.chech_if_id_declared(class_id)[0]
            # has_class_field returns len = 3 array. 0 bool if field with id found
            # idx 1 class object that field was found, idx 2 if the class that was found is same or parent class(inherited field ) 
            if (self.has_class_field( class_id_type, field_id)[0] or self.print_expression_list != None):
                tmp_class = self.has_class_field( class_id_type, field_id) 
                if len(self.function_stack) > 0 or self.get_class_field_type(tmp_class[1].name, field_id) == self.last_assignment_type or self.in_relop == True:
                    
                    if tmp_class[1].name != self.known_classes[-1] and tmp_class[2] == False:
                        field_id = f"{tmp_class[1].name}$self.{field_id}"
                        input()
                    current_expr += f"{class_id} -> {field_id}"
                else:
                    print(f"Assigning or returning '{field_id}', type '{class_id}' to field type '{self.last_assignment_type}'. Line {ctx.start.line}")
                    exit(0)

        if self.expression_stack:
            self.expression_stack[-1] = current_expr
            
    def exitFactor(self, ctx:oosParser.FactorContext):
       if ctx.expression():
            self.expression_stack[-1] += ")"
    
    # --------------------------------------------    
    
    def enterFunc_call(self, ctx:oosParser.Func_callContext):
        function_name = ctx.ID().getText()
        if self.function_call_param_num > 0:
            self.function_call_param_num_stack.append(self.function_call_param_num)
            self.function_call_param_num = 0
        
        if (self.function_obj_stack != []):
            id, type = self.function_obj_stack.pop()
            
            self.function_class_stack.append(type)
            
            
            self.function_stack.append(f"{function_name}({id}")

    def exitFunc_call(self, ctx:oosParser.Func_callContext):
        function_call = self.function_stack.pop()
        class_name = self.function_class_stack.pop()
        
        parts = function_call.split('(', 1)

        function_name = parts[0].strip()
        arguments = parts[1].strip() 
        rest_args = ""
        
        if ',' in arguments:
            rest_args = ", "
            rest_args  += arguments.split(',', 1)[1]
        
        object_param = arguments         
        
        ver = self.search_actual_class_method(class_name, function_name, self.function_call_param_num)

        if ver[1] != None:
            name = object_param.split(',')[0].split(')')[0]
            name = name.strip()
            if name == "self":
                name += "$"
            arguments = f"&{name} -> {ver[1].name}$self{rest_args}"

        if len(self.function_call_param_num_stack):
            self.function_call_param_num = self.function_call_param_num_stack.pop()
        else:
            self.function_call_param_num = 0       
        
        function_call = f"{function_name}${ver[0]}({arguments})"
        if self.expression_stack:
            
            self.expression_stack[-1] += function_call
        else:
            self.current_expression = function_call

    # --------------------------------------------    
            
    def enterArglist(self, ctx:oosParser.ArglistContext):
        if(ctx.argitem()):
            self.expression_stack.append("")
            
    
    def enterArgitem(self, ctx:oosParser.ArgitemContext):
        if (ctx.expression()):
            self.function_call_param_num += 1
            self.expression_stack[-1] +=", "

    def exitArgitem(self, ctx:oosParser.ArgitemContext):
        pass

    def exitArglist(self, ctx:oosParser.ArglistContext):
        if(ctx.argitem()):
            if self.expression_stack:
                completed_expression = self.expression_stack.pop()
                self.function_stack[-1] += completed_expression
               
    # --------------------------------------------    

    def enterDirect_call_stat(self, ctx:oosParser.Direct_call_statContext):
        # direct id.funtion
        if (ctx.getChildCount() >= 3 and ctx.getChild(1).getText() == '.' and ctx.ID and ctx.func_call()):
            id = str(ctx.ID())
            self.output.append(f"{self.tabbing()}")
            type = self.chech_if_id_declared(id)[0]
            self.function_obj_stack.append((id, type))
        
        # self.id.function
        elif ctx.getChildCount() == 4 and ctx.getChild(0).getText() == "self." and ctx.getChild(2).getText() == "." and ctx.ID() and ctx.func_call():
            
            self.output.append(f"{self.tabbing()}")
            id = str(ctx.getChild(1).getText())

            bool_class = self.has_class_field(self.known_classes[-1], id)

            if (bool_class[0]):
                type_class = self.chech_if_id_declared(id, True)
                self.last_assignment_type = type_class[0]
                if type_class[1].name != self.known_classes[-1]:
                    id = f"{type_class[1].name}$self.{id}"

                self.function_obj_stack.append((f"self$ -> {id}", self.last_assignment_type))  # hold that just in case it is consturctor or call in the function

    def exitDirect_call_stat(self, ctx:oosParser.Direct_call_statContext):
        self.output.append(f"{self.current_expression};")

    # --------------------------------------------    

    def enterPrint_stat(self, ctx:oosParser.Print_statContext):
        self.print_expression_list = []
        self.output.append(f"{self.tabbing()}printf(\"")

    def exitPrint_stat(self, ctx:oosParser.Print_statContext):
        
        fields=""
        formating = ""
 
        for expression in self.print_expression_list:
            fields += "%d "
            formating += str(", ")+expression
        self.output.append(f"{fields}\\n\"{formating});")

        self.print_expression_list = None

    # --------------------------------------------    

    def enterInput_stat(self, ctx:oosParser.Input_statContext):
        
        # 'input' ID
        id = None
        type = None
        #   in main 
        if ctx.getChildCount() == 2 and ctx.ID:
            id = ctx.ID().getText()
            type = self.chech_if_id_declared(id)[0]
            
        # in class input
        elif ctx.getChildCount() == 3 and ctx.ID:
            id = ctx.ID().getText()
            type = self.chech_if_id_declared(id, True)[0]
    
            if self.last_class_struct != "main":
                id = "self$ -> " + id
        if (type != "int"):
            print(f"You are trying to input on an 'Object' type which is illegal . Line {ctx.start.line}")
            exit(0)


        self.output.append(f"{self.tabbing()}scanf(\"%d\", &{id})")

    def exitInput_stat(self, ctx:oosParser.Input_statContext):
        pass

    # --------------------------------------------    

    def enterCondition(self, ctx:oosParser.ConditionContext):
        self.boolterm_count = len(ctx.boolterm()) - 1

    def exitCondition(self, ctx:oosParser.ConditionContext):
        
        self.output.append(f")\n{self.tabbing()}{{\n")
        self.indent()

    # --------------------------------------------    

    def enterBoolterm(self, ctx:oosParser.BooltermContext):
        pass

    def exitBoolterm(self, ctx:oosParser.BooltermContext):
        if self.boolterm_count > 0:
            self.output.append(" || ")
            self.boolfactor_count -= 1 

    # --------------------------------------------    
    
    def enterBoolfactor(self, ctx:oosParser.BoolfactorContext):
        self.in_relop = True
                
        if ctx.getChildCount() == 4 and ctx.getChild(0).getText() == 'not':
            self.output.append("!(") 

        elif ctx.getChildCount() == 3 and ctx.getChild(0).getText() == '[':
            self.output.append("(")

        elif ctx.expression(0) and ctx.rel_oper() and ctx.expression(1):
            pass

    def exitBoolfactor(self, ctx:oosParser.BoolfactorContext):
        self.in_relop = False

        if self.boolfactor_count > 0:
            self.output.append(" && ")
            self.boolfactor_count -= 1
        if ctx.getChildCount() in [3, 4] and ctx.getChild(0).getText() in ['not', '[']:
            self.output.append(")")
    # --------------------------------------------    
    
    def enterBoolterm(self, ctx:oosParser.BooltermContext):
        self.boolfactor_count = len(ctx.boolfactor()) - 1

    def exitBoolterm(self, ctx:oosParser.BooltermContext):
        if self.boolterm_count > 0:
            self.output.append(" || ")
            self.boolterm_count -= 1

    # --------------------------------------------    

    def enterWhile_stat(self, ctx:oosParser.While_statContext):
        self.output.append(f"\n{self.tabbing()}while(")

    def exitWhile_stat(self, ctx:oosParser.While_statContext):
        self.deindent()
        self.output.append(f"\n{self.tabbing()}}}")


    # --------------------------------------------    
    def enterIf_stat(self, ctx:oosParser.If_statContext):
        self.output.append(f"\n{self.tabbing()}if(")

    # Exit a parse tree produced by oosParser#if_stat.
    def exitIf_stat(self, ctx:oosParser.If_statContext):
        self.output.append(f"\n")
        
    # --------------------------------------------    

        # Enter a parse tree produced by oosParser#else_part.
    def enterElse_part(self, ctx:oosParser.Else_partContext):
        self.deindent()
        self.output.append(f"\n{self.tabbing()}}}")
        if (ctx.statements()):
            self.output.append(f"\n{self.tabbing()}else\n{self.tabbing()}{{\n")
            self.indent()

    # Exit a parse tree produced by oosParser#else_part.
    def exitElse_part(self, ctx:oosParser.Else_partContext):
        if (ctx.statements()):
            self.deindent()
            self.output.append(f"\n{self.tabbing()}}}")

    # -----------------Terminating Characters------------------    

    def enterRel_oper(self, ctx:oosParser.Rel_operContext):
        if ctx.getChildCount() > 0:
            self.output.append(f" {ctx.getText()} ")

    # --------------------------------------------    

    def enterAdd_oper(self, ctx:oosParser.Add_operContext):
        if self.expression_stack:
            self.expression_stack[-1] += (f" {ctx.getText()} ")

    # --------------------------------------------    

    def enterMul_oper(self, ctx:oosParser.Mul_operContext):
        if self.expression_stack:
            self.expression_stack[-1] += (f" {ctx.getText()} ")

