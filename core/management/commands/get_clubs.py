# python db_teams_matches get_teams {Turnier} {leagueShortcut} {leagueSeason}
# Turnier bezeichnet den Turniernamen in Tipptafel DB
# die anderen parameter sind von Open_Liga_DB
# zuerst teams dann die matches
# python db_teams_matches get_matches {Turnier} {leagueShortcut} {leagueSeason}

import requests
from django.core.management.base import BaseCommand
from core.models import Team, Tournament
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from PIL import Image
import os
from config.settings import BASE_DIR


default_image_path = os.path.join(BASE_DIR, 'common_static/pics/teams/default.png')

def get_logo_from_link(url):
    try:
        response = requests.get(url, stream=True)
        tf = NamedTemporaryFile()
        # Read the streamed image in sections
        for block in response.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break
            # Write image block to temporary file
            tf.write(block)
        Image.open(File(tf)) # just for checking if the file isnt corrupted
        return File(tf)
    except Exception as e:
        print(e)

    default_image_data = open(default_image_path, 'rb').read()
    
    default_img_temp = NamedTemporaryFile(delete=True)
    default_img_temp.write(default_image_data)
    default_img_temp.flush()
    
    default_image_file = File(default_img_temp)
    return default_image_file


class Command(BaseCommand):

    help = "Imports clubs (if not already in db) for season. \n args: <tournament> <leagueShortcut> <leagueSeason>"

    def add_arguments(self, parser):
        parser.add_argument("tournament", type=str)
        parser.add_argument("leagueShortcut", type=str)
        parser.add_argument("leagueSeason", type=str)
        return super().add_arguments(parser)
    
    def handle(self, *args, **kwargs):
        tournament = kwargs["tournament"]
        leagueShortcut = kwargs["leagueShortcut"]
        leagueSeason = kwargs["leagueSeason"]
        response = requests.get(f"https://api.openligadb.de/getavailableteams/{leagueShortcut}/{leagueSeason}")
        data = response.json()
        for team in data:
            if not Team.objects.filter(full_name=team["teamName"]).exists():
                new_team = Team.objects.create(
                     full_name=team["teamName"],
                     short_name=team["shortName"],
                     logo=get_logo_from_link(team["teamIconUrl"]),
                     open_db_info=team
                )
                new_team.tournament.set([Tournament.objects.get(name=tournament)])
                self.stdout.write(self.style.SUCCESS("Successfully added new team: " + team["teamName"]))
            else:
                #if team is in Bundesliga but not in champions league yet, add it
                existing_team =  Team.objects.get(full_name=team["teamName"]) 
                if not existing_team.tournament.filter(name=tournament).exists():
                    existing_team.tournament.set([Tournament.objects.get(name=tournament)])
                    self.stdout.write(self.style.SUCCESS("Successfully added old team to new Tournament: " + team["teamName"] + " -> " + tournament))
        

    

