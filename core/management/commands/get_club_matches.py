import requests
from django.core.management.base import BaseCommand
from core.models import Match, Team, Tournament
from datetime import datetime



def getTeam(team_name):
    return Team.objects.get(full_name=team_name)

class Command(BaseCommand):
    help = "Imports Club matches (if not already in db) for season. \n args: <tournament> <draw_impossible> <leagueShortcut> <leagueSeason>"

    def add_arguments(self, parser):
        parser.add_argument("tournament", type=str)
        parser.add_argument("draw_impossible", type=str)
        parser.add_argument("leagueShortcut", type=str)
        parser.add_argument("leagueSeason", type=str)
        return super().add_arguments(parser)
    
    def handle(self, *args, **kwargs):
        tournament = kwargs["tournament"]
        draw_impossible = kwargs["draw_impossible"]
        leagueShortcut = kwargs["leagueShortcut"]
        leagueSeason = kwargs["leagueSeason"]
        response = requests.get(f"https://api.openligadb.de/getmatchdata/{leagueShortcut}/{leagueSeason}")
        data = response.json()
        for match in data:
           try:
                if not match["matchIsFinished"] is True:
                  new_match = Match.objects.create(
                  start=datetime.strptime(match["matchDateTimeUTC"], "%Y-%m-%dT%H:%M:%SZ"),
                  season=leagueSeason,
                  t1=getTeam(match["team1"]["teamName"]),
                  t2=getTeam(match["team2"]["teamName"]),
                  draw_impossible = True if draw_impossible == "True" else False,
                  tournament=Tournament.objects.get(name=tournament),
                  open_db_info=match)
                  self.stdout.write(self.style.SUCCESS("Successfully added new match: " + str(new_match)))
           except Exception as e:
               print(f'Fehler: {match["team1"]["teamName"]} - {match["team2"]["teamName"]}')
               print(e)


