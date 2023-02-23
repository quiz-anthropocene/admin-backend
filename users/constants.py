from django.utils.translation import gettext_lazy as _


USER_ROLE_CONTRIBUTOR = "CONTRIBUTOR"
USER_ROLE_SUPER_CONTRIBUTOR = "SUPER-CONTRIBUTOR"
USER_ROLE_ADMINISTRATOR = "ADMINISTRATOR"
USER_ROLE_CHOICES = (
    (USER_ROLE_CONTRIBUTOR, _("Contributor")),
    (USER_ROLE_SUPER_CONTRIBUTOR, _("Super Contributor")),
    (USER_ROLE_ADMINISTRATOR, _("Administrator")),
)

IS_ADMIN_MESSAGE = _("You are an administrator")
ADMIN_REQUIRED_MESSAGE = _("You don't have the necessary rights")
ADMIN_REQUIRED_EDIT_FIELD_MESSAGE = _("You don't have the necessary rights to edit this field")
ONLY_ADMIN_ALLOWED_MESSAGE = _("Only an administrator can do it")
ONLY_PRIVATE_QUESTION_AUTHOR_ALLOWED_MESSAGE = _("Only the question author can edit a private question")
ONLY_PRIVATE_QUIZ_AUTHOR_ALLOWED_MESSAGE = _("Only the quiz author can edit a private quiz")
ONLY_QUESTION_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE = _(
    "Only the question author or a super-contributor can edit a public question"
)
ONLY_QUIZ_AUTHOR_OR_SUPER_CONTRIBUTOR_ALLOWED_MESSAGE = _(
    "Only the quiz author or a super-contributor can edit a public quiz"
)
ADMIN_REQUIRED_EDIT_FIELD_MESSAGE_FULL = f"{ADMIN_REQUIRED_EDIT_FIELD_MESSAGE}. {ONLY_ADMIN_ALLOWED_MESSAGE}."
