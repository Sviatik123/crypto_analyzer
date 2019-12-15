with open('pairs.txt', 'r') as file:
    pairs = file.read()
    pairs = pairs.replace('t', 'f')
    pairs = pairs.split('\n')
    pairs = list(filter(lambda x: len(x) == 7, pairs))
    pairs = list(set(list(map(lambda x: x[0:4], pairs))))

    with open('currencies.txt', 'w') as file2:
        for el in pairs:
            file2.write(el + '\n')

