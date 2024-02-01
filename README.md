# Job Recommendation API

## Overview

The Job Recommendation API is a Flask-based web service designed to provide job matching services based on user profiles and job descriptions. It utilizes Machine Learning techniques, such as cosine similarity, to measure the relevance between users' skills and job requirements.

## Features

- User profile retrieval from MongoDB.
- Job listings retrieval from MongoDB.
- Cosine similarity scoring between user skills and job requirements.
- RESTful endpoints with JSON responses.

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

- `/jobs/recommend`: GET request to retrieve job recommendations based on user ID and the number of recommendations.
- `/test_mongo_connection`: GET request to test the connection to the MongoDB database.

## Error Handling

The API includes detailed error handling, which provides descriptive error messages and HTTP status codes for the following cases:

- Resource not found (404)
- Internal server error (500)
- MongoDB errors
- User not found
  exceptions
