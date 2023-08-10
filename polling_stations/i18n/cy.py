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


class WelshMutationContextHelper:
    __slots__ = ("context", "key", "mutation")

    def __init__(self, context, key, mutation):
        self.context = context
        self.key = key
        self.mutation = mutation

    def __str__(self):
        # Mirroring i18n.BlockTranslateNode.render.render_value. We are slightly stymied
        # in that this is the only point we have late enough in the rendering process to
        # provide the custom representation, but that we have to return a string
        # (because this is a __str__ method). Because of this we have to include the
        # default_value functionality again.
        try:
            return self.context[self.key].name_with_welsh_mutation(self.mutation)
        except KeyError:
            default_value = self.context.template.engine.string_if_invalid
            return default_value % self.key if "%s" in default_value else default_value
        except AttributeError:
            return str(self.context[self.key])


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
        return str(self)
