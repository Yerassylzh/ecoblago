from catalog.models import *

def run():
    region = Region.objects.create(name="Улытауская область")
    City.objects.create(name="Вся область", region=region)
