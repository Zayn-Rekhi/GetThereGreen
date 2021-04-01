from termcolor import colored
import pandas as pd
import math

_PARAMETER_NAME = ["Ozone", "Sulfur dioxide", "Nitrogen dioxide (NO2)", "Carbon monoxide"]
_SAMPLE_DURATION = ["1 HOUR", "8-HR RUN AVG BEGIN HOUR", "8-HR RUN AVG END HOUR"]

_STATE_NAMES = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
                "Delaware", "District Of Columbia", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
                "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
                "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska",
                "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon",
                "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

_CENSUS_PATHS = ["datasets/commute/census_data_2010.csv", "datasets/commute/census_data_2011.csv",
                 "datasets/commute/census_data_2012.csv", "datasets/commute/census_data_2013.csv",
                 "datasets/commute/census_data_2014.csv", "datasets/commute/census_data_2015.csv",
                 "datasets/commute/census_data_2016.csv", "datasets/commute/census_data_2017.csv",
                 "datasets/commute/census_data_2018.csv", "datasets/commute/census_data_2019.csv"]

_AIR_PATHS = ["datasets/air_quality/annual_conc_by_monitor_2010.csv",
              "datasets/air_quality/annual_conc_by_monitor_2011.csv",
              "datasets/air_quality/annual_conc_by_monitor_2012.csv",
              "datasets/air_quality/annual_conc_by_monitor_2013.csv",
              "datasets/air_quality/annual_conc_by_monitor_2014.csv",
              "datasets/air_quality/annual_conc_by_monitor_2015.csv",
              "datasets/air_quality/annual_conc_by_monitor_2016.csv",
              "datasets/air_quality/annual_conc_by_monitor_2017.csv",
              "datasets/air_quality/annual_conc_by_monitor_2018.csv",
              "datasets/air_quality/annual_conc_by_monitor_2019.csv"]

def percentage(val, total):
    return int(val/total*100)


def clean_census_data(data, year):
    ret_data = []
    for index, value in data.iterrows():
        if index > 1:
            total = int(value["B08301_001E"]) + int(value["B08301_001M"])
            row = [
                value["NAME"],
                percentage(int(value["B08301_002E"]), total),
                percentage(int(value["B08301_010E"]), total),
                percentage(int(value["B08301_018E"]) + int(value["B08301_019E"]), total),
                year
            ]
            ret_data.append(row)
    return ret_data


def check_air_quality(row):
    if row[1] in _SAMPLE_DURATION and row[2] in _PARAMETER_NAME:
        return row
    else:
        # if row[1] in _SAMPLE_DURATION:
        #     print("{0}".format(colored(row[2], "green")))
        # if row[2] in _PARAMETER_NAME:
        #     print("{0}".format(colored(row[1], "blue")))
        return None


def get_average(val, rounding=True):
    if val != [0, 0]:
        if rounding: return int(val[0] / val[1])
        else: return round(val[0] / val[1], 3)
    else:
        return 0


def clean_air_quality(data):
    state_averages = {}

    for index, value in data.iterrows():
        if index > 1:
            row = [
                value["State Name"],
                value["Sample Duration"],
                value["Parameter Name"],
                value["Units of Measure"],
            ]
            try: row.append(float(value["99th Percentile"]))
            except ValueError: row.append(0)

            row = check_air_quality(row)

            if row:
                if row[0] not in state_averages.keys():
                    state_averages[row[0]] = [[0, 0], [0, 0], [0, 0], [0, 0]]
                else:
                    state = state_averages[row[0]][_PARAMETER_NAME.index(row[2])]
                    state[0] += row[4]
                    state[1] += 1

    return [[key, get_average(value[0], False), get_average(value[1]), get_average(value[2]), get_average(value[3])] \
            for key, value in state_averages.items()]


def merge(census_data, air_data):
    X_train, Y_train = [], []
    for point in air_data:
        census_point = list(filter(lambda x: x[0] == point[0], census_data))
        if census_point:
            census_point = census_point[0]
            del census_point[0]
            X_train.append(census_point)
            Y_train.append(point[1:])

    Y_train = list(zip(*Y_train))
    return X_train, list(Y_train[0]), list(Y_train[1]), list(Y_train[2]), list(Y_train[3])


def create_scale(train_data):
    max_val = math.ceil(max(train_data) / 20) * 20
    min_val = math.floor(min(train_data))
    step = int(max_val / 20)
    try:
        return list(range(min_val, max_val + step, step))
    except ValueError:
        return [0] * len(train_data)


def scale_data(train_data, scale):
    if not all(x==train_data[0] for x in train_data):
        data = []
        for point in train_data:
            index = 0
            for numb1, numb2, count in zip(scale[:-1], scale[1:], range(0, len(scale) - 1)):
                if numb1 <= point <= numb2:
                    index = count
                    break
            data.append(index)
        return data
    else:
        return [0]


def get_data(census_paths, air_paths):
    X_train, Y_train_0, Y_train_1, Y_train_2, Y_train_3 = [], [], [], [], []

    for census_path, air_path, year in zip(census_paths, air_paths, list(range(len(census_paths)))):
        census_data = pd.read_csv(census_path)
        air_data = pd.read_csv(air_path)

        census_data = clean_census_data(data=census_data, year=year)
        air_data = clean_air_quality(data=air_data)


        cur_X_train, cur_Y_train_0, cur_Y_train_1, cur_Y_train_2, cur_Y_train_3 = \
            merge(census_data=census_data, air_data=air_data)

        X_train.extend(cur_X_train)
        Y_train_0.extend(cur_Y_train_0)
        Y_train_1.extend(cur_Y_train_1)
        Y_train_2.extend(cur_Y_train_2)
        Y_train_3.extend(cur_Y_train_3)

        print("{0} and {1}.......{2}".format(colored(census_path, "cyan"), colored(air_path, "blue"), colored("DONE", "green")))

    return X_train, Y_train_0, Y_train_1, Y_train_2, Y_train_3


if __name__ == "__main__":
    X_train, Y_train_0, Y_train_1, Y_train_2, Y_train_3 = get_data(_CENSUS_PATHS, _AIR_PATHS)

    data = pd.DataFrame({"X_train":X_train,
                         "Y_train_0":Y_train_0,
                         "Y_train_1":Y_train_1,
                         "Y_train_2":Y_train_2,
                         "Y_train_3":Y_train_3})

    data.to_csv("out/training_data.csv")
