import json
from django.utils import timezone
from location.models import Country, Province, City

with open('scripts/dataset/ex_locations.json') as f:
    data = json.load(f)

for item in data:
    country_name = item['country']['name']
    country, created = Country.objects.get_or_create(name=country_name)

    for province_data in item['provinces']:
        province_name = province_data['name']
        province, created = Province.objects.get_or_create(name=province_name, country=country)

        for city_data in province_data['cities']:
            city_name = city_data['name']
            City.objects.get_or_create(name=city_name, province=province)
