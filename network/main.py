import tensorflow as tf
import numpy as np
import keras
import pandas as pd
import random

'''
X - State, Automobiles,  


'''


### LOAD DATA ###
def load():
    data = pd.read_csv("out/training_data.csv")
    X_train = []
    for key, value in data.iterrows(): X_train.append(eval(value["X_train"]))

    Y_train_0, Y_train_1, Y_train_2, Y_train_3 = data["Y_train_0"], data["Y_train_1"], data["Y_train_2"], data[
        "Y_train_3"]
    return X_train, list(Y_train_0.astype(float)), list(Y_train_1.astype(int)), list(Y_train_2.astype(int)), list(
        Y_train_3.astype(int))


X_train, Y_train_0, Y_train_1, Y_train_2, Y_train_3 = load()


def create(Y_train, path, output_layer, epochs):
    if path == "out/Ozone.h5": Y_train = [int(val * 100) for val in Y_train]

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(1, 4)),
        keras.layers.Dense(200, activation='relu'),
        keras.layers.Dense(200, activation='relu'),
        keras.layers.Dense(200, activation='relu'),
        keras.layers.Dense(400, activation='relu'),
        keras.layers.Dense(400, activation='relu'),
        keras.layers.Dense(output_layer, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(X_train, Y_train, epochs=epochs)
    model.save(path)


def check_accuracy(model, Y_train):
    for x_train, y_train in zip(X_train, Y_train):
        prediction = model.predict([x_train])
        print(np.argmax(prediction), int(y_train))


def alter(data):
    data_ = {}
    for key, value in data.items():
        ret_data = []
        store = {}

        for index, point in enumerate(value):
            if index == 0:
                ret_data.append(point)
            else:
                delta = point - ret_data[-1]
                if delta > 10:
                    ret_data.append(point - 2)
                elif delta < -10:
                    ret_data.append(ret_data[-1] - 2)
                elif delta == 0:
                    print(store)
                    if ret_data[-1] not in store.keys():
                        store[ret_data[-1]] = 1
                    else:
                        store[ret_data[-1]] += 1

                    if store[ret_data[-1]] > 3:
                        ret_data.append(ret_data[-1] + 2)
                    else:
                        ret_data.append(ret_data[-1])
                else:
                    ret_data.append(point)
        data_[key] = ret_data
    return data_


class LinearRegression():
    def __init__(self, vals):
        self.values = [(x, y) for x, y in zip(range(0, len(vals) - 1), vals)]

    def compute(self):
        SumOfX, SumOfY = 0, 0
        for value in self.values:
            SumOfX += value[0]
            SumOfY += value[1]

        SumOfX = SumOfX / len(self.values)
        SumOfY = SumOfY / len(self.values)

        dividend = []
        divisor = []
        for value in self.values:
            dividend.append(value[0] - SumOfX)
            divisor.append(value[1] - SumOfY)

        summationOfDividend = 0
        summationOfDivisor = 0
        for dividend, divisor in zip(dividend, divisor):
            summationOfDividend += dividend * dividend
            summationOfDivisor += dividend * divisor

        return int(summationOfDivisor / summationOfDividend)


class Summarize:
    def __init__(self, predictions):
        self.predictions = predictions
        self.translator = {
            "SulfurDioxide": "sulfur dioxide",
            "Ozone": 'ozone',
            'CarbonMonoxide': 'carbon monoxide',
            'NitrogenDioxide': 'nitrogen dioxide'
        }
        self.effects = {
            "Ozone": [
                "more difficulty to breathe deeply and vigorously.",
                "shortness of breath, and pain when taking a deep breath.",
                "coughing and sore or scratchy throat."],
            "SulfurDioxide": [
                "throat, eye, and nose irritation",
                "asthma and lung infections",
                "acid rain which can harm the growth of various crops and disrupt marine ecosystems."
            ],
            "NitrogenDioxide": [
                "irritation airways in the human respiratory system",
                "respiratory diseases, particularly asthma, leading to respiratory symptoms (such as coughing, wheezing or difficulty breathing)",
                "foliage damage, decreasing growth or reducing crop yields"
            ],
            "CarbonMonoxide": [
                "reduced ability for your blood to carry oxygen",
                "carbon monoxide poisoning",
                "expidation of processes that influence global warming"
            ]
        }
        self.summary = """
            The Machine Learning algorithm depicts the trends of air pollutants for the next 10 years; from 2020-2030.
        """

    def comparison(self, value):
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def find_effects(self):
        trends = self.find_trend()
        score = 0
        for key, value in trends.items():
            score += self.comparison(value)
            sentence = self.make_effects_sentence(key, value)
            self.summary += ' ' + sentence
        score = round(score * 1/3)
        if score == 0:
            self.summary += " No major changes occured in the amount of pollutant. Try changing around the parameters a little more to see different outcomes."
        elif score > 0:
            self.summary += " In the next 10 years, abundances of air pollutants increase. This is dangerous to both environmental and human health."
        elif score < 0:
            self.summary += " Wow! The abundances of air pollutants decrease in the next 10 years. This contributes drastically towards saving both environmental and human health."

    def make_effects_sentence(self, pollutant, trend):
        sentence = None

        if trend == 0:
            sentence = f"The amount of {self.translator[pollutant]} doesn't change."
        elif 0 < trend:
            sentence = f"""The amount of {self.translator[pollutant]} is increasing at a rate of {trend} ppb/year. This could lead to """
            possible_indices = [0, 1, 2]
            indexone = random.choice(possible_indices)
            del possible_indices[indexone]
            indextwo = random.choice(possible_indices)
            sentence += f"""{self.effects[pollutant][indexone]} and {self.effects[pollutant][indextwo]}."""
        elif 0 > trend:
            sentence = f"""The amount of {self.translator[pollutant]} is decreasing at a rate of {trend} ppb/year. Keep it up :)"""

        return sentence

    def find_trend(self):
        trend = {}
        for key, value in self.predictions.items():
            trend_pred = LinearRegression(value)
            trend[key] = trend_pred.compute()
        return trend

    def get(self):
        return self.summary


# data = {'Ozone': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 'SulfurDioxide': [3, 3, 32, 32, 32, 32, 32, 32, 32, 32],
#         'NitrogenDioxide': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'CarbonMonoxide': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]}
# summary = Summarize(data)
# summary.find_effects()
# summary_ = summary.get()
# print(summary_)

# OzoneModel = create(Y_train_0, path="out/Ozone.h5", output_layer=20, epochs=400)
# OzoneModel = tf.keras.models.load_model("out/Ozone.h5")
# preds = []
# for x in range(0, 100, 10):
#     preds.append(np.argmax(OzoneModel.predict([[x, 5, 3, 3]])))
# preds = alter(preds)
#
#
# SulfurModel = create(Y_train_1, path="out/SulfurDioxide.h5", output_layer=400, epochs=1000)
# SulfurModel = tf.keras.models.load_model("out/SulfurDioxide.h5")
# # check_accuracy(SulfurModel, Y_train_1)
# preds = []
# for x in range(10, 100, 1):
#     preds.append(np.argmax(SulfurModel.predict([[x, 1, 7, 3]])))
# preds = alter(preds)
# print(preds)
#
#
# NitrogenModel = create(Y_train_2, path="out/NitrogenDioxide.h5", output_layer=80, epochs=400)
# Nitrogenmodel = tf.keras.models.load_model("out/NitrogenDioxide.h5")
# preds = []
# for x in range(80, 100, 1):
#     preds.append(np.argmax(Nitrogenmodel.predict([[x, 1, 7, 3]])))
#
#
# check_accuracy(Nitrogenmodel, Y_train_2)
#
# CarbonModel = create(Y_train_3, path="out/CarbonMonoxide.h5", output_layer=10, epochs=500)
#
