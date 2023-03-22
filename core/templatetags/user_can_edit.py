from django import template


register = template.Library()


@register.simple_tag
def user_can_edit_question(user, question):
    return user.can_edit_question(question)


@register.simple_tag
def user_can_edit_quiz(user, quiz):
    return user.can_edit_quiz(quiz)


@register.simple_tag
def user_can_edit_comment(user, comment):
    return user.can_edit_comment(comment)
