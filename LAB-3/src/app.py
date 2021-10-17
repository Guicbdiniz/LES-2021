from flask import request, jsonify,Flask
from pydantic import BaseModel
from simpletransformers.classification import ClassificationModel

class Issue(BaseModel):
    title: str

app = Flask(__name__)

@app.route("/", methods = ['POST'])
async def root():
    try:
        issue_title = request.json['title']
        if issue_title is None:
            raise Exception('Invalid request body')

        model = ClassificationModel("roberta", "../outputs/checkpoint-1313-epoch-1", use_cuda=False)

        prediction, _ = model.predict([issue_title])
        if prediction[0] == 1:
            return {"prediction": "bug"}
        else:
            return {"prediction": "non-bug"}

    except Exception as e:
        print(f'Error: {e}')
        return {'type': 'invalid'}
