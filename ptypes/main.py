import re
import ptypes.formulas as formulas
from pprint import pprint
from copy import deepcopy


class InvalidTypeException(Exception):
    pass


class InvalidOctagramException(Exception):
    pass


Types: dict[str, "Type"] = {}
Octagrams: dict[str, "Octagram"] = {}


class Octagram:
    def __new__(cls, octagram, _initializing=False):
        if isinstance(octagram, str):
            octagram = octagram.upper()
        elif isinstance(octagram, Octagram):
            return octagram
        if octagram not in Octagrams:
            if not _initializing:
                raise InvalidOctagramException(f"octagram {octagram} is not valid.")
            if Octagrams.get(octagram) is None:
                Octagrams[octagram] = super().__new__(cls)
        return Octagrams[octagram]

    def __init__(self, octagram: str, *args, **kwargs):
        octagram = octagram.upper()
        if octagram in ["SDSF", "SDUF", "UDSF", "UDUF"]:
            self.octagram = octagram
        else:
            raise InvalidTypeException(f"Bad octagram {octagram}")
        self.development = octagram[:2]
        self.focus = octagram[2:]

    def get_attributes(self):
        return {self.development, self.focus}

    def __str__(self):
        return self.octagram

    def __repr__(self):
        return f"ptypes.Octagram('{self.octagram}')"


