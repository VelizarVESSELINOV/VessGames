from pandas import read_csv

dtf = read_csv("~/Downloads/countries.csv", keep_default_na=False, na_values="")

dtf.drop(columns={"id"}, inplace=True)
dtf.to_csv("data/quiz_country_capitals.csv", index=False)
