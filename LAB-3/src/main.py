from fastapi import FastAPI
from pydantic import BaseModel
from simpletransformers.classification import ClassificationModel

class Issue(BaseModel):
    title: str

app = FastAPI()

@app.post("/")
async def root(issue: Issue):
    try:
        issue_title = issue.title
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
