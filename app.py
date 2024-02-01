from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import urllib.parse
from bson import ObjectId, json_util
import os
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from werkzeug.exceptions import HTTPException
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Opportunity Recommendation API',
          description='Opportunity Recommendation API for the ByteMentors project')

ns = api.namespace('opportunities', description='Opportunity operations')

user_profile_model = api.model('UserProfile', {
    'bio': fields.String(required=True, description='User bio'),
    'preferredField': fields.String(required=True, description='User preferred field'),
    'skills': fields.List(fields.String, description='User skills')
})

opportunity_recommendation_model = api.model('OpportunityRecommendation', {
    'opportunity_info': fields.Raw(required=True, description='Opportunity Information'),
    'similarity_score': fields.Float(required=True, description='Similarity Score')
})

recommendations_model = api.model('Recommendations', {
    'user_info': fields.Nested(user_profile_model),
    'opportunity_recommendations': fields.List(fields.Nested(opportunity_recommendation_model))
})

class UserNotFoundException(Exception):
    pass

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error, please try again later."), 500

@app.errorhandler(PyMongoError)
def handle_mongo_error(e):
    app.logger.error(f"MongoDB Error: {str(e)}")
    return jsonify(error="A database error occurred."), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(UserNotFoundException)
def handle_user_not_found_exception(e):
    return jsonify({'error': str(e)}), 404

username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
cluster_url = os.getenv('MONGO_CLUSTER_URL')

username = urllib.parse.quote_plus(username)
password = urllib.parse.quote_plus(password)

client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster_url}/?retryWrites=true&w=majority')

USER_SIMILARITY_FIELDS = ['bio', 'preferredField', 'skills']
OPPORTUNITY_SIMILARITY_FIELDS = ['description', 'field']

def get_user_profile(user_id):
    db = client.ByteMentors.students
    user_profile = db.find_one({'_id': ObjectId(user_id)})
    if not user_profile:
        raise UserNotFoundException(f"User with id {user_id} not found")
    return user_profile

def get_all_opportunities():
    db = client.ByteMentors.opportunities
    currentDateTime = datetime.now()
    opportunities = list(db.find({'deadline': {'$gte': currentDateTime}}))
    return opportunities

def calculate_similarity(user_profile, opportunity, user_fields, opportunity_fields):
    def field_content_to_string(content):
        if isinstance(content, list):
            return ' '.join(content)
        return content

    user_text_pieces = [field_content_to_string(user_profile.get(field, '')) for field in user_fields]
    user_text = ' '.join(user_text_pieces)

    opportunity_text_pieces = [field_content_to_string(opportunity.get(field, '')) for field in opportunity_fields]
    opportunity_text = ' '.join(opportunity_text_pieces)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_text, opportunity_text])

    sim_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return sim_score

def format_recommendations(user_profile, recommendations):
    return {
        'user_info': user_profile,
        'opportunity_recommendations': [
            {'opportunity_info': opportunity, 'similarity_score': score}
            for opportunity, score in recommendations
        ]
    }

@ns.route('/recommend')
class OpportunityRecommendation(Resource):
    @api.doc(params={'user_id': 'User ID', 'num_recs': 'Number of Recommendations'})
    @api.marshal_with(recommendations_model)
    def get(self):
        num_recs = request.args.get('num_recs', default=3, type=int)
        user_id = request.args.get('user_id')

        user_profile = get_user_profile(user_id)
        if not user_profile:
            api.abort(404, "User not found")

        all_opportunities = get_all_opportunities()
        recommendations = []

        for opportunity in all_opportunities:
            similarity_score = calculate_similarity(user_profile, opportunity, USER_SIMILARITY_FIELDS, OPPORTUNITY_SIMILARITY_FIELDS)
            recommendations.append((opportunity, similarity_score))

        recommendations.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = recommendations[:num_recs]

        formatted_recommendations = format_recommendations(user_profile, top_recommendations)

        formatted_recommendations = json.loads(json_util.dumps(formatted_recommendations))

        return formatted_recommendations

@app.route('/test_mongo_connection', methods=['GET'])
def test_mongo_connection():
    try:
        db = client.ByteMentors.students
        user_profile = get_user_profile('658b06e8fd551216e9800908')

        if user_profile:
            return jsonify({'message': 'Connected to MongoDB', 'one_document': str(user_profile)}), 200
        else:
            return jsonify({'message': 'Connected to MongoDB, but no documents found in the collection'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to connect to MongoDB', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
