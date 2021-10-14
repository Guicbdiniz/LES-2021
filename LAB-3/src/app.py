from flask import Flask, request, jsonify

from simpletransformers.classification import ClassificationModel

app = Flask('bugornay')


@app.post('/')
def bug_of_nay():
    try:
        issue_title = request.json['title']
        if issue_title is None:
            raise Exception('Invalid request body')

        model = ClassificationModel("roberta", "../outputs/checkpoint-1313-epoch-1", use_cuda=False)

        prediction, _ = model.predict([issue_title])
        print(prediction)

        return jsonify({'type': 'bug'})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'type': 'invalid'})
