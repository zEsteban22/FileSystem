from abc import ABCMeta, abstractmethod

class Interface(metaclass=ABCMeta):
    @abstractmethod
    def do_something(self):
        pass

class Implementation(Interface):
    def do_other_something(self):
        print("Implementation")

try:
    i = Implementation()
    i.do_something()
except Exception as e:
    print("No se puede instanciar una clase con un método abstracto")