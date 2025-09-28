from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id}"


class Team(models.Model):
    name = models.CharField(max_length = 255)
    logo = models.ImageField(upload_to="teamlogos" , null = True , blank = True)
    created_by = models.ForeignKey(Profile,on_delete=models.CASCADE )
    created_at = models.DateTimeField(auto_now_add=True , null= True)

    def __str__(self):
        return self.name
    

class Player(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    role = models.CharField(max_length=50, null=True)
    batting_style = models.CharField(max_length=50, null=True)
    balling_style = models.CharField(max_length=50, null=True)
    team = models.ForeignKey(Team, on_delete = models.CASCADE, related_name="players")
    created_by = models.ForeignKey(Profile , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True , null = True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class BattingPerformance(models.Model):
    player = models.ForeignKey(Player , on_delete = models.CASCADE )
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    dot = models.IntegerField(default=0)
    singles = models.IntegerField(default=0)
    doubles = models.IntegerField(default=0)
    tripples = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    is_out = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    
    def strike_rate(self):
        return (self.runs / self.balls * 100) if self.balls > 0 else 0
    
    def boundary_percent(self):
        boundaries = self.fours + self.sixes
        return (boundaries / self.balls * 100) if self.balls > 0 else 0

    def __str__(self):
        return f"{self.player.firstname} {self.player.lastname}"

class BallingPerformance(models.Model):
    player = models.ForeignKey(Player , on_delete = models.CASCADE)
    wickets = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    hattricks = models.BooleanField(default=False)
    runs = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    maidens = models.IntegerField(default=0)
    no_balls = models.IntegerField(default=0)
    wides = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null = True)

    def overs_format(self):
        return f"{self.balls //6 }.{self.balls % 6}"
    
    def economy_rate(self):
        overs = self.balls / 6 if self.balls > 0 else 0
        return self.runs / overs if overs > 0 else 0
    
    def extras(self):
        return self.wides + self.no_balls
    
    def __str__(self):
        return f"{self.player.firstname} {self.player.lastname}"

class WicketKeeperPerformance(models.Model):
    player = models.ForeignKey(Player , on_delete=models.CASCADE)
    catches = models.IntegerField(default=0)
    stumppings = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.player.firstname} {self.player.lastname}"

class FieldingPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    catches = models.IntegerField(default=0)
    dropped = models.IntegerField(default=0)
    runouts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null = True)

    def catching_rate(self):
        if self.catches == 0 :
            return 100
        return (self.catches/(self.catches + self.dropped))*100

    def __str__(self):
        return f"{self.player.firstname} {self.player.lastname}"








