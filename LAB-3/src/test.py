from simpletransformers.classification import ClassificationModel


def main():
    title = input('What is the issue title?')
    model = ClassificationModel("roberta", "../outputs/checkpoint-1313-epoch-1", use_cuda=False)

    prediction, _ = model.predict([title])
    print(prediction)


if __name__ == '__main__':
    main()
