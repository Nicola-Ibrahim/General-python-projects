"""
Main goal:
    - Decorate the name_format() method that take person's data and format it in a certain shape
    - The people should be sorted in ascending order depending on their ages.
        -> Additional code for edit name's format
            -> Hence, decorating the name_format() method to add ability to sort people list before 
                the name_format() method execution.
"""


def person_lister(func):
    def inner(people):

        # Sorting the people list depending on their age which (age=iter[2])
        sorted_people = sorted(people, key=lambda iter: int(iter[2]))

        # Formatting each person's data in a specific shape
        formatted_people = list(map(func, sorted_people))

        # Returned formatted people's list
        return formatted_people
        
    return inner

@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')
