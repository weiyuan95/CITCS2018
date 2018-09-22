def get_square(num):
    return num ** 2


def prime_sum(num):
    result = []

    while num > 0:
        for i in range(num, -1, -1):
            if is_prime(i) and is_prime(num - i) is not False:
                result.append(i)
                num -= i
                break
    return result


def is_prime(number):
    if number == 1:
        return False

    for i in range(2, number + 1):
        if i != number and number % i == 0:
            return False

    return True


print(prime_sum(2))
