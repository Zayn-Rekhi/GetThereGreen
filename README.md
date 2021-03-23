![Get There Green Logo](ReadMedia/masterlogo.png?raw=true 'Get There Green')

# GetThereGreen - Our Solution to Air Pollution

GetThereGreen is an interactive simulation where users can see how their commute to work affects the quality of the air around them.

https://gettheregreen.ml

## Architecture

![Diagram of Get There Green architecture](ReadMedia/Architecture.png?raw=true 'Get There Green Architecture')

The API is hosted on a Raspberry Pi. This runs NGINX, Django, and TensorFlow in order to return predictions back to the frontend. The frontend is made in React/Typescript and hosted on Firebase

## Machine Learning

We used Tensorflow/Keras in order to create 4 highly accurate model (Multi-Layer Perceptron) that predicts the concentration of Sulfur Dioxide, Nitrogen Dioxide,
Carbon Monoxide, and Surface Level Ozone. The input data that wes used was acquired from the US Census data database under the specific header of **_B08301_**. The
air quality data was acquired from the EPA (United States Environmental Protection Agency) and is used as the labels for our training data.

## Navigate our repository

### Website Code

The React code is stored in the `app/` directory. You will find the components and such in `app/src`, while metadata and other information is stored in `public/src`

## How to Navigate The Repository

#API

The API folder is an API (Application Programming Interface) was created using the [DJANGO](https://www.djangoproject.com/) Web Framework. Machine Learning models are stored in the `api/models` folder where all the models have been zipped in order to save data for the repository. Most of the backend code that is used to process the incoming `POST` request is written in the `api/prediction/views.py` file. In order to run the following api, do the following:
``` 
1. Install Dependencies:
  pip3 install -r requirements.txt
2. Make Migrations: 
  python3 manage.py makemigrations
  python3 manage.py migrate
```
#NETWORK

In the Network folder, the models were trained and the data was cleaned. Firstly, the `census.py` file located in `network` is used in order to clean the data that is used to be fed into the Machine Learning algorithm. The `main.py` file is the testing file in whcih the models were created and functions that are used to format the predictions of the neural network were made. 

https://gettheregreen.ml/

