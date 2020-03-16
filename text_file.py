def bad_joke():
    import random as r
    text = []
    single_joke = []
    with open("joke.txt", 'r') as file:
        for line in file:
            if '*' in line:
                text.append(single_joke)
                single_joke = []
            else:
                single_joke.append(line)
        random_joke = ''.join(text[r.randint(0, len(text) - 1)])
    return random_joke

