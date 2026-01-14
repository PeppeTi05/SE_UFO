from dataclasses import dataclass

@dataclass
class State:
    id : str
    name : str
    capital : str
    # lat : float
    # lng : float
    # area : str
    # population : float
    # neighbors : str

    def __str__(self):
        return f'({self.id}, {self.name}, {self.capital})'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
