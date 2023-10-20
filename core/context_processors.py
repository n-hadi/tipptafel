from .models import Tournament
def tournaments(request): #returns all tournaments for rendering in all templates
    return {
        'tournaments' : Tournament.objects.all().order_by("-relevance")
    }