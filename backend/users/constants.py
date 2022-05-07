USER_ROLE_CONTRIBUTOR = "CONTRIBUTOR"
USER_ROLE_SUPER_CONTRIBUTOR = "SUPER-CONTRIBUTOR"
USER_ROLE_ADMINISTRATOR = "ADMINISTRATOR"
USER_ROLE_CHOICES = (
    (USER_ROLE_CONTRIBUTOR, "Contributeur"),
    (USER_ROLE_SUPER_CONTRIBUTOR, "Super Contributeur"),
    (USER_ROLE_ADMINISTRATOR, "Administrateur"),
)

ADMIN_REQUIRED_MESSAGE = (
    "Vous n'avez pas les droits nécessaires pour modifier ce champ (seul un administrateur peut le faire)"
)
