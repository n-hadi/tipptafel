from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
import datetime, random, string, pytz
from django.dispatch import receiver
from django.templatetags.static import static
from django.db.models.signals import post_save
from PIL import Image
from django.core.exceptions import ValidationError


# Create your models here.

def tournamentimg_url(instance, filename):
 return 'tournament/'+ filename



def return_image_format(image):
    try:
        img = Image.open(image)
        img_format = img.format
    except Exception as e:
        print("Error saving image for: " + image.name)
        print(e)
        img_format = 'PNG'

    format_to_extension = {
        'JPEG': 'jpg',
        'PNG': 'png',
        'GIF': 'gif',
        'SVG': 'svg',
        'WebP': 'webp',
    }
    return format_to_extension[img_format]
 
def teamlogo_url(instance,filename):
 if instance.national == True:
  return f'flags/{instance.full_name}.{return_image_format(instance.logo)}'
 else:
   return f'clubs/{instance.full_name}.{return_image_format(instance.logo)}'


class Tournament(models.Model):
 name = models.CharField(max_length=100)
 img = models.ImageField(upload_to=tournamentimg_url)
 relevance_scale = [
    (1, 'Not relevant'),
    (2, 'Slightly relevant'),
    (3, 'Moderately relevant'),
    (4, 'Quite relevant'),
    (5, 'Highly relevant')
 ]
 relevance = models.IntegerField(choices=relevance_scale, default="1")
 type_choices = [('nat','National'),('intc','International Clubs'),('int','International')]
 type = models.CharField(choices=type_choices,max_length=100)
 def __str__(self):
  return self.name
 

class Team(models.Model):
 full_name = models.CharField(max_length=100)
 short_name = models.CharField(max_length=100)
 abbr_name = models.CharField(max_length=5, default="")
 national = models.BooleanField(default=False)
 logo = models.ImageField(upload_to=teamlogo_url, default='pics/teams/default.png')
 logo_sm = ImageSpecField(source='logo', processors=[ResizeToFit(25,25)],format='PNG',options={'quality': 100})
 tournament = models.ManyToManyField('core.Tournament', blank=True)
 open_db_info = models.JSONField(default=dict)
 def __str__(self):
  return self.full_name

class Match(models.Model):
 identifier = models.CharField(default='', max_length=11, editable=False)
 start = models.DateTimeField()
 national = models.BooleanField(default=False)
 friendly = models.BooleanField(default=False)
 tournament = models.ForeignKey('core.Tournament',blank=True, on_delete=models.PROTECT)
 season = models.CharField(default="",max_length=999)
 t1 = models.ForeignKey('core.Team', related_name="t1",on_delete=models.PROTECT)
 t2 = models.ForeignKey('core.Team', related_name="t2",on_delete=models.PROTECT)
 t1_goals = models.IntegerField(blank=True, null=True)
 t2_goals = models.IntegerField(blank=True, null=True)
 t1_goals_penalties = models.IntegerField(blank=True, null=True)
 t2_goals_penalties = models.IntegerField(blank=True, null=True)
 penalties = models.BooleanField(default=False)
 draw_impossible = models.BooleanField(default=False)
 outcome_choices = [
  ('t1','Team 1'),
  ('t2','Team 2'),
  ('x','Unentschieden'),
  ('an','Anstehend'),
  ('u','Ungueltig')
  ]
 outcome = models.CharField(choices=outcome_choices, max_length=100, default="an", blank=True)
 open_db_info = models.JSONField(default=dict)

 def __str__(self):
  return str(self.t1) + ' - ' + str(self.t2)
 
 def status(self):
   if self.outcome == "an" or self.outcome == "u":
    return self.outcome
   else:
    goals1 = str(self.t1_goals + self.t1_goals_penalties) if self.t1_goals_penalties else str(self.t1_goals)
    goals2 = str(self.t2_goals + self.t2_goals_penalties) if self.t2_goals_penalties else str(self.t2_goals)
    outcome_str = str(self.t1) + " [ " + goals1 +" : "+ goals2 + " ] " + str(self.t2)     
    return outcome_str
 
 def convert_timezone_and_format(self, target_timezone, format):
        formatted_date = self.start.astimezone(pytz.timezone(target_timezone)).strftime(format)
        return formatted_date

@receiver(post_save, sender=Match)
def create_match_identifier(sender, instance, created, **kwargs):
 if instance.identifier == '':
    while True:
      characters = string.ascii_letters + string.digits
      identifier = ''.join(random.choice(characters) for _ in range(11))
      if not Match.objects.filter(identifier=identifier).exists():
       instance.identifier = identifier
       instance.save()
       break

  
  
class HomePageBackground(models.Model):
  img = models.ImageField(upload_to='homepage/')

 