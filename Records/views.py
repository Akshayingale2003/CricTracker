from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.hashers import make_password , check_password 
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def index(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password = password)
        if  user is not None:
            login(request , user)
            return redirect('/')
        else :
            messages.error(request,'invalid credentials')
    return render(request,'index.html')


def Logout(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method =='POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = make_password(password)

        )

        Profile.objects.create(user=user)
        messages.success(request,"user created successfully.")
    return render(request , 'register.html')

def profile(request):
    user = User.objects.get(id = request.user.id)
    
    if request.method == "POST":
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        messages.success(request, 'information changed successfully .. ')
        return redirect('profile')
    return render(request,'profile.html')

def change_password(request):
    user = User.objects.get(id = request.user.id)
    if request.method == "POST":
        old_password = request.POST['old_password']
        confirm_password = request.POST['confirm_password']
        new_password = request.POST['new_password']
        if user.check_password(old_password):
            if new_password == confirm_password :
                if old_password == new_password:
                    messages.error(request,'new password can not be same!')
                    return redirect('change_password')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'password changed successfully ..')
                    return redirect('change_password')
            else:
                messages.error(request, 'password does not match')
                return redirect('change_password')
        else:
            messages.error(request,'old password is wrong')    
            return redirect('change_password')

    return render(request, 'change_password.html')


def dashboard(request):
    players = Player.objects.all().count()
    teams = Team.objects.all().count()
    batting = BattingPerformance.objects.all()
    fielding = FieldingPerformance.objects.all()
    wicketkeeper = WicketKeeperPerformance.objects.all()
    balling = BallingPerformance.objects.all()
    users = Profile.objects.all().count()
    sixes = sum(p.sixes for p in batting)
    fours = sum(p.fours for p in batting)
    fcatches = sum(p.catches for p in fielding)
    wcatches = sum(p.catches for p in wicketkeeper)
    catches = fcatches + wcatches
    wickets = sum(p.wickets for p in balling)
    runs = sum(p.runs for p in batting)

    context = {
        'users' : users ,
        'players' : players,
        'teams' : teams,
        'sixes' : sixes,
        'fours' : fours ,
        'catches' : catches,
        'wickets': wickets,
         'runs' : runs
    }
    return render(request, 'dashboard.html', context)


def add_team(request):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(user = user)
    if request.method == "POST":
        team_name = request.POST.get('team_name')
        team_logo = request.FILES.get('teamlogo')  

        print("Team name:", team_name)
        print("Team logo:", team_logo)
        print("Type of team_logo:", type(team_logo))

        Team.objects.create(
            name=team_name,
            logo=team_logo,  
            created_by=profile
        )

        messages.success(request,'team created successfully')
        return redirect('add_team')
    return render(request, 'add_team.html')

def delete_team(request,id):
    team = Team.objects.get(id = id)
    team.delete()
    messages.success(request,'team deleted .. ')
    return redirect('my_teams')

