# Training Opportunities Recommendation API


## Overview

The Training Opportunities Recommendation API is a Flask-based web service designed to match users with training opportunities based on their profiles and the descriptions of the training programs. It employs Machine Learning techniques, such as cosine similarity, to measure the match between users' skills and the requirements of training opportunities.

## Features

- Retrieval of user profiles from MongoDB.
- Retrieval of training opportunity listings from MongoDB.
- Cosine similarity scoring to match user skills with training requirements.
- RESTful endpoints with JSON responses for ease of integration.

## Technologies Used

- Flask for the web server framework.
- Flask-RESTx for the RESTful API structure and Swagger documentation.
- pymongo for interacting with MongoDB Atlas.
- scikit-learn for TF-IDF vectorization and cosine similarity.
- dotenv for environment variable management.

## Prerequisites

Ensure you have the following installed:

- Python 3.6 or later
- pip (Python package installer)
- MongoDB Atlas account and cluster

## Setup and Installation

### Clone the Repository

To get started, clone this repository to your local machine:

`git clone <repository-url>`

### Install Dependencies

Install the required Python packages by navigating to the project directory and running:
`pip install -r requirements.txt`

### Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
MONGO_USERNAME=<Your MongoDB Atlas username>
MONGO_PASSWORD=<Your MongoDB Atlas password>
MONGO_CLUSTER_URL=<Your MongoDB Atlas cluster URL>

```

### Run the Application

To start the Flask application, use the following command:
`flask run`

This will start the development server on `http://localhost:5000/`.

## Usage

Once the server is running, you can access the Swagger UI to interact with the API by navigating to:
`http://localhost:5000/`

### Endpoints

- `/opportunities/recommend`: GET request to fetch training opportunity recommendations based on a user ID and desired number of recommendations.
- `/test_mongo_connection`: GET request to test the connection to the MongoDB database.

## Error Handling

The API includes detailed error handling, which provides descriptive error messages and HTTP status codes for the following cases:

- Resource not found (404)
- Internal server error (500)
- MongoDB errors
- User not found
  exceptions