class Type:
    """Represents a personality type and all its attributes.

    ```
    Type("ESTP")
    >>> ESTP
    Type("ESTP").E
    >>> True
    ```"""

    def __new__(cls, ptype, _initializing=False, _clone=False):
        if isinstance(ptype, str):
            ptype = ptype.upper()
        elif isinstance(ptype, Type):
            return ptype
        if _clone:
            return super().__new__(cls)
        if ptype not in Types:
            if not _initializing:
                raise InvalidTypeException(f"ptype {type} is not valid.")
            if Types.get(ptype) is None:
                Types[ptype] = super().__new__(cls)
        return Types[ptype]

    def clone(self):
        res = Type(self.type, _clone=True)
        res.octagram = self.octagram
        return res

    def __init__(self, type: str, *args, **kwargs):
        if hasattr(self, "type"):
            return

        self.type = type
        self.octagram = None
        self.E = "E" == type[0]
        self.S = "S" == type[1]
        self.T = "T" == type[2]
        self.J = "J" == type[3]
        self.I = not self.E
        self.N = not self.S
        self.F = not self.T
        self.P = not self.J
        self.Si = self.calc_formula("NP|SJ")
        self.Ne = self.calc_formula("Si")
        self.Se = self.calc_formula("!Si")
        self.Ni = self.calc_formula("Se")
        self.Ti = self.calc_formula("FJ|TP")
        self.Fe = self.calc_formula("Ti")
        self.Te = self.calc_formula("!Ti")
        self.Fi = self.calc_formula("Te")

        self.Crusader = self.calc_formula("SiTi")
        self.Templar = self.calc_formula("SeTi")
        self.Wayfarer = self.calc_formula("SeTe")
        self.Philosopher = self.calc_formula("SiTe")
        self.Quadra = (
            "Crusader"
            if self.Crusader
            else "Templar"
            if self.Templar
            else "Wayfarer"
            if self.Wayfarer
            else "Philosopher"
        )

        self.Structure = self.calc_formula("E&(ST|NJ)")
        self.Starter = self.calc_formula("E&(SF|NP)")
        self.Finisher = self.calc_formula("I&(ST|NJ)")
        self.Background = self.calc_formula("I&(SF|NP)")
        self.Interaction_style = (
            "Structure"
            if self.Structure
            else "Starter"
            if self.Starter
            else "Finisher"
            if self.Finisher
            else "Background"
        )
        self.Initiating = self.calc_formula("E")
        self.Responding = self.calc_formula("I")
        self.Direct = self.calc_formula("ST|NJ")
        self.Informative = self.calc_formula("SF|NP")
        self.Progression = self.calc_formula("ESF|IST|ENP|INJ")
        self.Outcome = self.calc_formula("EST|ISF|ENJ|INP")

        self.Guardian = self.calc_formula("SJ")
        self.Artisan = self.calc_formula("SP")
        self.Intellectual = self.calc_formula("NT")
        self.Idealist = self.calc_formula("NF")
        self.Temperament = (
            "Guardian"
            if self.Guardian
            else "Artisan"
            if self.Artisan
            else "Intellectual"
            if self.Intellectual
            else "Idealist"
        )
        self.Concrete = self.calc_formula("S")
        self.Abstract = self.calc_formula("N")
        self.Systematic = self.calc_formula("SJ|NT")
        self.Interest = self.calc_formula("SP|NF")
        self.Pragmatic = self.calc_formula("SP|NT")
        self.Affiliative = self.calc_formula("SJ|NF")

        self.ES = self.calc_formula("ES")
        self.EN = self.calc_formula("EN")
        self.IS = self.calc_formula("IS")
        self.IN = self.calc_formula("IN")
        self.ET = self.calc_formula("ET")
        self.EF = self.calc_formula("EF")
        self.IT = self.calc_formula("IT")
        self.IF = self.calc_formula("IF")
        self.EJ = self.calc_formula("EJ")
        self.EP = self.calc_formula("EP")
        self.IJ = self.calc_formula("IJ")
        self.IP = self.calc_formula("IP")
        self.ST = self.calc_formula("ST")
        self.SF = self.calc_formula("SF")
        self.NJ = self.calc_formula("NJ")
        self.NP = self.calc_formula("NP")
        self.TJ = self.calc_formula("TJ")  # Direct
        self.TP = self.calc_formula("TP")  # Prag
        self.FJ = self.calc_formula("FJ")  # Affil
        self.FP = self.calc_formula("FP")  # Informative

        self.Abstract_temple = self.calc_formula("EP|IJ")
        self.Concrete_temple = self.calc_formula("EJ|IP")
        self.Pragmatic_temple = self.calc_formula("SF|NT")
        self.Affiliative_temple = self.calc_formula("ST|NF")
        self.Soul = self.calc_formula("Abstract_templeAffiliative_temple")
        self.Heart = self.calc_formula("Abstract_templePragmatic_temple")
        self.Body = self.calc_formula("Concrete_templePragmatic_temple")
        self.Mind = self.calc_formula("Concrete_templeAffiliative_temple")
        self.Temple = (
            "Soul"
            if self.Soul
            else "Heart"
            if self.Heart
            else "Body"
            if self.Body
            else "Mind"
        )

        self.Intimacy = self.calc_formula("SoulTemplar")
        self.Justification = self.calc_formula("SoulPhilosopher")
        self.Satisfaction = self.calc_formula("HeartCrusader")
        self.Reverence = self.calc_formula("HeartWayfarer")
        self.Validation = self.calc_formula("MindTemplar")
        self.Authority = self.calc_formula("MindPhilosopher")
        self.Discovery = self.calc_formula("BodyCrusader")
        self.Purpose = self.calc_formula("BodyWayfarer")

        self.attr_1 = self.calc_formula("ET|SF")
        self.attr_2 = self.calc_formula("IT|NF")
        self.attr_3 = self.calc_formula("ET|NF")
        self.attr_4 = self.calc_formula("SF|IT")
        self.attr_5 = self.calc_formula("ST|EF")
        self.attr_6 = self.calc_formula("NT|IF")
        self.attr_7 = self.calc_formula("ST|IF")
        self.attr_8 = self.calc_formula("EF|NT")
        self.attr_9 = self.calc_formula("STJ|EFJ|NTP|IFP")
        self.attr_10 = self.calc_formula("STP|NTJ|EFP|IFJ")
        self.attr_11 = self.calc_formula("ETJ|SFJ|ITP|NFP")
        self.attr_12 = self.calc_formula("ETP|SFP|ITJ|NFJ")
        self.attr_13 = self.calc_formula("EFJ|STP|NTJ|IFP")
        self.attr_14 = self.calc_formula("STJ|EFP|NTP|IFJ")
        self.attr_15 = self.calc_formula("ETJ|SFP|ITP|NFJ")
        self.attr_16 = self.calc_formula("ETP|SFJ|ITJ|NFP")
        self.x = self.calc_formula("ST|NP")
        self.y = self.calc_formula("SF|NJ")
        self.w = self.calc_formula("ESJ|ENT|ISP|INF")
        self.z = self.calc_formula("ESP|ENF|ISJ|INT")
        self.p = self.calc_formula("ESF|ENJ|IST|INP")
        self.q = self.calc_formula("EST|ENP|ISF|INJ")

    def update_relationships(self):
        self.unconscious = self.convert(0b1001)
        self.silver = self.convert(0b0001)
        self.natural = self.convert(0b1110)
        self.superego = self.convert(0b0110)

        self.pedagogue = self.convert(0b1011)
        self.trust = self.convert(0b0011)
        self.intrigue = self.convert(0b1100)
        self.kindred = self.convert(0b0100)

        self.partnership = self.convert(0b1101)
        self.compliance = self.convert(0b0101)
        self.prudent = self.convert(0b1010)
        self.kinship = self.convert(0b0010)

        self.subconscious = self.convert(0b1111)
        self.conflict = self.convert(0b0111)
        self.sister = self.convert(0b1000)
        self.ego = self

    def calc_formula(self, formula):
        formula = formulas.format(formula)
        for var in formulas.VAR_REGEX.findall(formula):
            if getattr(self, var) is None:
                raise InvalidTypeException(f"Attribute {var} is not valid.")
            formula = re.sub(rf"\b{var}\b", str(getattr(self, var)), formula)
        return eval(formula)

    def get_attributes(self) -> set:
        res = {
            k for k, v in self.__dict__.items() if v is True and not k.startswith("_")
        }
        if self.octagram:
            res = res | self.octagram.get_attributes()
        return res

    def get_relationships(self) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if isinstance(v, Type) and not k.startswith("_")
        }

    def convert(self, conversion: int) -> "Type":
        """Converts the type to another type based on the conversion number.
        The conversion number is 4 bits

        ```
        ESTP.convert(0b1111)
        >>> INFJ
        ESTP.convert('0001')
        >>> ESTJ
        ```"""
        if isinstance(conversion, str):
            conversion = int(conversion, 2)
        if not isinstance(conversion, int) or conversion < 0 or conversion > 15:
            raise ValueError("Invalid input. Must be an integer between 0-15.")
        conversion_bin = bin(conversion)[2:].zfill(4)
        E = self.E ^ bool(int(conversion_bin[-4]))
        S = self.S ^ bool(int(conversion_bin[-3]))
        T = self.T ^ bool(int(conversion_bin[-2]))
        J = self.J ^ bool(int(conversion_bin[-1]))
        return Type(
            ("E" if E else "I")
            + ("S" if S else "N")
            + ("T" if T else "F")
            + ("J" if J else "P")
        )

    def set_octagram(self, octagram: Octagram) -> "Type":
        if not isinstance(octagram, Octagram):
            octagram = Octagram(octagram)
        self = self.clone()
        self.octagram = octagram
        return self

    def __str__(self):
        if self.octagram:
            return f"{self.type} {self.octagram}"
        return self.type

    def __repr__(self):
        base = f"ptypes.Type('{self.type}')"
        if self.octagram:
            base += f".set_octagram({self.octagram.__repr__()})"

        return base


