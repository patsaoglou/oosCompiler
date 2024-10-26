class class_method:

    def __init__(self, name, is_constructor=False, type_list=None, id_list=None):
        self.name = name
        self.is_constructor = is_constructor
        self.fields = {} 
        self.params = {}
        self.param_number = 0

    def set_as_constructor(self):
        self.is_constructor = True

    def set_name(self, new_name):
        self.name = new_name

    def add_field(self, field_name, field_type, is_param = False):
        if field_name in self.fields:
            print(f"Field '{field_name}' is already declared in scope of '{self.name}' method")
            exit(0)
        if is_param:
            self.params[field_name] = field_type
            self.param_number += 1
        self.fields[field_name] = field_type

    def has_field(self, field_name, expected_type=None):
        if field_name not in self.fields:
            return False
        if expected_type is not None:
            return self.fields[field_name] == expected_type
        return True
    
    def get_params(self):
        return self.params
    
    def __str__(self):
        # inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        params = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"\n\tMethod name: {self.name}\n\tFields: [{params}]\n\tParameter num: {str(self.param_number)}\n\tConstructor: {str(self.is_constructor)}"


class class_info:

    def __init__(self, name):
        self.name = name
        self.inherit_from = [] # class_info list
        self.methods = []      # class_method list
        self.constructor_number = 0
        self.fields = {}
    
    def add_inheritance(self, parent_class):    
        if isinstance(parent_class, class_info):
            self.inherit_from.append(parent_class)
        else:
            print("add_inheritance adding something that is not instance. Exit")
            exit(0)
    
    def add_method(self, method_name, is_constructor = False):
        new_method = class_method(None)
        
        if is_constructor:
            self.constructor_number +=1
            method_name = method_name + str(self.constructor_number)
            new_method.set_name(method_name)
            new_method.is_constructor = True
        
        for i in self.methods:
            if i.name == method_name:
                print(f"Method with name '{method_name}' is already declared in class '{self.name}'")
                exit(0)

        self.methods.append(new_method)
        return method_name
    
    def add_field_to_method(self, method_name, field_name, field_type, is_param = False):
        for method in self.methods:
            if method.name == method_name:
                if field_name in self.fields:
                    print(f"Field '{field_name}' is already declared in scope of '{method.name}' method")
                    exit(0)
                method.add_field(field_name, field_type, is_param)
                return
        print(f"Method with name '{method_name}' does not exist to add params")
        exit(0)
    
    def add_field(self, field_name, field_type):
        if field_name in self.fields:
            print(f"Field '{field_name}' is already declared in scope of '{self.name}'")
            exit(0)
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
        
        return f"Class name: {self.name}\nFields: [{fields_str}]\nInherits from: [{inheritance_str}]\nMethods:{methods_str}"