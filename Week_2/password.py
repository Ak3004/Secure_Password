import secrets
import string


def getting_equal_length(num):
    # Divide the number by 4 using integer division
    quotient = num // 4
    remainder = num % 4
    # Create a list with the quotient repeated 4 times
    result = [quotient] * 4
    # Distribute the remainder among the first few elements
    for i in range(remainder):
        result[i] += 1
    return result

def generate_secure_password(length=12):
    distribution = getting_equal_length(length)

    password = []

    password += [secrets.choice(string.ascii_lowercase) for _ in range(distribution[0])]
    password += [secrets.choice(string.ascii_uppercase) for _ in range(distribution[1])]
    password += [secrets.choice(string.digits) for _ in range(distribution[2])]
    password += [secrets.choice(string.punctuation) for _ in range(distribution[3])]


    # Shuffling the password
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)