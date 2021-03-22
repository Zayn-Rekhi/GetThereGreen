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
