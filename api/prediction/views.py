from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
from django.http import JsonResponse
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime as dt
import numpy as np
from statistics import mean
import json
import os
import time
import random

os.chdir("models")

_BASE_DATE = dt.datetime(2010, 1, 1)


def alter(data):
    data_ = {}
    for key, value in data.items():
        ret_data = []
        store = {}

        for index, point in enumerate(value):
            if index == 0:
                ret_data.append(point)
            else:
                delta = point-ret_data[-1]
                if delta > 10:
                    ret_data.append(point-2)
                elif delta < -10:
                    ret_data.append(ret_data[-1]-2)
                elif delta == 0:
                    print(store)
                    if ret_data[-1] not in store.keys():
                        store[ret_data[-1]] = 1
                    else:
                        store[ret_data[-1]] += 1

                    if store[ret_data[-1]] > 3: ret_data.append(ret_data[-1]+2)
                    else: ret_data.append(ret_data[-1])
                else:
                    ret_data.append(point)
        data_[key] = ret_data
    return data_

def log_request(req, data):
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/823032819600064523/qsNATX0D8FRtB4aX_GbNRfI41TFgBuMkXH9mDeI7kfXX6lvsuwgaxYUG_0QDkpCrhOHU")
    embed = DiscordEmbed(title=f"{dt.datetime.now():%Y-%m-%d}",
                         description=f'{req.method} {data}',
                         color=242424)

    webhook.add_embed(embed)
    webhook.execute()


class Prediction:
    def __init__(self):
        print(os.getcwd())
        print(os.listdir("."))
        self.models = {
            "Ozone": load_model("Ozone.h5"),
            "SulfurDioxide": load_model("SulfurDioxide.h5"),
            "NitrogenDioxide": load_model("NitrogenDioxide.h5"),
            "CarbonMonoxide": load_model("CarbonMonoxide.h5")
        }

    def average(self, predictions):
        ret = {}
        for key_, value_ in predictions.items():
            for _, value in value_.items():
                avg = int(mean(value))
                if key_ not in ret.keys():
                    ret[key_] = [avg]
                else:
                    ret[key_].append(avg)
        return ret

    def make(self, x_pred):
        predictions = {"Ozone": {}, "SulfurDioxide": {}, "NitrogenDioxide": {}, "CarbonMonoxide": {}}
        for point in x_pred:
            for key, value in self.models.items():
                pred = int(np.argmax(value.predict([point])))
                year = point[3]
                if year not in predictions[key].keys():
                    predictions[key][year] = [pred]
                else:
                    predictions[key][year].append(pred)
        return self.average(predictions)

class Clean:
    def __init__(self, data):
        self.data = data
        self.years = self.data["years"]
        self.ret = []

    def format(self):
        year_range = self.format_years()
        for year in year_range:
            self.ret.append([
                self.data["no-fuel"],
                self.data["public"],
                self.data["cars"],
                year
            ])

    def format_years(self):
        if isinstance(self.years, list):
            return range(self.years["end_date"] - _BASE_DATE, self.years["start_date"] - _BASE_DATE)
        else:
            return range(1, 11)

    def get(self):
        return self.ret

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
            The machine learning algorithm depicts the trends of air pollutants for the next 10 years; from 2020-2030.
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
            self.summary += "The amount of pollutant did not change all that much. Try changing around the parameters a little more to see different outcomes."
        elif score > 0:
            self.summary += "In the next 10 years, abundances of air pollutants increase. This is dangerous to both environmental and human health."
        elif score < 0:
            self.summary += "Wow! The abundances of air pollutants decrease in the next 10 years. This contributes drastically towards saving both environmental and human health."

    def make_effects_sentence(self, pollutant, trend):
        sentence = None

        if trend == 0:
            sentence = f"The amount of {self.translator[pollutant]} doesn't change."
        elif 0 < trend:
            sentence = f"""The amount of {self.translator[pollutant]} has increased by {trend} ppb. This could lead to """
            possible_indices = [0, 1, 2]
            indexone = random.choice(possible_indices)
            del possible_indices[indexone]
            indextwo = random.choice(possible_indices)
            sentence += f"""{self.effects[pollutant][indexone]} and {self.effects[pollutant][indextwo]}."""
        elif 0 > trend:
            sentence = f"""The amount of {self.translator[pollutant]} has decreased by {trend} ppb/year. Keep it up"""

        return sentence

    def find_trend(self):
        trend = {}
        for key, value in self.predictions.items():
            delta = value[-1]-value[0]
            trend[key] = delta 
        return trend

    def get(self):
        return self.summary


@csrf_exempt
def predict(request):
    p_data = json.loads(str(request.body, encoding='utf-8')) 
    
    #try:
    start = time.time()
    if p_data != "":
        clean = Clean(p_data)
        clean.format()
        values = clean.get()
        print(values)

        pred = Prediction()
        predictions = alter(pred.make(values))
        print(predictions)
        
        formatted_data = []
        for val in list(predictions.values()):
            formatted_data.extend(val)
            _max = max(formatted_data)

        summary = Summarize(predictions)
        summary.find_effects()
        summary_ = summary.get()
            
        ret_data = {
            "max": _max,
            "predictions": predictions,
            "summary": summary_
        }

    #except Exception as e:
    #    ret_data = {"error":f"{e}"}
    log_request(request, p_data)
    return JsonResponse(ret_data)
