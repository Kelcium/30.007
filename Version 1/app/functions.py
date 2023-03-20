class Passenger(passenger):

    def __init__(self, passenger):
        self.luggage_queue = passenger.luggage
        self.name = passenger.name
        pass

    @property
    def is_empty(self):
        return self.luggage_queue == []

    @property
    def name(self):
        return self.name

    @property
    def luggage_queue(self):
        return self.luggage_queue