def _check_duplicates():
    """This function is to make sure we don't
    create duplicate attributes in the future

    It will raise an exception if we do"""
    skip_attributes = [
        # These attributes have duplicates by design
        # Ensure that we only skip 1 of the N duplicates
        # So that we can still detect duplicates
        # If they appear in the future
        "Abstract",
        "Concrete",
        "Initiating",
        "Responding",
        "Ni",
        "Ne",
        "Ti",
        "Te",
    ]
    _attributes = {}
    for type_value, type in enumerate(Types):
        type_value = 2**type_value
        for attr in Type(type).get_attributes():
            if attr in skip_attributes:
                continue
            if attr not in _attributes:
                _attributes[attr] = type_value
            else:
                _attributes[attr] += type_value
    duplicates = {
        k: v
        for k, v in _attributes.items()
        if len([x for x in _attributes.values() if x == v]) > 1
    }
    if len(duplicates):
        groups = {}
        for k, v in duplicates.items():
            groups.setdefault(format(v, "016b"), []).append(k)
        pprint(groups)
        raise Exception("Duplicates found in attributes.")


ESTJ = Type("ESTJ", _initializing=True)
ESTP = Type("ESTP", _initializing=True)
ENTJ = Type("ENTJ", _initializing=True)
ENFJ = Type("ENFJ", _initializing=True)
ESFJ = Type("ESFJ", _initializing=True)
ESFP = Type("ESFP", _initializing=True)
ENTP = Type("ENTP", _initializing=True)
ENFP = Type("ENFP", _initializing=True)
ISTJ = Type("ISTJ", _initializing=True)
ISTP = Type("ISTP", _initializing=True)
INTJ = Type("INTJ", _initializing=True)
INFJ = Type("INFJ", _initializing=True)
ISFJ = Type("ISFJ", _initializing=True)
ISFP = Type("ISFP", _initializing=True)
INTP = Type("INTP", _initializing=True)
INFP = Type("INFP", _initializing=True)

SDSF = Octagram("SDSF", _initializing=True)
SDUF = Octagram("SDUF", _initializing=True)
UDSF = Octagram("UDSF", _initializing=True)
UDUF = Octagram("UDUF", _initializing=True)

for type in Types:
    Type(type)
for type in Types:
    Type(type).update_relationships()

_check_duplicates()
