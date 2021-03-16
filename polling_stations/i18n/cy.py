MUTATIONS = {
    "aspirate": {"c": "ch", "p": "ph", "t": "th"},
    "nasal": {"c": "ngh", "p": "mh", "t": "nh", "g": "ng", "b": "m", "d": "n"},
    "soft": {
        "c": "g",
        "p": "b",
        "t": "d",
        "g": "",
        "b": "f",
        "d": "dd",
        "rh": "r",
        "m": "f",
        "ll": "l",
    },
}


class WelshNameMutationMixin:
    def name_with_welsh_mutation(self, mutation):
        if "cy" in self.name_translated:
            name: str = self.name_translated["cy"]
            name_lower = name.lower()
            for original, mutated in MUTATIONS[mutation].items():
                if name_lower.startswith(original):
                    if name[0].isupper():
                        mutated = mutated.title()
                    return mutated + name[len(original) :]
            return name
        else:
            return str(self)
