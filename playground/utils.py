def read_public_keys():
    with open('public_keys.txt', 'r') as file:
        public_keys = [line.strip() for line in file.readlines()]
    return public_keys
