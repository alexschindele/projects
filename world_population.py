import json

filename = "population.json"
with open(filename) as f:
    pop_data = json.load(f)

for pop_dict in pop_data:
    if pop_dict["Year"] == "2010":
        country_name = pop_dict["Country Name"]
        population = pop_dict["Value"]
        print("{country_name}: {population}".format(country_name, population))