class Factory:
    pass

class A:
    def __init__(self, object_arg1, object_arg2=None):
        pass

class TestFactory(Factory):

    def __init__(self, fact_field1:int, fact_field2=None, fact_field3=2):

        self._fact_field = {"fact_field1": fact_field1, "fact_field2": fact_field2}

    def get_some_obj(self, arg1, arg2=5, arg3:int=None):

        b = A(arg1,arg2)
        return b
