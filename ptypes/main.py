import re
import ptypes.formulas as formulas


class InvalidTypeException(Exception):
    pass


Types = [
    "ESTJ", "ESTP", "ENTJ", "ENFJ", "ESFJ", "ESFP", "ENTP", "ENFP",
    "ISTJ", "ISTP", "INTJ", "INFJ", "ISFJ", "ISFP", "INTP", "INFP",
]


class Type:
    """Represents a personality type and all its attributes.

    ```
    Type("ESTP")
    >>> ESTP
    Type("ESTP").E
    >>> True
    ```"""
    _instances = {}

    def __new__(cls, type):
        if isinstance(type, str):
            type = type.upper()
        if type not in Types:
            raise InvalidTypeException(f"Type {type} is not valid.")
        if type not in cls._instances:
            cls._instances[type] = super().__new__(cls)
        return cls._instances.get(type)

    def __init__(self, type):
        if hasattr(self, "type"):
            return

        self._type = type
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
        self.Quadra = \
            "Crusader" if self.Crusader else \
            "Templar" if self.Templar else \
            "Wayfarer" if self.Wayfarer else \
            "Philosopher"

        self.Direct = self.calc_formula("ST|NJ")
        self.Informative = self.calc_formula("SF|NP")
        self.Initiating = self.calc_formula("E")
        self.Responding = self.calc_formula("I")
        self.Progression = self.calc_formula("ESF|IST|ENP|INJ")
        self.Outcome = self.calc_formula("EST|ISF|ENJ|INP")
        self.Concrete = self.calc_formula("S")
        self.Abstract = self.calc_formula("N")
        self.Systematic = self.calc_formula("SJ|NT")
        self.Interest = self.calc_formula("SP|NF")
        self.Pragmatic = self.calc_formula("SP|NT")
        self.Affiliative = self.calc_formula("SJ|NF")

        self.Abstract_temple = self.calc_formula("EP|IJ")
        self.Concrete_temple = self.calc_formula("EJ|IP")
        self.Pragmatic_temple = self.calc_formula("SF|NT")
        self.Affiliative_temple = self.calc_formula("ST|NF")
        self.Soul = self.calc_formula("Abstract_templeAffiliative_temple")
        self.Heart = self.calc_formula("Abstract_templePragmatic_temple")
        self.Body = self.calc_formula("Concrete_templePragmatic_temple")
        self.Mind = self.calc_formula("Concrete_templeAffiliative_temple")
        self.Temple = \
            "Soul" if self.Soul else \
            "Heart" if self.Heart else \
            "Body" if self.Body else \
            "Mind"

        self.attr_1 = self.calc_formula("ET|SF")
        self.attr_2 = self.calc_formula("IT|NF")
        self.attr_3 = self.calc_formula("ET|NF")
        self.attr_4 = self.calc_formula("SF|TI")
        self.attr_5 = self.calc_formula("ST|EF")
        self.attr_6 = self.calc_formula("TN|IF")
        self.attr_7 = self.calc_formula("ST|IF")
        self.attr_8 = self.calc_formula("EF|TN")
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
        #
        #
        #

        #
        #
        #
        #

        #
        #
        self.subconscious = self.convert(0b1111)
        self.ego = self

    def calc_formula(self, formula):
        formula = formulas.format(formula)
        for var in formulas.VAR_REGEX.findall(formula):
            if getattr(self, var) is None:
                raise InvalidTypeException(f"Attribute {var} is not valid.")
            formula = re.sub(rf'\b{var}\b', str(getattr(self, var)), formula)
        return eval(formula)

    def get_attributes(self) -> list:
        return [k for k, v in self.__dict__.items()
                if v is True and not k.startswith("_")]

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
        if not isinstance(conversion, int) \
                or conversion < 0 or conversion > 15:
            raise ValueError("Invalid input. Must be an integer between 0-15.")
        conversion_bin = bin(conversion)[2:].zfill(4)
        E = self.E ^ bool(int(conversion_bin[-4]))
        S = self.S ^ bool(int(conversion_bin[-3]))
        T = self.T ^ bool(int(conversion_bin[-2]))
        J = self.J ^ bool(int(conversion_bin[-1]))
        return Type(
            ("E" if E else "I") +
            ("S" if S else "N") +
            ("T" if T else "F") +
            ("J" if J else "P")
        )

    def __str__(self):
        return self._type

    def __repr__(self):
        return f"Type('{self._type}')"


def _check_duplicates():
    """This function is to make sure we don't
    create duplicate attributes in the future

    It will raise an exception if we do"""
    skip_attributes = [
        # These attributes have duplicates by design
        # Ensure that we only skip 1 of the N duplicates
        # So that we can still detect duplicates
        # If they appear in the future
        "Abstract", "Concrete",
        "Initiating", "Responding",
        "Ni", "Ne",
        "Ti", "Te",
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
    duplicates = {k: v for k, v in _attributes.items()
                  if len([x for x in _attributes.values() if x == v]) > 1}
    if len(duplicates):
        groups = {}
        for k, v in duplicates.items():
            groups.setdefault(format(v, '016b'), []).append(k)
        print(groups)
        raise Exception("Duplicates found in attributes.")


for type in Types:
    Type(type)
for type in Types:
    Type(type).update_relationships()

ESTJ = Type("ESTJ")
ESTP = Type("ESTP")
ENTJ = Type("ENTJ")
ENFJ = Type("ENFJ")
ESFJ = Type("ESFJ")
ESFP = Type("ESFP")
ENTP = Type("ENTP")
ENFP = Type("ENFP")
ISTJ = Type("ISTJ")
ISTP = Type("ISTP")
INTJ = Type("INTJ")
INFJ = Type("INFJ")
ISFJ = Type("ISFJ")
ISFP = Type("ISFP")
INTP = Type("INTP")
INFP = Type("INFP")


_check_duplicates()
