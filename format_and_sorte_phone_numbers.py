
import re
from dataclasses import dataclass

@dataclass
class regex_in:
    """Class that takes string and matching it with a pattern"""
    string: str

    def __eq__(self, pattern: str | re.Pattern):
        """Match string with the given pattern

        Args:
            pattern (str | re.Pattern): the desire pattern to be match with

        Returns:
            matching (bool): the value of there is a match or not
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
            
        assert isinstance(pattern, re.Pattern)
    
        return pattern.fullmatch(self.string) is not None


def wrapper(f):
    def fun(l):
        # Handle numbers and change its format
        # 07895462130 -> 0 78954 62130 -> +91 78954 62130
        new_numbers = []
        checking_pattern = "[+]?(\d{0,2})\s(\d){5}\s(\d){5}"
          
        for number in l:

            # Convert to string for regex and further concatenation
            number_str = str(number)
            
            match regex_in(number_str):
                case r"^(?P<section1>\d{5})(?P<section2>\d{5})$": # count: 10 numbers

                    matching = re.match(r"^(?P<section1>\d{5})(?P<section2>\d{5})$", number_str)
                    
                    number_str = " ".join(['+91', matching.group("section1"), matching.group("section2")])
                


                case r"^(?P<prefix>0)(?P<section1>\d{5})(?P<section2>\d{5})$": # count: 11 numbers
                    matching = re.match(r"^(?P<prefix>0)(?P<section1>\d{5})(?P<section2>\d{5})$", number_str)
                    
                    number_str = " ".join(['+91', matching.group("section1"), matching.group("section2")])

                case r"^(?P<prefix>91)(?P<section1>\d{5})(?P<section2>\d{5})$": # count: 12 numbers
                    matching = re.match(r"^(?P<prefix>91)(?P<section1>\d{5})(?P<section2>\d{5})$", number_str)
                    
                    number_str = " ".join(['+91', matching.group("section1"), matching.group("section2")])

            new_numbers.append(number_str) 
                    
        # Return sorting numbers
        sorting_numbers = f(new_numbers)
        return sorting_numbers
    return fun

@wrapper
def sort_phone(l):
    print(*sorted(l), sep='\n')

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    # l = [9195969878]
    sort_phone(l) 
