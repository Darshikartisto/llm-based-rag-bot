from flask import Flask, request, jsonify
from utils import search_articles, concatenate_content, generate_answer
import os
from flask_cors import CORS # type: ignore
app = Flask(__name__)
CORS(app)

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    
    try:
        
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'Query parameter is required'}), 400

        print(f"Received query: {user_query}")

        
        print("Step 1: Searching articles...")
        articles = search_articles(user_query)
        
        if not articles:
            return jsonify({'error': 'No relevant articles found.'}), 404

        
        print("Step 2: Concatenating content...")
        content = concatenate_content(articles)
        
        if not content.strip():
            return jsonify({'error': 'Failed to extract meaningful content from articles.'}), 500

        
        print("Step 3: Generating answer...")
        answer = generate_answer(content, user_query)
        
        if not answer.strip():
            return jsonify({'error': 'Failed to generate a response.'}), 500

        # Return the generated answer
        return jsonify({'answer': answer}), 200

    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': 'An unexpected error occurred.', 'details': str(e)}), 500

if __name__ == '__main__':
    
    app.run(host='localhost', port=5001)
