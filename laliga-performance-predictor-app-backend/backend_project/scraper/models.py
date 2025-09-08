from django.db import models

class GoalkeeperMatch(models.Model):
    player = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    matchday = models.IntegerField()
    teams = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    minutes = models.IntegerField()
    saves = models.IntegerField()
    goals_conceded = models.IntegerField()
    errors_leading_to_goal = models.IntegerField()
    penalties_saved = models.IntegerField()

    def __str__(self):
        return f"{self.player} - {self.season} - Matchday {self.matchday}"


class DefenderMatch(models.Model):
    player = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    matchday = models.IntegerField()
    teams = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    minutes = models.IntegerField()
    recoveries = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    goals_conceded = models.IntegerField()

    def __str__(self):
        return f"{self.player} - {self.season} - Matchday {self.matchday}"


class MidfielderMatch(models.Model):
    player = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    matchday = models.IntegerField()
    teams = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    minutes = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    key_passes = models.IntegerField()
    recoveries = models.IntegerField()

    def __str__(self):
        return f"{self.player} - {self.season} - Matchday {self.matchday}"
    
class ForwardMatch(models.Model):
    player = models.CharField(max_length=100)
    season = models.CharField(max_length=20)
    matchday = models.IntegerField()
    teams = models.CharField(max_length=50)
    result = models.CharField(max_length=10)
    minutes = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    shots_on_goal = models.IntegerField()
    dribbles = models.IntegerField()

    def __str__(self):
        return f"{self.player} - {self.season} - Matchday {self.matchday}"