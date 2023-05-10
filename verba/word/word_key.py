import verba.word.definitions as definitions

class WordKey:
    def __init__(self, *args, only=None):
        self.attributes = {}
        for arg in args:
            if arg not in definitions.value_to_attribute:
                continue

            attr_name = definitions.value_to_attribute[arg]
            if attr_name in self.attributes:
                raise ValueError(f'Provided two arguments for the attribute {attr_name}')

            if only and attr_name not in only:
                continue

            self.attributes[attr_name] = arg

    def union(self, other):
        return WordKey(*(other.attributes | self.attributes).values()) 

    def __repr__(self):
        pairs = sorted(self.attributes.items(), key=lambda x: definitions.key_order.index(x[0]))
        values = [x[1] for x in pairs]
        values_str = ', '.join(values)
        return f'({values_str})'

    def __getitem__(self, i):
        if i not in self.attributes:
            return None

        return self.attributes[i]

    def __hash__(self):
        return hash(tuple(sorted(self.attributes)))

    def __eq__(self, other):
        return self.attributes == other.attributes



