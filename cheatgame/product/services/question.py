from cheatgame.product.models import Question, Product
from cheatgame.users.models import BaseUser


def create_question(*, product: Product, question: str, sender: BaseUser) -> Question:
    return Question.objects.create(
        product=product,
        question=question,
        sender=sender
    )


def update_question(*, question_id: int, sender: BaseUser, question: str) -> Question:
    question_object = Question.objects.get(id=question_id)
    question_object.question = question
    question_object.sender = sender
    question_object.save()
    return question_object


def delete_question(*, question_id: int) -> None:
    Question.objects.get(id=question_id).delete()
