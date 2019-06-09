import get_data as gd
import pandas as pd
import requests
import mdax as md

print("getting MDAX symbols")
mda = md.mdax()
# print(mda.mdaxData)


mda.mdaxData.info()
