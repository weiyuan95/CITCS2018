import math
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from pprint import pprint
from collections import defaultdict
import requests
import statsmodels.api as sm
import json

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


def sliding_puzzle(data):
    from collections import deque
    from itertools import chain, tee
    from math import sqrt
    from random import choice

    class Puzzle:
        HOLE = 0

        """
        A class representing an '8-puzzle'.
        - 'board' should be a square list of lists with integer entries 0...width^2 - 1
           e.g. [[1,2,3],[4,0,6],[7,5,8]]
        """

        def __init__(self, board, hole_location=None, width=None):
            # Use a flattened representation of the board (if it isn't already)
            self.board = list(chain.from_iterable(board)) if hasattr(board[0], '__iter__') else board
            self.hole = hole_location if hole_location is not None else self.board.index(Puzzle.HOLE)
            self.width = width or int(sqrt(len(self.board)))

        @property
        def solved(self):
            """
            The puzzle is solved if the flattened board's numbers are in
            increasing order from left to right and the '0' tile is in the
            last position on the board
            """
            return self.board == list(range(1, self.width * self.width)) + [Puzzle.HOLE]

        @property
        def possible_moves(self):
            """
            A generator for the possible moves for the hole, where the
            board is linearized in row-major order.  Possibilities are
            -1 (left), +1 (right), -width (up), or +width (down).
            """
            # Up, down
            for dest in (self.hole - self.width, self.hole + self.width):
                if 0 <= dest < len(self.board):
                    yield dest
            # Left, right
            for dest in (self.hole - 1, self.hole + 1):
                if dest // self.width == self.hole // self.width:
                    yield dest

        def move(self, destination):
            """
            Move the hole to the specified index.
            """
            board = self.board[:]
            board[self.hole], board[destination] = board[destination], board[self.hole]
            return Puzzle(board, destination, self.width)

        @staticmethod
        def direction(a, b):

            """
            The direction of the movement of the hole (L, R, U, or D) from a to b.
            """
            if a is None:
                return None

            return {
                -a.width: 'U',
                -1: 'L',
                0: None,
                +1: 'R',
                +a.width: 'D',
            }[b.hole - a.hole]

        def __str__(self):
            return "\n".join(str(self.board[start: start + self.width])
                             for start in range(0, len(self.board), self.width))

        def __eq__(self, other):
            return self.board == other.board

        def __hash__(self):
            h = 0
            for value, i in enumerate(self.board):
                h ^= value << i
            return h

    class MoveSequence:
        """
        Represents the successive states of a puzzle taken to reach an end state.
        """

        def __init__(self, last, prev_holes=None):
            self.last = last
            self.prev_holes = prev_holes or []

        def branch(self, destination):
            """
            Makes a MoveSequence with the same history followed by a move of
            the hole to the specified destination index.
            """
            return MoveSequence(self.last.move(destination),
                                self.prev_holes + [self.last.hole])

        def __iter__(self):
            """
            Generator of puzzle states, starting with the initial configuration
            """
            states = [self.last]
            for hole in reversed(self.prev_holes):
                states.append(states[-1].move(hole))
            yield from reversed(states)

    class Solver:
        """
        An '8-puzzle' solver
        - 'start' is a Puzzle instance
        """

        def __init__(self, start):
            self.start = start

        def solve(self):
            """
            Perform breadth-first search and return a MoveSequence of the solution,
            if it exists
            """
            queue = deque([MoveSequence(self.start)])
            seen = set([self.start])
            if self.start.solved:
                return queue.pop()

            for seq in iter(queue.pop, None):

                for destination in seq.last.possible_moves:
                    attempt = seq.branch(destination)
                    if attempt.last not in seen:
                        seen.add(attempt.last)
                        queue.appendleft(attempt)
                        if attempt.last.solved:
                            return attempt

    # https://docs.python.org/3/library/itertools.html#itertools-recipes
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def SortGame(board):
        result = []

        puzzle = Puzzle(board)

        move_seq = iter(Solver(puzzle).solve())

        for from_state, to_state in pairwise(move_seq):
            # print('------\n{} \nto\n \n{}\n-----'.format(from_state, to_state))
            # print()

            swappedWith = from_state.board[to_state.board.index(0)]

            result.append(swappedWith)

            Puzzle.direction(from_state, to_state)
            # print(to_state)

        return {'result': result}

    return SortGame(data)


def get_lat_and_longs(data):

    def _convert_to_degress(value):
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)


    def get_coords(image):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_coords above)"""

        exif_data = image._getexif()
        lat = None
        long = None

        if 34853 in exif_data:

            gps_dict = exif_data[34853]

            lat, gps_lat_ref = _convert_to_degress(gps_dict[2]), gps_dict[1]
            long, gps_long_ref = _convert_to_degress(gps_dict[4]), gps_dict[3]

            if gps_lat_ref != "N":
                lat = 0 - lat

            if gps_long_ref != "E":
                long = 0 - long

        return lat, long

    results = []

    for url_dic in data:
        url = url_dic["path"]
        r = requests.get(url, stream=True)
        r.raw.decode_content = True
        image = Image.open(r.raw)
        lat, long = get_coords(image)

        results.append({"lat": lat, "long": long})

    return results


def dino(data):
    print(data)
    return 1


def get_unknowns(data):
    print(data)
    inputs = data["input"]
    outputs = data["output"]

    model = sm.OLS(outputs, inputs)
    results = model.fit()
    results.summary()


if __name__ == "__main__":
    data = {
  "input": [
    [1, 2, 3],
    [2, 3, 4],
    [2, 1, 4],
    [5, 3, 2],
    [2, 1, 2],
    [1, 1, 1],
      [3, 3, 1],
      [5, 4, 1],
      [8, 2, 4]
  ],
  "output": [
    6,
    9,
    7,
    10,
    5,
      3,
      7,
      10,
      14
   ],
  "question": [3, 4, 5]
}
    # get_unknowns(data)

    data = {'boss': {'name': 'joker', 'offense': 11}, 'skills': [{'name': 'Grapple Gun', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Hacking Device', 'offense': 6, 'points': 2, 'require': 'Grapple Gun'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Hacking Device', 'offense': 6, 'points': 2, 'require': 'Grapple Gun'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}, {'name': 'Remote', 'offense': 7, 'points': 3, 'require': 'Hacking Device'}, {'name': 'Bomb', 'offense': 20, 'points': 5, 'require': 'Remote'}, {'name': 'Inverted takedown', 'offense': 5, 'points': 1, 'require': None}, {'name': 'Shockwave attack', 'offense': 8, 'points': 3, 'require': 'Inverted takedown'}]}
    json.loads(data)