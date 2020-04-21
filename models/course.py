from models.generic import GenericModel


class Course(GenericModel):
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    def get_students(self):
        raise NotImplementedError
