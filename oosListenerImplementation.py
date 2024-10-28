from oosListener import oosListener
from oosParser import oosParser
from symbolTable import *
import copy

class oosListenerImplementation(oosListener):

    def __init__(self):
        self.class_entries = {}

        self.output = []
        self.known_classes = []
        self.last_class_struct = None
        self.last_method_def = None
        self.last_method_obj = None
        self.in_constructor = False
        self.parenthesis_stack = []
        self.last_assignment_type = None #  this is used so i can check if assignement is same type as declaration

        self.id_list = []
        self.types_list = []
        self.last_type= None

        self.parlist = []
        self.actual_pars = []
    
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
        method = class_obj.add_method(method_name, is_constructor, return_type)
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
            if (class_obj.has_field(field_name)):
                return True
            else:
                print(f"Class '{class_name}' does not have field '{field_name}' declared")
                exit(0)
    
    def get_class_field_type(self, class_name, field_name):
        return self.get_class_obj(class_name).get_field_type(field_name)
    
    def get_method_field_type(self, field_name):
        return self.last_method_obj.get_field_type(field_name)

    
    def chech_if_id_declared(self, id, is_self = False):
        if self.last_class_struct == "main" or is_self:
            if self.has_class_field(self.last_class_struct, id) == True:
                
                return self.get_class_field_type(self.last_class_struct, id)
            else:
                print(f"Field with name '{id}': int not declared in scope of {self.last_method_obj.get_name()}")
                exit(0)
        elif self.last_method_obj.has_field(id) == True:
            return self.get_method_field_type(id)
        else:
            print(f"Field with name '{id}': int not declared in scope of {self.last_method_obj.get_name()}")
            exit(0)
            
    def check_if_overide_methods_valid(self, class_name, method_object):
        class_obj = self.get_class_obj(class_name)
        class_obj.check_if_overide_methods_valid( method_object)        

    def get_oos_compiled(self):
        return "".join(self.output)

    # --------------------------------------------

    def enterStartRule(self, ctx:oosParser.StartRuleContext):
        # adding necessary C includes
        self.output.append(f"#include <stdio.h>\n")
        self.output.append(f"#include <stdlib.h>\n")

    # --------------------------------------------

    def enterClass_def(self, ctx:oosParser.Class_defContext):

        class_name = ctx.class_name(0).ID().getText()
        self.last_class_struct = class_name

        self.output.append(f"\ntypedef struct {self.last_class_struct} {{")
        self.known_classes.append(f"{self.last_class_struct}")
        self.output.append("\n")

        self.add_class(class_name)

    def exitClass_def(self, ctx:oosParser.Class_defContext):
        pass

    # --------------------------------------------

    def enterClass_body(self, ctx:oosParser.Class_bodyContext):
        self.output.append(f"}} {self.last_class_struct};\n")
    
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
        self.output.append("\t")

        decl_type = self.types_list.pop()
        self.output.append(f"{decl_type} ")
        
        if decl_type != "int":
            for id in self.id_list:
                if self.last_method_def is None or self.known_classes[-1] == "main":
                    self.add_field_to_class(self.last_class_struct, id, decl_type)
                else:
                    self.add_field_to_class_method(self.last_class_struct, self.last_method_obj, id, decl_type)
            # switct to pointers cause it is an object
            self.id_list[:] = [f"*{id}" for id in self.id_list]
            self.output.append(f"{", ".join(self.id_list)}")
        else:
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
            self.output.append(f"\n{constructor_class_name}* init${self.last_method_obj.get_method_with_version()}({constructor_class_name} *self$")

        self.in_constructor = True
            
    def exitConstructor_def(self, ctx:oosParser.Constructor_defContext):
        self.check_if_overide_methods_valid(self.known_classes[-1], self.last_method_obj)
        self.last_method_def = None
        self.output.append(f"\n}}\n")
        self.in_constructor = False

   
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
            self.output.append(f"\tif(self$ == NULL)\n\t{{\t\n\t\tself$ = ({self.last_class_struct} *)malloc(sizeof({self.last_class_struct}));\n\t}}\n\n")

    # --------------------------------------------

    def enterMethod_def(self, ctx:oosParser.Method_defContext):
        method_name = ctx.ID().getText()
        self.last_method_def = method_name
        text, ret = ctx.getText().split(':', 1)
        return_type = ""
        
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
        self.output.append(f"\n}}\n")

    # --------------------------------------------    

    def enterClass_main_def(self, ctx:oosParser.Method_main_defContext):
        self.last_class_struct = "main"
        self.known_classes.append("main")
        self.add_class("main")

        self.output.append(f"\nint main(void)\n{{\n")
        

    def exitClass_main_def(self, ctx:oosParser.Method_main_defContext):
        self.output.append(f"\n\n\treturn 0;\n}}")
        
    # --------------------------------------------    

    def enterStatement(self, ctx:oosParser.StatementContext):
        pass

    # Exit a parse tree produced by oosParser#statement.
    def exitStatement(self, ctx:oosParser.StatementContext):
        self.output.append(f";\n")

    # --------------------------------------------    

    def enterReturn_stat(self, ctx:oosParser.Return_statContext):
        self.output.append(f"\treturn ")
        
        if ctx.expression():
            self.last_assignment_type = self.last_method_obj.get_return_type()
        elif ctx.getChildCount() == 2 and ctx.getChild(1).getText() == "self":
            self.output.append(f"self$")
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() == "self.":
            id = ctx.ID().getText()
            type = self.chech_if_id_declared(id, True)
            if (type != self.last_method_obj.get_return_type()):
                print(f"On '{self.last_method_obj.get_name()}' : returns '{self.last_method_obj.get_return_type()}', returning incompatible type '{type}'. Line {ctx.start.line}")
                exit()
            self.output.append(f"self$ -> {id}")


    def exitReturn_stat(self, ctx:oosParser.Return_statContext):
        pass
        # here i should check if the returns made are type of return type of the method and raise error

    # --------------------------------------------    

    def enterAssignment_stat(self, ctx:oosParser.Assignment_statContext):
        if "self." in ctx.getText() and self.last_class_struct != "main":
            class_self, assign = ctx.getText().split('.',1)
            
            field, val = assign.split('=')

            if (self.has_class_field(self.known_classes[-1], field)):
                self.last_assignment_type = self.chech_if_id_declared(field, True)
                self.output.append(f"\tself$ -> {field} = ")
        elif ctx.ID:
            id = str(ctx.ID())
            self.output.append(f"\t")
            self.last_assignment_type = self.chech_if_id_declared(id)
            self.output.append(f"{id} = ")
   
        
    def exitAssignment_stat(self, ctx:oosParser.Assignment_statContext):
        pass

     # --------------------------------------------    
    
    def enterFactor(self, ctx:oosParser.FactorContext):
        # this is used to keep track of parenthesis in case of expresion

        is_expression = ctx.expression() is not None
        self.parenthesis_stack.append(is_expression)

        if ctx.INTEGER():
            if (self.last_assignment_type != "int"):
                print(f"Assigning or returning '{ctx.getText()}', type int to field type '{self.last_assignment_type}'. Line {ctx.start.line}")
                exit(0)
            self.output.append(f"{ctx.getText()}")

        elif ctx.expression():
            self.output.append(f"( ")
        
        elif ctx.getChildCount() == 2 and ctx.getChild(0).getText() == "self." and ctx.ID():
            field = str(ctx.getChild(1).getText())
            if (self.has_class_field(self.known_classes[-1], field) and self.last_class_struct != "main"):
                self.output.append(f"self$ -> {field}")
            else:
                self.output.append(f"{field}")
        elif ctx.getChildCount() == 3 and ctx.getChild(1).getText() == '.':
            class_id = ctx.getChild(0).getText() 
            field_id = ctx.getChild(2).getText() 

            class_id_type = self.chech_if_id_declared(class_id)
            if (self.has_class_field( class_id_type, field_id)):
                if self.get_class_field_type(class_id_type, field_id) == self.last_assignment_type:
                    self.output.append(f"{class_id} -> {field_id}")
                else:
                    print(f"Assigning or returning '{field_id}', type {class_id} to field type '{self.last_assignment_type}'. Line {ctx.start.line}")

        elif ctx.getChildCount() == 1 and ctx.ID():

            id_type = self.chech_if_id_declared(ctx.ID(0).getText())
            if id_type == self.last_assignment_type:
                self.output.append(f"{str(ctx.ID(0))}")
            else:
                print(f"Assigning or returning '{ctx.getText()}', type {id_type} to field type '{self.last_assignment_type}'. Line {ctx.start.line}")
                exit(0)
            
    def exitFactor(self, ctx:oosParser.FactorContext):
        if (len(self.parenthesis_stack) > 0):
            was_expression = self.parenthesis_stack.pop()
            if was_expression:
                self.output.append(")")

    # -----------------Terminating Characters------------------    

    def enterRel_oper(self, ctx:oosParser.Rel_operContext):
        self.output.append(f" {ctx.getText()} ")

    # --------------------------------------------    

    def enterAdd_oper(self, ctx:oosParser.Add_operContext):
        self.output.append(f" {ctx.getText()} ")

    # --------------------------------------------    

    def enterMul_oper(self, ctx:oosParser.Mul_operContext):
         self.output.append(f" {ctx.getText()} ")

