from oosListener import oosListener
from oosParser import oosParser

class oosListenerImplementation(oosListener):

    def __init__(self):
        self.output = []

        self.id_list = []

    def get_oos_compiled(self):
        return "".join(self.output)

    # --------------------------------------------
   
    def enterClass_def(self, ctx:oosParser.Class_defContext):
        print("called: enterClass_def")

        class_name = ctx.class_name(0).ID().getText()
        self.output.append(f"typedef struct {class_name} {{\n")

    def exitClass_def(self, ctx:oosParser.Class_defContext):
        class_name = ctx.class_name(0).ID().getText()
        self.output.append(f"\n}} {class_name};\n")

    # --------------------------------------------

    def enterDecl_line(self, ctx:oosParser.Decl_lineContext):
        print("called: enterDecl_line")
        for id_object in ctx.ID():
            self.id_list.append(f"{id_object.getText()}")

    def exitDecl_line(self, ctx:oosParser.Decl_lineContext):
        pass

    # --------------------------------------------
   
    def enterTypes(self, ctx:oosParser.TypesContext):
        print("called: enterTypes")
        if ctx.class_name():
            pass
        elif ctx.getText() == "int":
            self.output.append(f"\t{ctx.getText()} ")

        if self.id_list:
            self.output.append(", ".join(self.id_list))
        self.id_list = []
           
    def exitTypes(self, ctx:oosParser.TypesContext):
        self.output.append(f";\n")

    # --------------------------------------------
   