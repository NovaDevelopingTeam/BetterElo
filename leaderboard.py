class Leaderboard:
    def __init__(self, size: int):
        self.size = size
        self.users = []
    
    def add_user(self, user: int, elo: int):
        if elo > self.users[-1][1]:
            if len(self.users) == self.size:
                del self.users[-1]
                self.users.append((user, elo))
                self.users.sort(reverse=True, key=lambda tup: tup[1])
            else:
                self.users.append((user, elo))
                self.users.sort(reverse=True, key=lambda tup: tup[1])
    
    def re_sort(self):
        self.users.sort(reverse=True, key=lambda tup: tup[1])
    
    def string(self):
        res = f""
        c = 1
        for tup in self.users:
            user = tup[0]
            elo = tup[1]
            res = res + f"{c}: [{user}](tg://user?id={user}): {elo}\n"
            c += 1
        return res
