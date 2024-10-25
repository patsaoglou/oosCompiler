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
        self.fields = {}
    
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

    def add_field(self, field_name, field_type):
        self.fields[field_name] = field_type
    
    def get_field_type(self, field_name):
        field_type = self.fields.get(field_name)
        if (field_type):
            return field_type
        else:
            print("get_field_type field does not exist. Exit")
            exit(0)

    def __str__(self):
        inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        methods_str = '\n  '.join([str(method) for method in self.methods])
        fields_str = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"Class name: {self.name}\nFields: [{fields_str}]\nInherits from: [{inheritance_str}]\nMethods:\n  {methods_str}"