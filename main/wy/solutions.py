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
    expense_dict = {person: 0 for person in people}

    # total people represent the total number of friends
    total_people = len(people)

    # expense is a dict
    for expense in expenses:
        to_pay_person = expense["paidBy"]
        amount = expense["amount"]
        excluded_people = []

        if "exclude" in expense:
            excluded_people = expense["exclude"]

        if len(excluded_people) == total_people:
            continue

        amount_payable_to_each = round(amount, 2) / (total_people - len(excluded_people))
        amt_payable = round(amount_payable_to_each, 2)
        amt_owed = amount - amt_payable

        if to_pay_person in excluded_people:
            expense_dict[to_pay_person] += amount
        else:
            expense_dict[to_pay_person] += amt_payable

        for person in people:
            if person not in excluded_people and person != to_pay_person:
                expense_dict[person] += amt_owed

    result = []
    while len(expense_dict) > 0:

        max_person = max(expense_dict.items(), key=lambda x: x[1])
        min_person = min(expense_dict.items(), key=lambda x: x[1])
        min_person_amt = min_person[1]
        max_person_amt = max_person[1]

        if abs(min_person_amt) > max_person_amt:
            expense_dict[min_person[0]] += max_person_amt
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": max_person_amt})

            expense_dict.pop(max_person[0])

        elif abs(min_person_amt) < max_person_amt:
            expense_dict[max_person[0]] += min_person_amt
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": abs(min_person_amt)})
            expense_dict.pop(min_person[0])

        else:
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": max_person_amt})

            expense_dict.pop(min_person[0])
            expense_dict.pop(max_person[0])

    return {"transactions": result}


if __name__ == "__main__":
    data = {
        "name": "Jan Expense Report",
        "persons": ["Alice", "Bob", "Claire", "David"],
        "expenses": [
            {
                "category": "Breakfast",
                "amount": 100,
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
