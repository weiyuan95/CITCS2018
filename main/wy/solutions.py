import math
from decimal import Decimal, ROUND_HALF_UP
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
        amount = Decimal(expense["amount"]).quantize(0, rounding=ROUND_HALF_UP)
        excluded_people = []

        if "exclude" in expense:
            excluded_people = expense["exclude"]

        if len(excluded_people) == total_people:
            continue

        amount_payable_to_each = Decimal(amount / (total_people - len(excluded_people))).quantize(0, rounding=ROUND_HALF_UP)

        amt_payable = amount_payable_to_each

        if to_pay_person in excluded_people:
            expense_dict[to_pay_person] += Decimal(amount).quantize(0, rounding=ROUND_HALF_UP)
        else:
            expense_dict[to_pay_person] += Decimal(amount - amt_payable).quantize(0, rounding=ROUND_HALF_UP)

        for person in people:
            if person not in excluded_people and person != to_pay_person:
                expense_dict[person] -= amt_payable

        print(expense_dict)
    # print(expense_dict)
    result = []
    while len(expense_dict) > 0:

        max_person = max(expense_dict.items(), key=lambda x: x[1])
        min_person = min(expense_dict.items(), key=lambda x: x[1])
        min_person_amt = min_person[1]
        max_person_amt = max_person[1]
        # print(result)
        # print(min_person)
        # print(max_person)
        # print()

        if abs(min_person_amt) > max_person_amt:
            expense_dict[min_person[0]] += max_person_amt
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": float(round(max_person_amt, 2))})

            expense_dict.pop(max_person[0])

        elif abs(min_person_amt) < max_person_amt:
            expense_dict[max_person[0]] += min_person_amt
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": float(round(abs(min_person_amt)))})
            expense_dict.pop(min_person[0])

        else:
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": float(round(max_person_amt, 2))})
            print(expense_dict)
            expense_dict.pop(max_person[0])
            expense_dict.pop(min_person[0])

    return {"transactions": result}


if __name__ == "__main__":
    data = {
    "name": "Jan Expense Report",
    "persons": ["Alice", "Bob", "Claire", "David"],
    "expenses": [
        {
            "category": "Breakfast",
            "amount": 60,
            "paidBy": "Bob",
            "exclude": ["Claire","David", "Bob"]
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
