from pprint import pprint as print
from enum import Enum
from copy import deepcopy


class Types(Enum):
    ESTJ = 0
    ESTP = 1
    ENTJ = 2
    ENFJ = 3
    ESFJ = 4
    ESFP = 5
    ENTP = 6
    ENFP = 7
    ISTJ = 8
    ISTP = 9
    INTJ = 10
    INFJ = 11
    ISFJ = 12
    ISFP = 13
    INTP = 14
    INFP = 15


class Quadras(Enum):
    crusader = 0
    templar = 1
    wayfarer = 2
    philosopher = 3


attributes_dictionary = {
    "expression": [
        ["structure", "in_charge", "DIC"],
        ["starter", "get_things_going"],
        ["finisher", "chart_the_course"],
        ["background", "behind_the_scenes"],
        #
        ["direct"],
        ["informative"],
        ["initiating", "extrovert", "E"],
        ["responding", "introvert", "I"],
        ["outcome", "control"],
        ["progression", "movement"],
    ],
    "worldview": [
        ["guardian", "SJ"],
        ["artistan", "SP"],
        ["intellectual", "NT"],
        ["idealist", "NJ"],
        #
        ["concrete", "sensor", "S"],
        ["affiliative"],
        ["systematic"],
        ["abstract", "intuitive", "N"],
        ["pragmatic"],
        ["interest"],
    ],
    "quadra": [
        ["crusader", "alpha"],
        ["templar", "beta"],
        ["wayfarer", "gamma"],
        ["philosopher", "delta"],
        #
        ["earthwater", "earth", "water", "waterearth", "si", "ne", "nesi", "sine"],
        ["swordmace", "sword", "mace", "macesword", "ti", "fe", "tife", "feti"],
        ["firewind", "fire", "wind", "windfire", "se", "ni", "seni", "nise"],
        ["spearbow", "spear", "bow", "bowspear", "te", "fi", "tefi", "fite"],
    ],
    "temple": [
        ["soul"],
        ["heart"],
        ["body"],
        ["mind"],
    ],
    "origin": [
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
}

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
    "ESTJ": ["ESTJ", "structure", "guardian", "philosopher", "mind", "authority"],
    "ESTP": ["ESTP", "structure", "artistan", "templar", "soul", "intimacy"],
    "ENTJ": ["ENTJ", "structure", "intellectual", "wayfarer", "body", "purpose"],
    "ENFJ": ["ENFJ", "structure", "idealist", "templar", "mind", "validation"],
    "ESFJ": ["ESFJ", "starter", "guardian", "crusader", "body", "discovery"],
    "ESFP": ["ESFP", "starter", "artistan", "wayfarer", "heart", "reverance"],
    "ENTP": ["ENTP", "starter", "intellectual", "crusader", "heart", "satisfaction"],
    "ENFP": ["ENFP", "starter", "idealist", "philosopher", "soul", "justification"],
    "ISTJ": ["ISTJ", "finisher", "guardian", "philosopher", "soul", "justification"],
    "ISTP": ["ISTP", "finisher", "artistan", "templar", "mind", "validation"],
    "INTJ": ["INTJ", "finisher", "intellectual", "wayfarer", "heart", "reverance"],
    "INFJ": ["INFJ", "finisher", "idealist", "templar", "soul", "intimacy"],
    "ISFJ": ["ISFJ", "background", "guardian", "crusader", "heart", "satisfaction"],
    "ISFP": ["ISFP", "background", "artistan", "wayfarer", "body", "purpose"],
    "INTP": ["INTP", "background", "intellectual", "crusader", "body", "discovery"],
    "INFP": ["INFP", "background", "idealist", "philosopher", "mind", "authority"],
}


