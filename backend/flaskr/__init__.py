import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ----------------------------------------------------------------------------#
# Formatting
# ----------------------------------------------------------------------------#

def format_items(items):
    """ Format the given items. """
    formatted_items = [item.format() for item in items]

    return formatted_items

# ----------------------------------------------------------------------------#
# Paginate Questions
# ----------------------------------------------------------------------------#

def paginate_questions(request, selected_items=None):
    """ Paginate questions by controlling db operations. """
    questions_limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
    selected_page = request.args.get('page', 1, type=int)
    start_index = (selected_page - 1) * questions_limit
    end_index = start_index + QUESTIONS_PER_PAGE

    if selected_items:
        current_questions = selected_items[start_index: end_index]
    else:
        current_questions = \
            Question.query.order_by(Question.id).limit(
                questions_limit
            ).offset(start_index).all()

    formatted_current_questions = format_items(current_questions)

    return formatted_current_questions

# ----------------------------------------------------------------------------#
# Create app
# ----------------------------------------------------------------------------#

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,DELETE,OPTIONS'
        )
        return response

    @app.route('/categories')
    def get_paginated_categories():
        """ Get all vailable categories, paginated. """
        categories_limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
        selected_page = request.args.get('page', 1, type=int)
        start_index = (selected_page - 1) * categories_limit
        
        current_categories = \
            Category.query.order_by(Category.id).limit(
                categories_limit
            ).offset(start_index).all()

        if len(current_categories) == 0:
            abort(404)

        formatted_categories = format_items(current_categories)
        categories_dict = {}
        for category in formatted_categories:
            key = category['id']
            value = category['type']
            categories_dict[key] = value

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    @app.route('/questions')
    def get_paginated_questions():
        """ Get all questions, paginated. """
        total_questions = len(Question.query.all())
        current_questions = paginate_questions(request)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categories_dict = {
            category.id: category.type for category in categories
        }

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': total_questions,
            'categories': categories_dict,
            'current_category': None
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """ Get questions based the chosen category. """
        candidate_questions = \
            Question.query.filter_by(
                category=str(category_id)
            ).order_by(Question.id).all()

        if len(candidate_questions) == 0:
            abort(404)
            
        current_questions = paginate_questions(request, candidate_questions)
        chosen_category = Category.query.get(category_id).type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(candidate_questions),
            'current_category': chosen_category
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """ Delete the specific question based on the given question id. """
        question = Question.query.filter_by(id=question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def get_next_quiz():
        """ Get the next question based on chosed category and
            answered questions.
        """
        body = request.get_json()

        if body is None:
            abort(400)

        try:
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if not previous_questions:
                candidate_questions = Question.query.filter_by(
                    category=quiz_category['id']
                ).all()
            else:
                candidate_questions = Question.query.filter_by(
                    category=quiz_category['id']
                ).filter(Question.id.notin_(previous_questions)).all()

            # answered all questions
            if len(candidate_questions) != 0:
                formatted_candidate_questions = [
                    candidate.format() for candidate in candidate_questions
                ]
                random_id = random.randint(0, len(candidate_questions) - 1)
                new_question = formatted_candidate_questions[random_id]
            else:
                new_question = None
            # print(new_question)

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        """ Create a new question. """
        body = request.get_json()

        if body is None:
            abort(400)
        
        if 'searchTerm' in body:
            return search_questions(body)
        else:
            # print("**** Start Create ****")
            try:
                question = body.get('question', None)
                answer = body.get('answer', None)
                difficulty = body.get('difficulty', None)
                category = body.get('category', None)
                new_question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category
                )
                new_question.insert()

                return jsonify({
                    'success': True
                })
            except:
                abort(422)

    @app.route('/questions', methods=['POST'])
    def search_questions(body):
        """ Search questions based on search string. """
        # print("**** Start Search ****")

        search_string = body['searchTerm']
        try:
            if not search_string:
                current_questions = paginate_questions(request)
            else:
                candidate_questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search_string))
                ).all()
                current_questions = paginate_questions(request, candidate_questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(candidate_questions),
                'currentCategory': None
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(422)
    def unpreocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Not Allowed Method"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    return app
