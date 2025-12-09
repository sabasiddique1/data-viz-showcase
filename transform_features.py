# Transforming Data into Features
#
# This script converts categorical review data into numeric features:
# - Maps boolean and rating labels to numbers
# - One-hot encodes department_name
# - Converts review_date to datetime
# - Scales numeric features

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler


def main():
    csv_path = os.path.join('csv', 'reviews.csv')
    reviews = pd.read_csv(csv_path)

    print(reviews.columns)
    print(reviews.info())

    print(reviews["recommended"].value_counts())

    binary_dict = {True: 1, False: 0}
    reviews["recommended_binary"] = reviews["recommended"].map(binary_dict)
    print(reviews["recommended_binary"].value_counts())

    print(reviews["rating"].value_counts())

    rating_dict = {
        "Loved it": 5,
        "Liked it": 4,
        "Was okay": 3,
        "Not great": 2,
        "Hated it": 1,
    }
    reviews["rating_numeric"] = reviews["rating"].map(rating_dict)
    print(reviews["rating_numeric"].value_counts())

    print(reviews["department_name"].value_counts())

    one_hot = pd.get_dummies(reviews["department_name"])
    reviews = reviews.join(one_hot)
    print(reviews.columns)

    reviews["review_date"] = pd.to_datetime(reviews["review_date"])
    print(reviews["review_date"].dtype)

    numeric_reviews = reviews[["recommended_binary", "rating_numeric"] + list(one_hot.columns)]
    numeric_reviews.index = reviews["clothing_id"]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_reviews)
    print(scaled_data)


if __name__ == "__main__":
    main()