class Type:
    def __init__(self, type_: Types):
        if type_ in list(Types):
            type_ = type_.name
        type_ = type_.upper()
        if type_ not in [x.name for x in list(Types)]:
            raise

        has_attributes = deepcopy(_types_dict)[type_]
        for v in [_ for _ in has_attributes]:
            has_attributes += deepcopy(_types_dict).get(v, [])

        for catagory, groups in attributes_dictionary.items():
            for attributes in groups[::-1]:
                x = set(has_attributes) & set(attributes)
                if len(x):
                    exec(f"self.{catagory} = {repr(attributes[0])}")
                    for i in attributes:
                        exec(f"self.{i} = True")
                        if i not in has_attributes:
                            has_attributes += [i]
                else:
                    for i in attributes:
                        exec(f"self.{i} = False")

        self.attributes = list(set(has_attributes))
        self.type = type_
        self.quadra: Quadras = Quadras[self.quadra]

        if True:
            self.expression = self.expression
            self.progression = self.progression
            self.movement = self.movement
            self.outcome = self.outcome
            self.control = self.control
            self.responding = self.responding
            self.introvert = self.introvert
            self.I = self.I
            self.initiating = self.initiating
            self.extrovert = self.extrovert
            self.E = self.E
            self.informative = self.informative
            self.direct = self.direct
            self.background = self.background
            self.behind_the_scenes = self.behind_the_scenes
            self.finisher = self.finisher
            self.chart_the_course = self.chart_the_course
            self.starter = self.starter
            self.get_things_going = self.get_things_going
            self.structure = self.structure
            self.in_charge = self.in_charge
            self.DIC = self.DIC
            self.interest = self.interest
            self.worldview = self.worldview
            self.pragmatic = self.pragmatic
            self.abstract = self.abstract
            self.intuitive = self.intuitive
            self.systematic = self.systematic
            self.affiliative = self.affiliative
            self.concrete = self.concrete
            self.sensor = self.sensor
            self.S = self.S
            self.idealist = self.idealist
            self.NJ = self.NJ
            self.intellectual = self.intellectual
            self.NT = self.NT
            self.artistan = self.artistan
            self.SP = self.SP
            self.guardian = self.guardian
            self.SJ = self.SJ
            self.spearbow = self.spearbow
            self.spear = self.spear
            self.bow = self.bow
            self.bowspear = self.bowspear
            self.te = self.te
            self.fi = self.fi
            self.tefi = self.tefi
            self.fite = self.fite
            self.firewind = self.firewind
            self.fire = self.fire
            self.wind = self.wind
            self.windfire = self.windfire
            self.se = self.se
            self.ni = self.ni
            self.seni = self.seni
            self.nise = self.nise
            self.quadra = self.quadra
            self.swordmace = self.swordmace
            self.sword = self.sword
            self.mace = self.mace
            self.macesword = self.macesword
            self.ti = self.ti
            self.fe = self.fe
            self.tife = self.tife
            self.feti = self.feti
            self.earthwater = self.earthwater
            self.earth = self.earth
            self.water = self.water
            self.waterearth = self.waterearth
            self.si = self.si
            self.ne = self.ne
            self.nesi = self.nesi
            self.sine = self.sine
            self.philosopher = self.philosopher
            self.delta = self.delta
            self.wayfarer = self.wayfarer
            self.gamma = self.gamma
            self.templar = self.templar
            self.beta = self.beta
            self.crusader = self.crusader
            self.alpha = self.alpha
            self.mind = self.mind
            self.body = self.body
            self.temple = self.temple
            self.heart = self.heart
            self.soul = self.soul
            self.validation = self.validation
            self.origin = self.origin
            self.satisfaction = self.satisfaction
            self.reverance = self.reverance
            self.purpose = self.purpose
            self.justification = self.justification
            self.intimacy = self.intimacy
            self.discovery = self.discovery
            self.authority = self.authority
            self.INFP = self.INFP
            self.INTP = self.INTP
            self.ISFP = self.ISFP
            self.ISFJ = self.ISFJ
            self.INFJ = self.INFJ
            self.INTJ = self.INTJ
            self.ISTP = self.ISTP
            self.ISTJ = self.ISTJ
            self.ENFP = self.ENFP
            self.ENTP = self.ENTP
            self.ESFP = self.ESFP
            self.ESFJ = self.ESFJ
            self.ENFJ = self.ENFJ
            self.ENTJ = self.ENTJ
            self.ESTP = self.ESTP
            self.ESTJ = self.ESTJ
            self.attributes = self.attributes
            self.type = self.type

    def subconsious(self):
        return Type(type_conversion(self.type, 0b1111))

    def unconsious(self):
        return Type(type_conversion(self.type, 0b1001))

    def superego(self):
        return Type(type_conversion(self.type, 0b0110))

    def __call__(self) -> str:
        return self.type

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return self.type

    def to_dict(self) -> dict:
        return {x: y for x, y in vars(self).items() if x[0] != "_"}


def type_conversion(type_: str, conv) -> str:
    if type(conv) == int:
        if conv > 15 or conv < 0:
            raise
        conv = f"0000{bin(conv)[2:]}"[-4:]
    if type(conv) != str:
        raise
    if len(conv) != 4:
        raise

    base = "ESTJ"
    base_inv = "INFP"
    type_binary = ""
    for i in range(4):
        type_binary += str(int(base[i] == type_[i]))
    out_binary = ""
    for i in range(4):
        if int(conv[i]):
            out_binary += str(1 - int(type_binary[i]))
        else:
            out_binary += str(int(type_binary[i]))
    out = ""
    for i in range(4):
        if int(out_binary[i]):
            out += base[i]
        else:
            out += base_inv[i]
    return out


def main():
    type_ = Type(Types.ESFP)
    type_

    type_ = type_.superego().subconsious()
    print(type_.attributes)


if __name__ == "__main__":
    main()
