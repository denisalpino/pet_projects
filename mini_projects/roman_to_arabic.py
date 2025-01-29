from functools import total_ordering

@total_ordering
class RomanNumeral:
    __ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    __ARABIC = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}

    def __init__(self, number) -> None:
        self._roman_number = number
        self._arabic_number = RomanNumeral._from_roman(self._roman_number)

    @staticmethod
    def _from_roman(roman_number):
        a, b = 0, RomanNumeral.__ROMAN[roman_number[0]]
        arabic_number = RomanNumeral.__ROMAN[roman_number[-1]]
        for i in range(1, len(roman_number)):
            a, b = b, RomanNumeral.__ROMAN[roman_number[i]]
            if a >= b:
                arabic_number += a
            else:
                arabic_number -= a
        return arabic_number

    @staticmethod
    def _to_roman(arabic_number):
        _arabic_number = arabic_number
        roman_number = ''
        for num in RomanNumeral.__ARABIC.items():
            while _arabic_number >= num[0]:
                _arabic_number -= num[0]
                roman_number += num[1]
        return roman_number

    def __str__(self) -> str:
        return f'{self._roman_number}'

    def __int__(self):
        return self._arabic_number

    def __eq__(self, other) -> bool:
        if isinstance(other, RomanNumeral):
            return self._arabic_number == other._arabic_number
        return NotImplemented

    def __lt__(self, other) -> bool:
        if isinstance(other, RomanNumeral):
            return self._arabic_number < other._arabic_number
        return NotImplemented

    def __add__(self, other):
        return RomanNumeral(RomanNumeral._to_roman(self._arabic_number + other._arabic_number))

    def __sub__(self, other):
        return RomanNumeral(RomanNumeral._to_roman(self._arabic_number - other._arabic_number))