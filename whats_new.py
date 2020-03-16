def news():
    import random as r
    webpage = 'https://stopgame.ru/newsdata/{}'.format(r.randint(42100, 42159))
    return webpage
