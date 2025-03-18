from ckeditor.fields import RichTextField
from django.db import models
from solo.models import SingletonModel


class Configuration(SingletonModel):
    # basics
    application_name = models.CharField(
        max_length=255,
        default="Quiz de l'Anthropocène",
        editable=False,
        help_text="Le nom de l'application",
    )
    application_tagline = models.CharField(
        max_length=255,
        help_text="La tagline de l'application",
    )
    application_about = RichTextField(blank=True, help_text="A propos de l'application")

    # links
    application_open_source_code_url = models.URLField(
        max_length=500,
        default="https://github.com/quiz-anthropocene",
        editable=False,
        help_text="Le lien vers le code de l'application",
    )
    application_backend_url = models.URLField(
        max_length=500, blank=True, help_text="Le lien vers le backend de l'application"
    )
    application_frontend_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers le frontend de l'application",
    )
    application_frontend_ecoindex_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers le test EcoIndex.fr du frontend",
    )

    # social links
    application_facebook_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers la page Facebook de l'application",
    )
    application_twitter_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers la page Twitter de l'application",
    )
    application_linkedin_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers la page Linkedin de l'application",
    )

    # ngo
    helloasso_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers la page HelloAsso de l'association",
    )
    office_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="L'adresse du bureau de l'association",
    )
    office_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Le lien vers la page du bureau de l'association",
    )

    # timestamps
    daily_stat_last_aggregated = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois qu'a été lancé le script de mise à jour des Daily Stats",  # noqa
    )
    notion_questions_scope_0_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_1_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions (lot 1) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_2_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions (lot 2) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_3_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions (lot 3) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_4_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions (lot 4) ont été importées depuis Notion",  # noqa
    )
    notion_questions_scope_5_last_imported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les questions (lot 5) ont été importées depuis Notion",  # noqa
    )
    github_data_last_exported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que la donnée a été exportée vers Github",  # noqa
    )
    github_stats_last_exported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les stats ont été exportées vers Github",  # noqa
    )
    notion_contributions_last_exported = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="La dernière fois que les contributions exportées vers Notion",  # noqa
    )

    def __str__(self):
        return "Configuration de l'application"

    class Meta:
        verbose_name = "Configuration de l'application"
