def fist_topic_id(quiz_data):
    """
    Return the first topic idx in the list.
    """
    topics = quiz_data['quiz']['topic']
    min_idx = topics[0]['id']
    return min_idx

def check_above_topics(quiz,telegram_id, topic_id, min_topic_id):
    """
    Check if the user has solved all the above topics.
    """

    if topic_id == min_topic_id:
        return True
    elif quiz.get_percentage(telegram_id, int(topic_id)-1)['solved'] >= 70:
        return True
    else:
        return False