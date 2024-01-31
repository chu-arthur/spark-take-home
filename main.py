from collections import defaultdict

zip_to_rate_area_map = {}
excluded_zips = set()

#Map zipcode to proepr rate areas
#Mark the zips with multiple rate areas that we don't calculate the SLCSP for
with open("slcsp/zips.csv") as f:
    next(f)
    for line in f:
        zip, state, _, _, rate_area = line.split(",")
        if zip in zip_to_rate_area_map and zip_to_rate_area_map[zip] != state+rate_area.strip():
            excluded_zips.add(zip)
        else:
            zip_to_rate_area_map[zip] = state + rate_area.strip()

rate_area_silver_plans = defaultdict(list)

#List all the silver plan rates for each rate area
with open("slcsp/plans.csv") as f:
    next(f)
    for line in f:
        _, state, metal_level, rate, rate_area = line.split(",")
        if metal_level == 'Silver':
            rate_area_silver_plans[state + rate_area.strip()].append(rate)

#Get the slcsp for each zipcode
#For zipcodes with multiple rate areas, or only 1 silver plan, leave the rate blank
with open("slcsp/slcsp.csv") as f:
    print(next(f)[:-1])
    for line in f:
        zipcode = line[:5]
        if zipcode in excluded_zips or len(rate_area_silver_plans[zip_to_rate_area_map[zipcode]]) <= 1:
            print(line[:-1])
        else:
            print(line[:-1] + sorted(rate_area_silver_plans[zip_to_rate_area_map[zipcode]])[1])