# ptypes

Standard python package for personality types

Example Usage
```sh
pip install git+https://github.com/Psight-Limited/ptypes.git
```
Getting personality type objects
```py
>>> from ptypes import *

>>> ENTP
Type('ENTP')

>>> Type('ENTP')
Type('ENTP')

```
Attributes
```py
>>> ENTP.get_attributes()
['E', 'T', 'N', 'P', 'Si', 'Ne', 'Ti', 'Fe', 'Crusader', 'Starter', 'Initiating', 'Informative', 'Progression', 'Intellectual', 'Abstract', 'Systematic', 'Pragmatic', 'EN', 'ET', 'EP', 'NP', 'TP', 'Abstract_temple', 'Pragmatic_temple', 'Heart', 'attr_1', 'attr_3', 'attr_6', 'attr_8', 'attr_9', 'attr_12', 'attr_14', 'attr_16', 'x', 'w', 'q']

>>> ENTP.Direct
False
```
Conversions
```py
>>> ENTP.subconscious
Type('ISFJ')

>>> ENTP.subconscious.Direct
False

>>> ENTP.subconscious.get_attributes()
['S', 'J', 'I', 'F', 'Si', 'Ne', 'Ti', 'Fe', 'Crusader', 'Background', 'Responding', 'Informative', 'Outcome', 'Guardian', 'Concrete', 'Systematic', 'Affiliative', 'IS', 'IF', 'IJ', 'SF', 'FJ', 'Abstract_temple', 'Pragmatic_temple', 'Heart', 'attr_1', 'attr_4', 'attr_6', 'attr_7', 'attr_10', 'attr_11', 'attr_14', 'attr_16', 'y', 'z', 'q']
```
Calculating vectors
```py
>>> ENTP.calc_formula("EP|IJ") # This calculates if they have an (E and P) or (I and J)
True
```
