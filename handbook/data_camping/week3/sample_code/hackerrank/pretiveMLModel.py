import pandas as pd
from xml.etree import ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from typing import Dict, Tuple


def clean_data(dataset: str) -> Tuple[Dict[str, float], float]:

    # Step 1: Parsing the XML data, Extracting and Shaping data
    tree = ET.parse(dataset)
    root = tree.getroot()

    data = []
    for listing in root.findall('listing'):
        row = {}
        for attribute in listing:
            row[attribute.tag] = attribute.text
        data.append(row)
    df = pd.DataFrame(data)

    # Step 2,3,4: Cleansing data
    df.drop_duplicates(inplace=True)

    df.dropna(subset=['price', 'neighborhood'], inplace=True)

    df['price'] = pd.to_numeric(df['price'])

    # Step 5: Calculating the Average Price per Neighborhood Group
    avg_prices = df.groupby('neighbourhood_group')['price'].mean().to_dict()


    # Step 6: Developing the Predictive Model and Evaluation
    X = df[['latitude', 'longitude', 'minimum_nights', 'availability_365']]
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)

    return avg_prices, mae
# DryRun

avg_prices, mae = clean_data('airbnb_data.xml')