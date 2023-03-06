from pprint import pprint

TYPES = [
    "ESTJ",
    "ESTP",
    "ENTJ",
    "ENFJ",
    "ESFJ",
    "ESFP",
    "ENTP",
    "ENFP",
    "ISTJ",
    "ISTP",
    "INTJ",
    "INFJ",
    "ISFJ",
    "ISFP",
    "INTP",
    "INFP",
]


attributes_dictionary = (
    {
        "expression": [
            ["structure", "in_charge", "DIC"],
            ["starter", "get_things_going"],
            ["finisher", "chart_the_course"],
            ["background", "behind_the_scenes"],
            ["direct"],
            ["informative"],
            ["initiating", "extroverted", "extrovert", "E"],
            ["responding", "introverted", "introvert", "I"],
            ["outcome", "control"],
            ["progression", "movement"],
        ],
        "worldview": [
            ["guardian", "SJ"],
            ["artistan", "SP"],
            ["intellectual", "NT"],
            ["idealist", "NJ"],
            ["concrete", "sensor", "S"],
            ["affiliative"],
            ["systematic"],
            ["abstract", "intuitive", "I"],
            ["pragmatic"],
            ["interest"],
        ],
        "quadra": [
            ["crusader", "alpha"],
            ["templar", "beta"],
            ["wayfarer", "gamma"],
            ["philosopher", "delta"],
        ],
        "armament": [
            ["earthwater", "earth", "water", "waterearth", "si", "ne", "nesi", "sine"],
            ["swordmace", "sword", "mace", "macesword", "ti", "fe", "tife", "feti"],
            ["firewind", "fire", "wind", "windfire", "se", "ni", "seni", "nise"],
            ["spearbow", "spear", "bow", "bowspear", "te", "fi", "tefi", "fite"],
        ],
        "origin": [
            ["background"],
            ["finisher"],
            ["starter"],
            ["structure"],
            ["authority"],
            ["discovery"],
            ["intimacy"],
            ["justification"],
            ["purpose"],
            ["reverance"],
            ["satisfaction"],
            ["validation"],
        ],
        "type": [
            ["ESTJ"],
            ["ESTP"],
            ["ENTJ"],
            ["ENFJ"],
            ["ESFJ"],
            ["ESFP"],
            ["ENTP"],
            ["ENFP"],
            ["ISTJ"],
            ["ISTP"],
            ["INTJ"],
            ["INFJ"],
            ["ISFJ"],
            ["ISFP"],
            ["INTP"],
            ["INFP"],
        ],
    },
)


_types_dict = {
    "structure": ["direct", "initiating", "outcome"],
    "starter": ["informative", "initiating", "progression"],
    "finisher": ["direct", "responding", "progression"],
    "background": ["informative", "responding", "outcome"],
    "guardian": ["concrete", "affiliative", "systematic"],
    "artistan": ["concrete", "pragmatic", "interest"],
    "intellectual": ["abstract", "pragmatic", "systematic"],
    "idealist": ["abstract", "affiliative", "interest"],
    "crusader": ["earthwater", "swordmace"],
    "templar": ["firewind", "swordmace"],
    "wayfarer": ["firewind", "spearbow"],
    "philosopher": ["earthwater", "spearbow"],
    "ESTJ": ["structure", "guardian", "philosopher", "mind", "authority"],
    "ESTP": ["structure", "artistan", "templar", "soul", "intimacy"],
    "ENTJ": ["structure", "intellectual", "wayfarer", "body", "purpose"],
    "ENFJ": ["structure", "idealist", "templar", "mind", "validation"],
    "ESFJ": ["starter", "guardian", "crusader", "body", "discovery"],
    "ESFP": ["starter", "artistan", "wayfarer", "heart", "reverance"],
    "ENTP": ["starter", "intellectual", "crusader", "heart", "satisfaction"],
    "ENFP": ["starter", "idealist", "philosopher", "soul", "justification"],
    "ISTJ": ["finisher", "guardian", "philosopher", "soul", "justification"],
    "ISTP": ["finisher", "artistan", "templar", "mind", "validation"],
    "INTJ": ["finisher", "intellectual", "wayfarer", "heart", "reverance"],
    "INFJ": ["finisher", "idealist", "templar", "soul", "intimacy"],
    "ISFJ": ["background", "guardian", "crusader", "heart", "satisfaction"],
    "ISFP": ["background", "artistan", "wayfarer", "body", "purpose"],
    "INTP": ["background", "intellectual", "crusader", "body", "discovery"],
    "INFP": ["background", "idealist", "philosopher", "mind", "authority"],
}

labels = TYPES
id2label = {id: label for id, label in enumerate(labels)}
label2id = {label: id for id, label in enumerate(labels)}


class Type:
    def __init__(self, type_: str):
        type_ = type_.upper()
        if type_ in TYPES:
            self.type_ = type_
        else:
            raise

        attributes = []

        for k, v in _types_dict[type_].items():
            exec(f"self.{k} = {repr(v)}")
            attributes += [v]

        for k, v in self.to_dict().items():
            if v not in _types_dict:
                continue

            for k, v in _types_dict[v].items():
                exec(f"self.{k} = {repr(v)}")
                if v:
                    attributes += [k]

        self.attributes = attributes

    def __call__(self, *args, **kwds) -> str:
        return self.type_

    def __str__(self, *args, **kwds) -> str:
        return self.type_

    def to_dict(self) -> dict:
        return {x: y for x, y in vars(self).items() if x[0] != "_"}


class Side(dict):
    def __init__(self, type: str):
        self.type_ = type
        type_vectors = dict(_types_dict[type])
        for attribute in _types_dict[type].values():
            vectors = _types_dict.get(attribute)
            if vectors != None:
                for key, value in vectors.items():
                    type_vectors[key] = value
        type_vectors = {key: value for key, value in sorted(type_vectors.items())}
        for key, value in type_vectors.items():
            self[key] = value


def type_conversion(type: str, conv) -> str:
    conv = str(conv)
    base = "ESTJ"
    base_inv = "INFP"
    type_int = ""
    for i in range(4):
        type_int += str(int(base[i] == type[i]))
    out_int = ""
    for i in range(4):
        if int(conv[i]):
            out_int += str(1 - int(type_int[i]))
        else:
            out_int += str(int(type_int[i]))
    out = ""
    for i in range(4):
        if int(out_int[i]):
            out += base[i]
        else:
            out += base_inv[i]


def main():
    ptype = Type("ENTP")
    pprint(ptype)
    pprint(ptype.attributes)


if __name__ == "__main__":
    main()
