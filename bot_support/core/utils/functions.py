from fuzzywuzzy import fuzz

def recognize_questio(quwstion, questions):
    recognized = {'id': '', 'percent': 0}
    for key, value in questions.items():
        for q in value:
            percent = fuzz.ratio(quwstion, q)
            if percent > recognized['percent']:
                recognized['id'] = key
                recognized['percent'] = percent
    if recognized['percent'] < 60:
        result = 0
    else:
        result = recognized['id']
    return result

