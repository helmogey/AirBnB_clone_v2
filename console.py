#!/usr/bin/python3
""" consol.py defines HBNBCommand class"""
import cmd
import json
import sys
import re
from models import storage
from models.base_model import BaseModel

def check_float(x):
    """Checks if `x` is float.
    """
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True

def check_int(x):
    """Checks if `x` is int.
    """
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

def parse_args(arg):
    """Parse `arg` to an `int`, `float` or `string`.
    """
    parsed = re.sub("\"", "", arg)

    if check_int(parsed):
        return int(parsed)
    elif check_float(parsed):
        return float(parsed)
    else:
        return arg

def validate_args(args):
    """Runs checks on args to validate classname attributes and values.
    """
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True

class HBNBCommand(cmd.Cmd):
    """Console for HBNB project"""

    prompt = '(hbnb) '
    classes = {"BaseModel", "User", "State", "City",
               "Amenity", "Review", "Place"}
    # file_path = "file.json"
    file_storage = storage

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")
        return True

    def do_help(self, arg):
        """Display help about commands"""
        super().do_help(arg)

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass


    def do_create(self, args):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id.
        If the class name is missing, print ** class name missing **
        If the class name doesn't exist, print ** class doesn't exist **
        """
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kw = {}
            for arg in arg_list[1:]:
                arg_splited = arg.split("=")
                arg_splited[1] = eval(arg_splited[1])
                if type(arg_splited[1]) is str:
                    arg_splited[1] = arg_splited[1].replace("_", " ").replace('"', '\\"')
                kw[arg_splited[0]] = arg_splited[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_instance = HBNBCommand.classes[arg_list[0]](**kw)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        args = args.split()
        if args == "":
            print("** class name missing **")
        if args[0] not in self.classes:
            print("** class doesn't exist **")
        if len(args) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])
            try:
                obj = objects[key]
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id (save the change into the JSON file)"""
        if not args:
            print("** class name missing **")
            return

        try:
            class_name, id_ = args.split()
            class_ = eval(class_name)
            if not issubclass(class_, BaseModel):
                print("** class doesn't exist **")
                return
            if not id_:
                print("** instance id missing **")
                return
            key = f"{class_.__name__}.{id_}"
            if key not in self.file_storage.__objects:
                print("** no instance found **")
                return
            del self.file_storage.__objects[key]
            self.file_storage.save()
        except Exception as e:
            print("** class doesn't exist **")

    def do_all(self, args):
        """Prints all string representation of all instances based or not on the class name"""
        objects = storage.all()
        list = []
        if not args:
            for name in objects.keys():
                obj = objects[name]
                list.append(str(obj))
            return
        args = args.split(" ")
        if args[0] in self.classes:
            for name in objects:
                if name[0:len(args[0])] == args[0]:
                    obj = objects[name]
                list.append(str(obj))
        else:
            print("** class doesn't exist **")
            return

    def do_update(self, arg: str):
        """Updates an instance based on the class name and id.
        """
        args = arg.split(maxsplit=3)
        if args[0] not in self.classes:
            print("** class doesn't exist **")

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        match_json = re.findall(r"{.*}", arg)
        if match_json:
            payload = None
            try:
                payload: dict = json.loads(match_json[0])
            except Exception:
                print("** invalid syntax")
                return
            for k, v in payload.items():
                setattr(req_instance, k, v)
            storage.save()
            return
        if not validate_args(args):
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if first_attr:
            setattr(req_instance, args[2], first_attr[0])
        else:
            value_list = args[3].split()
            setattr(req_instance, args[2], parse_args(value_list[0]))
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
