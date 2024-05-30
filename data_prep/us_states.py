from pandas import read_csv
from uom import convert

dtf = read_csv(
    "~/Downloads/us-states-territories.csv", keep_default_na=False, na_values=""
)

print(dtf)

dtf.Population2015 = dtf.Population2015.str.replace(",", "").astype("Int64")
dtf.Population2019 = dtf.Population2019.str.replace(",", "").astype("Int64")
dtf.AreaSquareMiles = dtf.AreaSquareMiles.str.replace(",", "").astype("float64")
dtf["Area"] = convert(dtf.AreaSquareMiles, "mi2", "m2")

dtf.drop(columns={"AreaSquareMiles"}, inplace=True)

print(dtf)

dtf.to_csv("data/quiz_us_state_capitals.csv", index=False)
