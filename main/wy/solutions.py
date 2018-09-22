import math
from pprint import pprint


def get_square(num):
    return num ** 2


def prime_sum(num):
    temp = []
    used_biggest = []
    not_found = True

    while not_found:
        temp = []
        temp_num = num

        while temp_num > 0:

            for i in range(temp_num, -1, -1):
                if is_prime(i) and i not in used_biggest:
                    temp.append(i)
                    temp_num -= i
                    break

            if temp_num == 1:
                temp.append(1)
                temp_num = 0

        flag = [not is_prime(j) for j in temp]

        if not any(flag):
            not_found = False
        else:
            used_biggest.append(temp[0])

    return temp


def is_prime(number):
    if number == 2:
        return True
    if number % 2 == 0 or number <= 1:
        return False

    sqr = int(math.sqrt(number)) + 1

    for i in range(3, sqr, 2):
        if number % i == 0 and number != i:
            return False

    return True


def calculate_expenses(people, expenses):

    # we first create the expense dict to map each person to every other person
    expense_dict = {}
    for person in people:
        temp = {}

        for other_person in people:
            if other_person != person:
                temp[other_person] = 0

        expense_dict[person] = temp

    # total people represent the total number of friends
    total_people = len(people)

    # expense is a dict
    for expense in expenses:
        to_pay_person = expense["paidBy"]
        amount = expense["amount"]
        excluded_people = []

        if "exclude" in expense:
            excluded_people = expense["exclude"]

        amount_payable_to_each = amount / (total_people - len(excluded_people))
        amt_payable = round(amount_payable_to_each, 2)

        # expense_dict format
        # {person (from):
        #           {
    #                   person1 who person owes money to (to): $,
    #                   person2 who person owes money to(to): $},
    #                   },
    #     }

        for owing_person in people:
            if owing_person not in excluded_people and owing_person != to_pay_person:
                # check if the person that needs to be paid owes money to the person paying
                prev_owed = expense_dict[to_pay_person][owing_person]
                if amt_payable <= prev_owed:
                    expense_dict[to_pay_person][owing_person] = prev_owed - amt_payable
                else:
                    expense_dict[owing_person][to_pay_person] = amt_payable - prev_owed

    # transform data to proper format
    result = {"transactions": []}

    for from_person, to_person_dict in expense_dict.items():
        for to_person, payable in to_person_dict.items():

            payable_data = {"from": from_person, "to": to_person, "amount": payable}
            result["transactions"].append(payable_data)

    return result


if __name__ == "__main__":
    data = {
        "name": "Jan Expense Report",
        "persons": ["Alice", "Bob", "Claire", "David"],
        "expenses": [
            {
                "category": "Breakfast",
                "amount": 60,
                "paidBy": "Bob",
                "exclude": ["Claire","David"]
            },
            {
                "category": "Phone Bill",
                "amount": 100,
                "paidBy": "Claire"
            },
            {
                "category": "Groceries",
                "amount": 80,
                "paidBy": "David"
            },
            {
                "category": "Petrol",
                "amount": 40,
                "paidBy": "David"
            }
        ]
    }
    pprint(calculate_expenses(data["persons"], data["expenses"]))
