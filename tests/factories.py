from main.models import Question


def create_questions():
    questions = [
        Question(question='Favourite pet?'),
        Question(question='Secret crush?'),
        Question(question='Where did you go for honeymoon?'),
        Question(question='Which president do you hate most?'),
        Question(question='Mother maiden name?'),
    ]
    Question.objects.bulk_create(questions)
