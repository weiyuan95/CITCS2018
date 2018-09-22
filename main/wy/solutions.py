import math
from decimal import Decimal, ROUND_HALF_UP
from pprint import pprint
from collections import defaultdict

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
    print(expenses)
    # we first create the expense dict to map each person to every other person
    expense_dict = {person: 0 for person in people}

    # total people represent the total number of friends
    total_people = len(people)

    # expense is a dict
    for expense in expenses:
        to_pay_person = expense["paidBy"]
        # amount = Decimal(expense["amount"]).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
        amount = expense["amount"]

        # print(amount)
        # amount = expense["amount"]

        excluded_people = []

        if "exclude" in expense:
            excluded_people = expense["exclude"]

        if len(excluded_people) == total_people:
            continue

        if len(excluded_people) == len(people) - 1 and to_pay_person not in excluded_people:
            continue

        # included_num = Decimal(total_people - len(excluded_people)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        # included_num = total_people / excluded_people
        # amount_payable_to_each = Decimal(amount / included_num).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
        amount_payable_to_each = amount / (total_people - len(excluded_people))

        # amt_payable = round(amount_payable_to_each, 2)
        amt_payable = amount_payable_to_each

        if to_pay_person in excluded_people:
            # expense_dict[to_pay_person] += Decimal(amount).quantize(0, rounding=ROUND_HALF_UP)
            expense_dict[to_pay_person] += amount
        else:
            # expense_dict[to_pay_person] += Decimal(amount - amt_payable).quantize(0, rounding=ROUND_HALF_UP)
            expense_dict[to_pay_person] += amount - amt_payable

        for person in people:
            if person not in excluded_people and person != to_pay_person:
                expense_dict[person] -= amt_payable

    # expense_dict = {k: Decimal(v).quantize(Decimal(".01"), rounding=ROUND_HALF_UP) for k, v in expense_dict.items()}
    print(sum(list(expense_dict.values())))
    print("BELOW HERE")
    print(expense_dict)
    # print(expense_dict)
    result = []
    while len(expense_dict) > 1:

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
                           # "amount": float(round(max_person_amt, 2))
                           "amount": float(Decimal(max_person_amt).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
                           })

            expense_dict.pop(max_person[0])

        elif abs(min_person_amt) < max_person_amt:
            expense_dict[max_person[0]] += min_person_amt
            result.append({"from": min_person[0],
                           "to": max_person[0],
                           "amount": float(
                               Decimal(abs(min_person_amt)).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
                           })
            expense_dict.pop(min_person[0])

        else:
            result.append({"from": min_person[0],
                           "to": max_person[0],

                           # "amount": float(round(max_person_amt, 2))
                           "amount": float(Decimal(max_person_amt).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
                           })
            print(expense_dict)

            expense_dict.pop(min_person[0])
            expense_dict.pop(max_person[0])

        if len(expense_dict) == 1:
            break
        print(expense_dict)
        return {"transactions": result}
        # "amount": float(round(abs(min_person_amt)))


def min_dist_sol(dist_list):
    d = sorted(dist_list)
    pair = min(zip(d, d[1:]), key=lambda x: x[1] - x[0])

    return {"answer": pair[1] - pair[0]}


def min_camps_sol(pos_dist_list):
    movements = {k: (d['pos'] - d['distance'] if d['pos'] - d['distance'] > 0 else 0,
                     d['pos'] + d['distance']) for k, d in enumerate(pos_dist_list)}

    roms = sorted(movements.items(), key=lambda x: x[0])

    intercepts = []
    common = None

    for pos, rom in roms:
        if common is None:
            common = rom[1]
        else:
            if rom[0] <= common <= rom[1]:
                continue
            else:
                intercepts.append(common)
                common = rom[1]

    intercepts.append(common)

    return {"answer": len(set(intercepts))}


def Broadcaster(data): #broadcaster
    master = []
    slave = []

    for item in data:
        master.append(item[0])
        slave.append(item[-1])

    master = set(master)
    slave = set(slave)

    realmaster = master.difference(slave)
    return  {
        "result" : list(realmaster)
    }


def most_nodes(data): #most connected node
    '''
    {
        "data" : ['U->V', 'J->L', 'C->G', 'T->Y', 'K->Q', 'E->M', 'F->O', 'N->Z', 'K->W', 'E->T', 'P->D', 'B->W', 'H->A', 'X->R', 'X->S', 'K->I']
    }
    '''

    d = defaultdict(set)

    for conn in data:
        master, slave = conn.split('->')

        d[master].add(slave)

        for node, connections in d.items():
            if master == node:
                continue
            if master in connections:
                d[node].add(slave)
            if slave in connections:
                d[node].add(master)

    # pprint(d)
    return {
        "result": sorted(d.items(), key=lambda x: len(x[1]))[-1][0]
    }


if __name__ == "__main__":
    pass