def my_teams(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    teams = Team.objects.filter(created_by=profile)
    context = {
        'teams' : teams,
   
    }
    return render(request , 'my_teams.html' , context)


def edit_team(request,id):
    team = Team.objects.get(id = id)
    if request.method == 'POST':
        team.name =  request.POST['team_name']
        team.logo = request.FILES.get('teamlogo')
        team.save()
        messages.success(request, 'team edited ... ')
    context = {
        'team' : team
    }
    return render(request, 'editteam.html', context)


def add_player(request):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(user = user)
    teams = Team.objects.filter(created_by = profile)
    if request.method == "POST":
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        role = request.POST['role']  
        team = request.POST['team']
        batting_style = request.POST['bat_style']
        balling_style = request.POST['ball_style']
        Player.objects.create(firstname=firstname,lastname=lastname,
                              role=role, team_id = team,
                              batting_style=batting_style,balling_style=balling_style , 
                              created_by = profile)
        messages.success(request,'player added successfully ')
    context = {
        'teams' : teams,
    }
    return render(request, 'add_player.html' , context)


def my_players(request):
    user = User.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    players = Player.objects.filter(created_by = profile)
    context ={
        'players' : players
    }
    return render(request, 'my_players.html',context)


def edit_player(request,id):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(user = user)
    teams = Team.objects.filter(created_by = profile)
    player = Player.objects.get(id = id)
    
    if request.method == 'POST':
        player.firstname = request.POST['first_name']
        player.lastname = request.POST['last_name']
        player.role = request.POST['role']
        team_id = request.POST.get('team')
        if team_id :
            player.team = Team.objects.get(id = team_id)

        player.batting_style = request.POST['bat_style']
        player.balling_style = request.POST['ball_style']
        player.save()
        messages.success(request,'player edited successfully ')

    context = {
        'player' : player,
        'teams': teams
    }
    return render(request , 'editplayer.html' , context)

def delete_player(request ,id):
    player = Player.objects.get(id= id)
    player.delete()
    messages.success(request, 'player deleted')
    return redirect('my_players')


def my_dashboard(request):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(user = user)
    players = Player.objects.filter(created_by = profile)
    teams = Team.objects.filter(created_by = profile)
    battingperformance = BattingPerformance.objects.filter(player__in = players).order_by('created_at').reverse()
    ballingperformance = BallingPerformance.objects.filter(player__in = players).order_by('created_at').reverse()
    fieldingperformance = FieldingPerformance.objects.filter(player__in = players).order_by('created_at').reverse()
    WicketKeeperperformance = WicketKeeperPerformance.objects.filter(player__in = players).order_by('created_at').reverse()
    total_players = players.count()
    total_teams = teams.count()
    sixes = sum(p.sixes for p in battingperformance)
    fours = sum(p.fours for p in battingperformance)
    wickets = sum(p.wickets for p in ballingperformance)

    batting = battingperformance[:5]
    balling = ballingperformance[:5]
    fielding = fieldingperformance[:5]
    wicketkeeping = WicketKeeperperformance[:5]

    context = {
        'players':players,
        'teams':teams,
        'total_players':total_players,
        'total_teams':total_teams,
        'sixes' : sixes,
        'fours' : fours,
        'wickets' : wickets,
        'batting': batting,
        'balling':balling,
        'fielding':fielding,
        'wicketkeeping' : wicketkeeping,

    }
    return render(request , 'my_dashboard.html' , context)


# performance >>>>>

from django.urls import reverse

def add_performance(request):
     user = User.objects.get(id = request.user.id)
     profile = Profile.objects.get(user = user)
     players = Player.objects.filter(created_by = profile)
     if request.method == 'POST':
         player_id = request.POST.get('player_id')
         performance_type = request.POST.get('performance_type')

         if player_id and performance_type:
            if performance_type == "batting":
                return redirect(reverse("add_batting_performance", args=[player_id]))
            elif performance_type == "bowling":
                return redirect(reverse("add_balling_performance", args=[player_id]))
            elif performance_type == "fielding":
                return redirect(reverse("add_fielding_performance", args=[player_id]))
            elif performance_type == "wicketkeeper":
                return redirect(reverse("add_wicketkeeping_performance", args=[player_id]))

     return render(request , 'performance/add_performance.html' , {'players':players})



def add_batting_performance(request ,id):
    player = Player.objects.get(id = id)
    if request.method == "POST":
        is_out = request.POST.get('out_status')
        singles = request.POST.get('singles')
        doubles = request.POST.get('doubles')
        tripples = request.POST.get('tripples')
        dots = request.POST.get('dots')
        fours = request.POST.get('fours')
        sixes = request.POST.get('sixes')
        runs = int(sixes)*6 + int(fours)*4 + int(tripples)*3 + int(doubles)*2 + int(singles)
        balls = int(sixes) + int(fours) + int(tripples) + int(doubles) + int(singles) + int(dots)
        BattingPerformance.objects.create(player=player,runs=runs,balls = balls , is_out = is_out ,
                                           singles=singles,doubles=doubles,tripples=tripples,
                                           fours=fours,sixes=sixes ,dot = dots)
        messages.success(request,'performance added successfully.')
    return render(request , 'performance/add_batting_performance.html', {'player':player})

def add_balling_performance(request,id):
    player = Player.objects.get(id= id)
    if request.method == 'POST':
        balls = request.POST.get('balls')
        runs = request.POST.get('runs')
        wickets = request.POST.get('wickets')
        wides = request.POST.get('wides')
        no_balls = request.POST.get('no_balls')
        sixes = request.POST.get('sixes_conceded')
        fours = request.POST.get('fours_conceded')
        maidens = request.POST.get('maidens')
        BallingPerformance.objects.create(player=player,balls=balls,runs=runs,
                                          wickets=wickets,wides=wides,no_balls=no_balls,
                                          sixes=sixes,fours=fours,maidens=maidens)
        messages.success(request,'performance added succussfully.')
    return render(request , 'performance/add_balling_performance.html', {'player':player})

def add_fielding_performance(request,id):
    player = Player.objects.get(id = id)
    if request.method == 'POST':
        catches = request.POST.get('catches')
        dropped = request.POST.get('dropped')
        runouts = request.POST.get('runouts')
        FieldingPerformance.objects.create(player=player,catches=catches,
                                           dropped=dropped,runouts=runouts)
        messages.success(request,'performance added successfully.')
    return render(request , 'performance/add_fielding_performance.html', {'player':player})

def add_wicketkeeping_performance(request,id):
    player = Player.objects.get(id = id)
    if request.method == 'POST':
        catches = request.POST.get('catches')
        stumpings = request.POST.get('stumpings')
        WicketKeeperPerformance.objects.create(player=player,catches=catches,stumppings=stumpings)
        messages.success(request,'performance addedd successfully.')
    return render(request , 'performance/add_wicketkeeping_performance.html', {'player':player})



def view_performance(request):
    user = User.objects.get(id = request.user.id)
    profile = Profile.objects.get(user = user)
    players = Player.objects.filter(created_by = profile)
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        performance_type = request.POST.get('performance_type')
        if player_id and performance_type:
           if performance_type == "batting":
               return redirect(reverse("player_batting_performance", args=[player_id]))
           elif performance_type == "bowling":
               return redirect(reverse("player_balling_performance", args=[player_id]))
           elif performance_type == "fielding":
               return redirect(reverse("player_fielding_performance", args=[player_id]))
           elif performance_type == "wicketkeeper":
               return redirect(reverse("player_wicketkeeping_performance", args=[player_id]))
    
    return render(request,'performance/view_performance.html',{'players':players})



def player_batting_performance(request,id):
    player = Player.objects.get(id = id)
    performances = BattingPerformance.objects.filter(player=player)
    context = {
        'player' : player,
        'performances' : performances
    }
    return render(request,'performance/player_batting_performance.html' , context)


def player_balling_performance(request,id):
    player = Player.objects.get(id = id)
    performances = BallingPerformance.objects.filter(player=player)
    context = {
        'player':player,
        'performances':performances
    }
    return render(request,'performance/player_balling_performance.html' , context)


def player_wicketkeeping_performance(request,id):
    player = Player.objects.get(id = id)
    performances = WicketKeeperPerformance.objects.filter(player=player)
    context = {
        'player' : player,
        'performances' : performances
    }
    return render(request,'performance/player_wicketkeeping_performance.html' , context)


def player_fielding_performance(request,id):
    player = Player.objects.get(id = id)
    performances = FieldingPerformance.objects.filter(player=player)
    context = {
        'player' : player,
        'performances' : performances
    }
    return render(request,'performance/player_fielding_performance.html' , context)

def calculate_batting_stats(performances):
    total_runs = sum(p.runs for p in performances)
    total_balls = sum(p.balls for p in performances )
    total_singles = sum(p.singles for p in performances )
    total_doubles = sum(p.doubles for p in performances )
    total_tripples = sum(p.tripples for p in performances)
    total_fours = sum(p.fours for p in performances)
    total_sixes = sum(p.sixes for p in performances )
    played = len(performances)
    dismissals = sum(1 for p in performances if p.is_out)
    avg = total_runs / dismissals if dismissals > 0 else total_runs
    strike_rate = (total_runs * 100 / total_balls) if total_balls > 0 else 0
    high_score = max(p.runs for p in performances)
    boundary_percent = ((total_fours+total_sixes)/total_balls )*100

    return {
        "runs": total_runs,
        "balls": total_balls,
        'singles' : total_singles,
        'doubles' : total_doubles,
        'tripples' : total_tripples,
        "fours": total_fours,
        "sixes": total_sixes,
        "played": played,
        "average": round(avg, 2),
        "strike_rate": round(strike_rate, 2),
        'high_score':high_score,
        'boundary_percent':round(boundary_percent,2),
    }


def calculate_balling_stats(performances):
     played = len(performances)
     balls = sum(p.balls for p in performances)
     overs = balls//6 + (balls%6)/10 
     wickets = sum(p.wickets for p in performances)
     runs_conceded = sum(p.runs for p in performances)
     hattricks = sum(1 for p in performances if p.hattricks)
     fours = sum(p.fours for p in performances)
     sixes = sum(p.sixes for p in performances)
     maidens = sum(p.maidens for p in performances)
     wides = sum(p.wides for p in performances)
     no_balls = sum(p.no_balls for p in performances)
     extras = wides + no_balls

     threewickethall = sum(1 for p in performances if p.wickets>=3 and p.wickets<5)
     fivewickethall = sum(1 for p in performances if p.wickets>=5)

     

     return {
         'played' : played ,
         'balls' : balls ,
         'runs' : runs_conceded,
         'wickets' : wickets,
         'overs' : overs,
         'hattricks' : hattricks,
         'threewickethall' : threewickethall,
         'fivewickethall' : fivewickethall,
        #  'economy' : economy ,
         'fours' : fours,
         'sixes' : sixes,
         'maidens' : maidens,
         'wides' : wides ,
         'no_balls' : no_balls,
         'extras' : extras,
     }


def calculate_fielding_performance(performances):
    played = len(performances)
    catches = sum(p.catches for p in performances)
    dropped = sum(p.dropped for p in performances)
    runouts = sum(p.runouts for p in performances)

    return {
        'played' : played,
        'catches' : catches,
        'dropped' : dropped,
        'runouts' : runouts,
    }

def calculate_wicketkeeping_performance(performances):
    played = len(performances)
    catches = sum(p.catches for p in performances)
    stumpings = sum(p.stumppings for p in performances)
    return {
        'played' : played ,
        'catches' : catches,
        'stumpings' : stumpings
    }


def player_stats(request,id):
    player = Player.objects.get(id = id)
    batting_performance = BattingPerformance.objects.filter(player=player)
    balling_performance = BallingPerformance.objects.filter(player=player)
    fielding_performance = FieldingPerformance.objects.filter(player=player)
    wicketkeeping_performance = WicketKeeperPerformance.objects.filter(player=player)
    
    batting = ()
    balling = ()
    fielding = ()
    wicketkeeping = ()
    if batting_performance :
        batting = calculate_batting_stats(batting_performance)
    
    if balling_performance:
        balling = calculate_balling_stats(balling_performance)
    
    if fielding_performance:
        fielding = calculate_fielding_performance(fielding_performance)
    
    if wicketkeeping_performance:
        wicketkeeping = calculate_wicketkeeping_performance(wicketkeeping_performance)


    context = {
        'player':player,
        'batting_performance' :batting,
        'balling_performance' : balling,
        'fielding_performance' : fielding,
        'wicketkeeping_performance' : wicketkeeping,
    
    }
    return render(request,'stats/player_stats.html',context)

