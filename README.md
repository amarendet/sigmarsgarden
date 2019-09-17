# Solver for Sigmar's Garden in Opus Magnum

This is a solver for the small game Sigmar's Garden from Opus Magnum.

It consists of a single Python3 script: `sigmar.py`.

Input the puzzle by changing the variable LINES in the script, for example:

```python
LINES = [
    "teata4",
    "hhoooem",
    "aoaooeof",
    "eooaahooe",
    "vootoosoom",
    "efefo6ofm2v",
    "hoofooaooa",
    "vooftsoo1",
    "sovoofot",
    "tmooos5",
    "tfe3ht",
]
```

The correspondance between element and character is in the variable `CHAR_TO_ELEM`:

```python
CHAR_TO_ELEM = {
    "o": Element.VOID,
    "f": Element.FIRE,
    "t": Element.EARTH,
    "e": Element.WATER,
    "a": Element.AIR,
    "s": Element.SALT,
    "v": Element.LIFE,
    "m": Element.DEATH,
    "h": Element.MERCURY,
    "1": Element.LEAD,
    "2": Element.TIN,
    "3": Element.IRON,
    "4": Element.COPPER,
    "5": Element.SILVER,
    "6": Element.GOLD,
}
```

Change it to you preferences !

Then, just run the script on the command line, it will output a path like this:

```text
(10, 5) Element.EARTH (10, 0) Element.EARTH
(0, 0) Element.EARTH (9, 0) Element.EARTH
(0, 1) Element.WATER (5, 0) Element.WATER
(5, 10) Element.LIFE (9, 1) Element.DEATH
(0, 2) Element.AIR (6, 9) Element.AIR
(8, 2) Element.LIFE (4, 9) Element.DEATH
(10, 1) Element.FIRE (7, 3) Element.FIRE
(7, 4) Element.EARTH (0, 3) Element.EARTH
(7, 5) Element.SALT (8, 0) Element.SALT
(6, 3) Element.FIRE (8, 5) Element.FIRE
(10, 2) Element.WATER (3, 8) Element.WATER
(2, 7) Element.FIRE (5, 3) Element.FIRE
(0, 4) Element.AIR (6, 6) Element.AIR
(4, 0) Element.LIFE (1, 6) Element.DEATH
(5, 1) Element.FIRE (5, 7) Element.FIRE
(4, 6) Element.SALT (9, 5) Element.SALT
(3, 0) Element.WATER (5, 2) Element.WATER
(7, 0) Element.LIFE (5, 8) Element.DEATH
(7, 8) Element.LEAD (10, 4) Element.MERCURY
(4, 3) Element.EARTH (8, 7) Element.EARTH
(2, 0) Element.AIR (3, 3) Element.AIR
(3, 4) Element.AIR (2, 2) Element.AIR
(5, 9) Element.TIN (3, 5) Element.MERCURY
(10, 3) Element.IRON (6, 0) Element.MERCURY
(0, 5) Element.COPPER (1, 1) Element.MERCURY
(2, 5) Element.WATER (1, 5) Element.WATER
(9, 6) Element.SILVER (1, 0) Element.MERCURY
(5, 5) Element.GOLD (5, 5) Element.GOLD
```

In `(10, 5)`, for example, the first number is the line on the board and the second number the offset from the beginning of the line.

Enjoy!
