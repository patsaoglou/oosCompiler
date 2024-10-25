from oosListener import oosListener
from oosParser import oosParser

class class_method:

    def __init__(self, name, is_constructor=False, type_list=None, id_list=None):
        self.name = name
        self.is_constructor = is_constructor
        self.type_list = type_list if type_list is not None else []
        self.id_list = id_list if id_list is not None else []
        self.fields = {} 

    def set_as_constructor(self):
        self.is_constructor = True

    def add_param(self, type_, id_):
        self.type_list.append(type_)
        self.id_list.append(id_)
        self.fields[id_] = type_

    def add_field(self, field_name, field_type):
        self.fields[field_name] = field_type

    def has_field(self, field_name, expected_type=None):
        if field_name not in self.fields:
            return False
        if expected_type is not None:
            return self.fields[field_name] == expected_type
        return True

    def __str__(self):
        inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        methods_str = '\n  '.join([str(method) for method in self.methods])
        fields_str = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"Class name: {self.name}\nInherits from: [{inheritance_str}]\nFields: [{fields_str}]\nMethods:\n  {methods_str}"


class class_info:

    def __init__(self, name):
        self.name = name
        self.inherit_from = [] # class_info list
        self.methods = []      # class_method list
    
    def add_inheritance(self, parent_class):    
        if isinstance(parent_class, class_info):
            self.inherit_from.append(parent_class)
        else:
            print("add_inheritance adding something that is not instance. Exit")
            exit(0)

    def add_method(self, method):
        if isinstance(method, class_method):
            self.methods.append(method)
        else:
            print("add_method adding something that is not instance. Exit")
            exit(0)

    def __str__(self):
        inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        methods_str = '\n  '.join([str(method) for method in self.methods])
        
        return f"Class name: {self.name}\nInherits from: [{inheritance_str}]\nMethods:\n  {methods_str}"

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
    
    def add_class(self, class_info_obj):
        if isinstance(class_info_obj, class_info):
            self.class_entries[class_info_obj.name] = class_info_obj

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
                self.output.append(f", {self.types_list[idx]} *{self.parlist[idx]}")
            else:
                self.output.append(f", {self.types_list[idx]} {self.parlist[idx]}")
          
        self.parlist = []
        self.types_list = []

        self.output.append(f")\n{{\n\t")
         