class Encloser:
    pass

class Encloser:
    def __init__(self,  encloser_number:int,  size:int) -> None:
        self.encloser_number = encloser_number
        self.size = size
        self.coordinates = None

    def set_coordinate(self, coordinates:list(tuple(int, int))) -> Encloser:
        self.coordinates =  coordinates
        return self