from flask_login import login_required, session_protected
from itsdangerous import json
from numpy import cross
from . import data
from flask_cors import cross_origin
from flask import jsonify, request, url_for
from ..tasks import gettweets_pipeline, analyise_tweet_pipe



@data.route('/get_tweets', methods=["POST"])
@login_required
@cross_origin()
def get_tweets():
    """
    """
    if request.method == "POST":

        search_query = request.form.get("query")

        item_data_count = 10
        
        tweets = gettweets_pipeline(search_query, item_data_count)

        result = analyise_tweet_pipe(tweets)

        
        return result


@data.route('/save_to_database/<result>', methods=["PUT"])
@cross_origin()
def save_tweets(result):
    pass


@data.route('/previous-analysis/<platform>', methods=['POST','GET'])
@cross_origin()
def fetch_analysis(platform):

    """
    """
    pass



@data.route('/analyze-tweets', methods=['POST'])
def analyise_tweets():

    if request.method == "POST":

        search_query = request.form.get("query")

        item_data_count = 10

        task = gettweets_pipeline.apply_async((search_query, item_data_count),)

        return jsonify({}), 202, {'Location': url_for('data.taskstatus',
                                                  task_id=task.id)}


@data.route('/status/<task_id>')
def taskstatus(task_id):
    task = analyise_tweet_pipe.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return response
