from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

class QuestionAnsweringModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('deepset/roberta-base-squad2')
        self.model = AutoModelForQuestionAnswering.from_pretrained('deepset/roberta-base-squad2')
        self.qa_pipeline = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer)

    def extract_answer(self, question, context):
        result = self.qa_pipeline(question=question, context=context, max_answer_len=50)
        answer = result.get('answer', '')
        score = result.get('score', 0.0)
        return answer, score
