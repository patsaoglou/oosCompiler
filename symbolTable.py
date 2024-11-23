class class_method:

    def __init__(self, name, is_constructor = False):
        self.version = 1
        self.name = name
        self.is_constructor = is_constructor
        self.fields = {} 
        self.params = {}
        self.param_number = 0
        self.return_type = None

    def set_version(self, next):
        self.version = next
    
    def get_version(self):
        return self.version

    def set_return_type(self, return_type):
        self.return_type = return_type
    
    def get_return_type(self):
        return self.return_type

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
        if str(field_name) not in list(self.fields.keys()):
            return False
        if expected_type is not None:
            
            return str(self.fields.get(str(field_name))) == str(expected_type)
        return True
    
    def get_field_type(self, field_name):
        if (self.has_field(field_name)):
            return self.fields.get(field_name)

    def get_params(self):
        return self.params
    
    def get_method_with_version(self):
        return self.name+"$"+str(self.version)
    
    def get_name(self):
        return self.name
    
    def get_param_number(self):
        return self.param_number


    def __str__(self):
        # inheritance_str = ', '.join([parent.name for parent in self.inherit_from])
        params = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"\n\tMethod name: {self.name}\n\tFields: [{params}]\n\tParameter num: {str(self.param_number)}\n\tVersion: {str(self.version)}\n\tReturns: {str(self.return_type)}\n\tConstructor: {str(self.is_constructor)}"


class class_info:

    def __init__(self, name):
        self.name = name
        self.inherits_from = [] # class_info list
        self.methods = {}
        self.constructor_number = 0
        self.fields = {}
    
    def add_inheritance(self, parent_class):    
        if isinstance(parent_class, class_info):
            self.inherits_from.append(parent_class)
        else:
            print("add_inheritance adding something that is not instance. Exit")
            exit(0)
    
    def add_method(self, method_name, is_constructor = False, return_type = "void", global_method_versions = {}):
      
        new_method = class_method(None)
        new_method.add_field("self",self.name, True)
        if is_constructor:
            self.constructor_number +=1
            new_method.set_return_type(self.name)
            new_method.set_name(method_name)
            new_method.is_constructor = True
        else:
            new_method.set_name(method_name)
            new_method.set_return_type(return_type)

        # print(self)
        ver = global_method_versions.get(method_name)
        if ver == None:
           
            self.methods[method_name] = []
            self.methods[method_name].append(new_method)
            global_method_versions[method_name] = 1
        else:
            if self.methods.get(method_name) == None: #might be in global version but not inside the current class
                self.methods[method_name] = []
            self.methods[method_name].append(new_method)
            new_method.set_version(ver+1)
            global_method_versions[method_name] = ver + 1

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
    
    # returns [boolean, class_object, if class self same as class found]. used to know if i need to add self->x or self -> object.x on the final append 
    def has_field(self, field_name):
        field_type = self.fields.get(field_name)

        if (field_type):
            return [True, self, True]
        else:
            
            class_object = self.search_field_in_inherited_classes(field_name)
            if class_object:
                
                return [True, class_object, False] 
            else:
                return [False, None, False]
    
    def get_field_type(self, field_name):
        if (self.has_field(field_name)[0]):
            return self.fields.get(field_name)


    def check_if_overide_methods_valid(self, method_object):
        method_name = method_object.get_name()
        overrided_methods = self.methods[method_name]
        method_object_types = list(method_object.get_params().values())
        for method in overrided_methods:
            if method == method_object:
                continue
            if method.get_param_number == method_object.get_param_number():
                method_types = list(method.get_params().values())
                for type in range(len(method_types)):
                    if method_types[type] != method_object_types[type]:
                        return
                print(f"All parameters are the same type within overided methods '{method.get_method_with_version()}' and '{method_object.get_method_with_version()}'")
                exit(0)

    def search_method(self, method_name, param_num):

        methods_with_name = self.methods.get(method_name)
        
        inherited = None

        if methods_with_name == None:
            inherited = self.search_method_in_inherited_classes( method_name, param_num)

            if (inherited == None):
                print(f"Method '{method_name}' is not declared in class '{self.name}'")
                exit(0)
        if methods_with_name != None:
            for method in methods_with_name:
                
                if method.param_number == param_num + 1:
                    if method.is_constructor:
                        return [str(method.version) + "$init", None]                
                    return [method.version, None]
        elif (inherited != None):
            return inherited
        else:
            print(f"Method '{method_name}' with parameter number '{param_num}' is not declared in class '{self.name}'")
            exit(0)
    
    def search_method_in_inherited_classes(self, method_name, param_num):
        for inherited_class in self.inherits_from:
            methods_of_class = inherited_class.methods.get(method_name)
            
            if methods_of_class != None:
                for method in methods_of_class:
                    if method.param_number == param_num + 1:
                        return [method.version, inherited_class]
        
        return None
    
    def add_inheritage_class(self, class_object):
        self.inherits_from.append(class_object)
    
    def search_field_in_inherited_classes(self, field_name):
        
        # returns class object of the inherited class that has the field declared or none 
        # if not found. none used to know if field is not found either on current class or parent classes 
        for inherited_class in self.inherits_from:
            if inherited_class.has_field(field_name)[0]:
                return inherited_class
        
        return None
    

    def __str__(self):
        inheritance_str = ', '.join([parent.name for parent in self.inherits_from])
        
        all_classes = [cls for classes_list in self.methods.values() for cls in classes_list]
        methods_str = '\n  '.join([str(method) for method in all_classes])
        fields_str = ', '.join([f"{name}: {type_}" for name, type_ in self.fields.items()])
        
        return f"Class name: {self.name}\nFields: [{fields_str}]\nInherits from: [{inheritance_str}]\nMethods:{methods_str}"