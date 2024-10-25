from oosListener import oosListener
from oosParser import oosParser
from symbolTable import *

class oosListenerImplementation(oosListener):

    def __init__(self):
        self.class_entries = {}

        self.output = []
        self.known_classes = []
        self.last_class_struct = None

        self.id_list = []
        self.types_list = []
        self.last_type= None

        self.parlist = []
        self.actual_pars = []
    
    def add_class(self, class_name):
        new = class_info(class_name)
        if isinstance(new, class_info):
            self.class_entries[new.name] = new
    
    def add_field_to_class(self, class_name, field_name, field_type):
        class_obj = self.class_entries.get(class_name)
        if (class_obj):
            class_obj.add_field(field_name, field_type)
            print(class_obj)
        else:
            print("adding field to class that does not exist.")
            exit(0)

    def get_class_obj(self, class_name):
        return self.class_entries.get(class_name)

    def has_class_field_with_value(self, class_name, field_name, field_type):
        class_obj = self.get_class_obj(class_name)
        if (class_obj):
            if class_obj.get_field_type(field_name) == field_type:
                return True
            else:
                return False

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
            # switct to pointers cause it is an object
            self.id_list[:] = [f"*{id}" for id in self.id_list]
            self.output.append(f"{", ".join(self.id_list)}")
        else:
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
            self.output.append(f"\n{constructor_class_name}* init${constructor_class_name}({constructor_class_name} *self$")
            
    def exitConstructor_def(self, ctx:oosParser.Constructor_defContext):
        
        # ti allo mporei
        self.output.append(f"\n}}\n")

   
    def enterParlist(self, ctx:oosParser.ParlistContext):
        if ctx.ID():
            for id in ctx.ID():
                self.parlist.append(f"{id.getText()}")

    # Exit a parse tree produced by oosParser#parlist.
    def exitParlist(self, ctx:oosParser.ParlistContext):

        for idx in range(len(self.types_list)):
            
            if self.types_list[idx] != "int":
                self.add_field_to_class(self.known_classes[-1], self.parlist[idx], self.types_list[idx])
                self.output.append(f", {self.types_list[idx]} *{self.parlist[idx]}")
            else:
                self.add_field_to_class(self.known_classes[-1], self.parlist[idx], self.types_list[idx])
                self.output.append(f", {self.types_list[idx]} {self.parlist[idx]}")
          
        self.parlist = []
        self.types_list = []

        self.output.append(f")\n{{\n\t")

        # defining dynamic memory allocation for new object
        print(self.get_class_obj("Number"))
        self.output.append(f"")