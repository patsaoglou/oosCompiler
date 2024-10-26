class class_method:

    def __init__(self, name, is_constructor = False):
        self.version = 1
        self.name = name
        self.is_constructor = is_constructor
        self.fields = {} 
        self.params = {}
        self.param_number = 0
        self.return_type = None

    def set_next_version(self, next):
        self.version = next
    
    def get_version(self):
        return self.version

    def set_return_type(self, return_type):
        self.return_type = return_type

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
    
    def get_method_with_version(self):
        return self.name+"$"+str(self.version)
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        # inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        params = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"\n\tMethod name: {self.name}\n\tFields: [{params}]\n\tParameter num: {str(self.param_number)}\n\tVersion: {str(self.version)}\n\tReturns: {str(self.return_type)}\n\tConstructor: {str(self.is_constructor)}"


class class_info:

    def __init__(self, name):
        self.name = name
        self.inherit_from = [] # class_info list
        self.methods = {}
        self.constructor_number = 0
        self.fields = {}
    
    def add_inheritance(self, parent_class):    
        if isinstance(parent_class, class_info):
            self.inherit_from.append(parent_class)
        else:
            print("add_inheritance adding something that is not instance. Exit")
            exit(0)
    
    def add_method(self, method_name, is_constructor = False, return_type = "void"):
        new_method = class_method(None)
        
        if is_constructor:
            self.constructor_number +=1
            new_method.set_return_type(self.name)
            new_method.set_name(method_name)
            new_method.is_constructor = True
        else:
            new_method.set_name(method_name)
            new_method.set_return_type(return_type)

        if method_name not in self.methods:
            self.methods[method_name] = []
            self.methods[method_name].append(new_method)
        else:
            list_overided_methods = self.methods.get(method_name)
            self.methods[method_name].append(new_method)
            new_method.set_next_version(list_overided_methods[-1].get_version()+1)

        return [method_name, new_method]
    
    def add_field_to_method(self, method_obj, field_name, field_type, is_param = False):
        if field_name in method_obj.fields:
            print(f"Field '{field_name}' is already declared in scope of '{method_obj.name}' method")
            exit(0)
        method_obj.add_field(field_name, field_type, is_param)

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

    def check_if_overide_methods_valid(self, method_object):
        method_name = method_object.get_name()
        overrided_methods = self.methods[method_name]
        method_object_types = list(method_object.get_params().values())
        for method in overrided_methods:
            if method == method_object:
                continue
            if len(method.get_params()) == len(method_object.get_params()):
                method_types = list(method.get_params().values())
                for type in range(len(method_types)):
                    if method_types[type] != method_object_types[type]:
                        return
                print(f"All parameters are the same type within overided methods '{method.get_method_with_version()}' and '{method_object.get_method_with_version()}'")
                exit(0)

    def __str__(self):
        inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        
        all_classes = [cls for classes_list in self.methods.values() for cls in classes_list]
        methods_str = '\n  '.join([str(method) for method in all_classes])
        fields_str = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"Class name: {self.name}\nFields: [{fields_str}]\nInherits from: [{inheritance_str}]\nMethods:{methods_str}"