class SimuObject:

    def __init__(self,movable):
        self.movable = movable
        #TODO
        pass


class Cube(SimuObject):

    def __init__(self, size):
        super().__init__(True)
        self.size = size

        #TODO
        pass
