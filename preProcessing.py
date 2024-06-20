import pandas as pd
def preprocess(data, region):
    data = data[data["Season"]=="Summer"]

    data = data.merge(region, on="NOC", how="left", suffixes=('_data', '_region'))
    data.drop_duplicates(inplace=True)

    data = pd.concat([data, pd.get_dummies(data["Medal"])], axis=1)
    return data