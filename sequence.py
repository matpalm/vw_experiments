class Sequence:

    def __init__(self, initial_seq=0):
        self.to_mapping = {}
        self.from_mapping = {}
        self.seq = initial_seq

    def id_for(self, thing):
        if thing in self.to_mapping:            
            return self.to_mapping[thing]
        self.to_mapping[thing] = self.seq
        self.from_mapping[self.seq] = thing
        self.seq += 1
        return self.seq - 1

    def if_from(self, tid):
        return self.from_mapping[tid]
