import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# ----------------------------------------------------------------------------#
# Pagination
# ----------------------------------------------------------------------------#

def do_pagination(request, questions):
    """ Paginate questions. """
    page = request.args.get('page', 1, type=int)
    start_id = (page - 1) * QUESTIONS_PER_PAGE
    end_id = start_id + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in questions]
    current_questions = formatted_questions[start_id: end_id]

    return current_questions

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
        categories = Category.query.order_by(Category.id).all()
        current_categories = do_pagination(request, categories)

        if len(current_categories) == 0:
            abort(404)

        categories_dict = {}
        for category in current_categories:
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
        questions = Question.query.order_by(Question.id).all()
        current_questions = do_pagination(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categories_dict = {
            category.id: category.type for category in categories
        }

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': categories_dict,
            'current_category': None
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """ Get questions based the chosen category. """
        questions = Question.query.filter_by(
            category=str(category_id)
        ).order_by(Question.id).all()
        current_questions = do_pagination(request, questions)

        if len(current_questions) == 0:
            abort(404)

        chosen_category = Category.query.get(category_id).type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
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

            if len(candidate_questions) == 0:
                abort(404)

            formatted_candidate_questions = [
                candidate.format() for candidate in candidate_questions
            ]
            random_id = random.randint(0, len(candidate_questions) - 1)
            new_question = formatted_candidate_questions[random_id]
            # print(new_question)

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():
        """ Create a new question or search questions. """
        body = request.get_json()
        
        if body is None:
            abort(400)

        try:
            search_item = body.get('searchTerm', None)
            if search_item:
                candidate_questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search_item))
                ).all()
                current_questions = do_pagination(request, candidate_questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': len(candidate_questions),
                    'currentCategory': None
                })
            else:
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
