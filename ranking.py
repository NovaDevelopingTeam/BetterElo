class Ranking:
    def __init__(self, bronze: int, silver: int, gold: int, platinum: int, diamond: int, champion: int, finalchampion: int):
        self.bronze_start = 0
        self.bronze_end = bronze
        self.silver_start = bronze + 1
        self.silver_end = silver
        self.gold_start = silver + 1
        self.gold_end = gold
        self.platinum_start = gold + 1
        self.platinum_end = platinum
        self.diamond_start = platinum + 1
        self.diamond_end = diamond
        self.champion_start = diamond + 1
        self.champion_end = champion
        self.finalchampion_start = champion + 1
    
    def give_rank(self, elo: int):
        if elo <= self.bronze_end:
            return "bronze"
        elif elo <= self.silver_end:
            return "silver"
        elif elo <= self.gold_end:
            return "gold"
        elif elo <= self.platinum_end:
            return "platinum"
        elif elo <= self.diamond_end:
            return "diamond"
        elif elo <= self.champion_end:
            return "champion"
        elif elo >= self.finalchampion_start:
            return "final champion"