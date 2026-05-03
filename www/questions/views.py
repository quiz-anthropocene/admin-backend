import datetime
import io
import re

import pandas as pd
from dal import autocomplete
from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from activity.utilities import create_event
from api.questions.serializers import QuestionFullStringSerializer
from categories.models import Category
from contributions.forms import CommentCreateForm
from contributions.models import Comment
from contributions.tables import CommentTable
from core import constants
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from core.utils.s3 import S3Upload
from history.utilities import get_diff_between_two_history_records
from questions.filters import QuestionFilter
from questions.forms import QUESTION_FORM_FIELDS, QuestionCreateForm, QuestionEditForm
from questions.models import Question
from questions.tables import QuestionQuizTable, QuestionTable
from quizs.models import QuizQuestion
from stats.models import QuestionAggStat
from tags.models import Tag
from users import constants as user_constants


class QuestionListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "questions/list.html"
    context_object_name = "questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category", "author", "validator").prefetch_related("tags", "quizs")
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class QuestionDetailView(ContributorUserRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail_view.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        # context["question_dict"] = model_to_dict(question, fields=[field.name for field in question._meta.fields])
        context["question_dict"] = QuestionFullStringSerializer(question).data
        return context


class QuestionDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = QuestionEditForm
    template_name = "questions/detail_edit.html"
    success_message = _("The question was updated.")
    # success_url = reverse_lazy("questions:detail_view")

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs.get("pk"))

    def get_form(self, *args, **kwargs):
        """
        - some fields are only editable by the author
        - some fields are only editable by administrators (or question author if private)
        """
        question = self.get_object()
        form = super().get_form(self.form_class)
        if not self.request.user.is_question_author(question):
            form.fields["author_certify_necessary_rights"].disabled = True
            form.fields["author_agree_commercial_use"].disabled = True
        if not self.request.user.can_validate_question(question):
            form.fields["validation_status"].disabled = True
            form.fields["validation_status"].help_text = user_constants.ADMIN_REQUIRED_EDIT_FIELD_MESSAGE_FULL
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # S3 Upload form
        s3_upload = S3Upload(kind="question_answer_image")
        context["s3_form_values"] = s3_upload.form_values
        context["s3_upload_config"] = s3_upload.config
        return context

    def form_valid(self, form):
        question_before = self.get_object()
        question = form.save(commit=False)
        # Change detected on the validation_status field
        if question_before.validation_status != question.validation_status:
            # Question validated! set the validator data + create event
            if question.is_validated:
                question.validator = self.request.user
                question.validation_date = timezone.now()
                if not question.is_private:
                    create_event(user=self.request.user, event_verb="VALIDATED", event_object=question)
            # Question not validated anymore... reset the validator data
            elif question_before.is_validated:
                question.validator = None
                question.validation_date = None
        question.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.get_success_message(form.cleaned_data),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("questions:detail_view", args=[self.kwargs.get("pk")])


class QuestionDetailQuizListView(ContributorUserRequiredMixin, SingleTableMixin, ListView):
    model = QuizQuestion
    template_name = "questions/detail_quizs.html"
    context_object_name = "question_quizs"
    table_class = QuestionQuizTable

    def get(self, request, *args, **kwargs):
        self.question = Question.objects.get(id=self.kwargs.get("pk"))
        return super().get(request, *args, **kwargs)

    def get_table_data(self):
        return self.question.quizquestion_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.question
        return context


class QuestionDetailCommentListView(ContributorUserRequiredMixin, SingleTableMixin, FormMixin, ListView):
    model = Comment
    template_name = "questions/detail_comments.html"
    context_object_name = "question_contributions"
    table_class = CommentTable
    form_class = CommentCreateForm

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__id=self.kwargs.get("pk"))
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id=self.kwargs.get("pk"))
        return context

    def get_initial(self):
        return {
            "type": constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR,
            "question": self.kwargs.get("pk"),
            "status": constants.COMMENT_STATUS_PROCESSED,
            "author": self.request.user,
            "parent": None,
        }

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        # response
        messages.add_message(self.request, messages.SUCCESS, self.get_success_message(form.cleaned_data))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

    def get_success_message(self, cleaned_data):
        return _("Your message was created.")

    def get_success_url(self):
        return reverse_lazy("questions:detail_comments", args=[self.kwargs.get("pk")])


class QuestionDetailStatsView(ContributorUserRequiredMixin, DetailView):
    model = QuestionAggStat
    template_name = "questions/detail_stats.html"
    context_object_name = "question_stats"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_agg_stat_dict"] = model_to_dict(self.get_object())
        del context["question_agg_stat_dict"]["question"]
        context["question"] = Question.objects.get(id=self.kwargs.get("pk"))
        return context


class QuestionDetailHistoryView(ContributorUserRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail_history.html"
    context_object_name = "question"

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_history"] = self.get_object().history.all()
        context["question_history_delta"] = list()
        for record in context["question_history"]:
            new_record = record
            if new_record.prev_record:
                delta_changes = get_diff_between_two_history_records(
                    new_record,
                    old_record=new_record.prev_record,
                    excluded_fields=Question.QUESTION_RELATION_FIELDS,
                    returns="changes",
                )
                context["question_history_delta"].append(delta_changes)
            else:
                # probably a create action
                # we create the diff ourselves because there isn't any previous record
                delta_fields = QUESTION_FORM_FIELDS + Question.QUESTION_FLATTEN_FIELDS
                delta_new = [{"field": k, "new": v} for k, v in record.__dict__.items() if k in delta_fields if v]
                context["question_history_delta"].append(delta_new)
        return context


class QuestionCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = "questions/create.html"
    success_url = reverse_lazy("questions:list")
    # success_message = ""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        # create event
        if not self.object.is_private:
            create_event(user=self.request.user, event_verb="CREATED", event_object=self.object)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.get_success_message(form.cleaned_data),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        success_url = super().get_success_url()
        next_url = self.request.GET.get("next", None)
        # sanitize next_url
        if next_url:
            # safe_url = get_safe_url(self.request, param_name="next")
            # if safe_url:
            #     return safe_url
            return next_url
        return success_url

    def get_success_message(self, cleaned_data):
        question_text_short = self.object.text if (len(self.object.text) < 20) else (self.object.text[:18] + "…")
        question_url = reverse_lazy("questions:detail_view", args=[self.object.id])
        question_link = (
            f"<a href='{question_url}' title='{self.object.text}'><strong>{question_text_short}</strong></a>"
        )
        return mark_safe(_("The question {question_link} was created.").format(question_link=question_link))


class QuestionAutocomplete(ContributorUserRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Question.objects.public_or_by_author(author=self.request.user)

        if self.q:
            if self.q.replace(" ", "").isdigit():
                qs = qs.filter(id=self.q)
            else:
                qs = qs.filter(text__icontains=self.q)

        return qs


# ---------------------------------------------------------------------------
# ODS import
# ---------------------------------------------------------------------------

ODS_SHEET_NAME = "Résultats de la requête"

ODS_REQUIRED_COLUMNS = [
    "ID",
    "Text",
    "Type",
    "Difficulty",
    "Language",
    "Answer Choice A",
    "Answer Choice B",
    "Answer Correct",
    "Has Ordered Answers",
]

ODS_VALID_TYPES = ["QCM", "QCM-RM", "VF"]
ODS_VALID_LANGUAGES = ["FRENCH", "ENGLISH", "ITALIAN", "GERMAN", "SPANISH"]


class ODSUploadForm(forms.Form):
    ods_file = forms.FileField(
        label=_("Fichier ODS"),
        help_text=_("Fichier .ods avec l'onglet « Résultats de la requête »"),
    )

    def clean_ods_file(self):
        f = self.cleaned_data["ods_file"]
        if not f.name.lower().endswith(".ods"):
            raise forms.ValidationError(_("Le fichier doit être au format .ods"))
        return f


class QuestionImportODSView(ContributorUserRequiredMixin, FormView):
    template_name = "questions/import_ods.html"
    form_class = ODSUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("results", None)
        return context

    def form_valid(self, form):
        ods_file = form.cleaned_data["ods_file"]
        results = self._process_ods(ods_file)
        context = self.get_context_data(form=form, results=results)
        return self.render_to_response(context)

    # ------------------------------------------------------------------
    # Core parsing
    # ------------------------------------------------------------------

    def _process_ods(self, ods_file):
        results = {"created": [], "updated": [], "errors": [], "global_error": None}

        try:
            df = pd.read_excel(
                io.BytesIO(ods_file.read()),
                sheet_name=ODS_SHEET_NAME,
                engine="odf",
                dtype=str,
                keep_default_na=False,
            )
        except Exception as e:
            msg = str(e)
            if "sheet" in msg.lower() or "worksheet" in msg.lower():
                results["global_error"] = (
                    f"L'onglet « {ODS_SHEET_NAME} » est introuvable dans le fichier."
                )
            else:
                results["global_error"] = f"Erreur lors de la lecture du fichier : {msg}"
            return results

        missing = [c for c in ODS_REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            results["global_error"] = f"Colonnes manquantes : {', '.join(missing)}"
            return results

        for idx, row in df.iterrows():
            row_num = idx + 2  # 1-indexed + header row
            try:
                self._process_row(row, results)
            except Exception as e:
                results["errors"].append({"row": row_num, "error": str(e)})

        return results

    def _process_row(self, row, results):
        def val(col, default=""):
            v = row.get(col, default)
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return default
            return str(v).strip()

        def parse_bool(col):
            v = val(col)
            if v == "True":
                return True
            if v == "False":
                return False
            if v == "":
                return None
            raise ValueError(f"Valeur invalide pour « {col} » : « {v} » (attendu : True ou False)")

        # --- ID ---
        id_str = val("ID")
        if not id_str:
            raise ValueError("Le champ « ID » est vide")
        try:
            question_id = int(float(id_str))
        except ValueError:
            raise ValueError(f"L'ID « {id_str} » n'est pas un entier valide")

        # --- Required text fields ---
        text = val("Text")
        if not text:
            raise ValueError("Le champ « Text » est vide")

        q_type = val("Type")
        if q_type not in ODS_VALID_TYPES:
            raise ValueError(f"Type invalide : « {q_type} » (attendu : {', '.join(ODS_VALID_TYPES)})")

        difficulty_str = val("Difficulty")
        try:
            difficulty = int(float(difficulty_str))
            if difficulty not in range(5):
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError(f"Difficulté invalide : « {difficulty_str} » (attendu : 0–4)")

        language = val("Language")
        if language not in ODS_VALID_LANGUAGES:
            raise ValueError(f"Langue invalide : « {language} » (attendu : {', '.join(ODS_VALID_LANGUAGES)})")

        answer_choice_a = val("Answer Choice A")
        answer_choice_b = val("Answer Choice B")
        if not answer_choice_a or not answer_choice_b:
            raise ValueError("Les choix de réponse A et B sont obligatoires")

        answer_correct = val("Answer Correct")
        if not answer_correct:
            raise ValueError("La réponse correcte (Answer Correct) est obligatoire")

        has_ordered = parse_bool("Has Ordered Answers")
        if has_ordered is None:
            raise ValueError("Le champ « Has Ordered Answers » est vide (attendu : True ou False)")
        # Model rule: VF questions must always have ordered answers
        if q_type == constants.QUESTION_TYPE_VF:
            has_ordered = True

        # --- Category ---
        category = None
        category_id_str = val("Category ID")
        if category_id_str:
            try:
                cat_id = int(float(category_id_str))
                category = Category.objects.get(id=cat_id)
            except Category.DoesNotExist:
                raise ValueError(f"Catégorie ID {category_id_str} introuvable")
            except (ValueError, TypeError):
                raise ValueError(f"Category ID invalide : « {category_id_str} »")

        # --- Tags ---
        tag_names = self._parse_curly_list(val("Tag List"))
        tags_qs = Tag.objects.filter(name__in=tag_names) if tag_names else Tag.objects.none()

        # --- Quiz list ---
        quiz_ids = self._parse_curly_list_int(val("Quiz List"))

        # --- Author / Validator ---
        from django.contrib.auth import get_user_model
        User = get_user_model()

        author = None
        author_id_str = val("Author ID")
        if author_id_str:
            try:
                author = User.objects.filter(id=int(float(author_id_str))).first()
            except (ValueError, TypeError):
                pass

        validator = None
        validator_id_str = val("Validator ID")
        if validator_id_str:
            try:
                validator = User.objects.filter(id=int(float(validator_id_str))).first()
            except (ValueError, TypeError):
                pass

        # --- Dates ---
        def parse_date_field(col):
            s = val(col)
            if not s:
                return None
            from django.utils.dateparse import parse_date, parse_datetime
            dt = parse_datetime(s)
            if dt:
                return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
            d = parse_date(s)
            if d:
                return timezone.make_aware(datetime.datetime.combine(d, datetime.time.min))
            return None

        created = parse_date_field("Created")
        validation_date = parse_date_field("Validation Date")

        # --- Boolean author fields ---
        author_agree = parse_bool("Author Agree Commercial Use")
        author_certify = parse_bool("Author Certify Necessary Rights")

        # --- Build field dict ---
        fields = {
            "text": text,
            "hint": val("Hint"),
            "type": q_type,
            "difficulty": difficulty,
            "language": language,
            "answer_choice_a": answer_choice_a,
            "answer_choice_b": answer_choice_b,
            "answer_choice_c": val("Answer Choice C"),
            "answer_choice_d": val("Answer Choice D"),
            "answer_correct": answer_correct,
            "has_ordered_answers": has_ordered,
            "answer_explanation": val("Answer Explanation"),
            "answer_audio_url": val("Answer Audio URL"),
            "answer_audio_url_text": val("Answer Audio URL Text"),
            "answer_video_url": val("Answer Video URL"),
            "answer_video_url_text": val("Answer Video URL Text"),
            "answer_source_accessible_url": val("Answer Source Accessible URL"),
            "answer_source_accessible_url_text": val("Answer Source Accessible URL Text"),
            "answer_source_scientific_url": val("Answer Source Scientific URL"),
            "answer_source_scientific_url_text": val("Answer Source Scientific URL Text"),
            "answer_book_recommendation": val("Answer Book Recommendation"),
            "answer_image_url": val("Answer Image URL"),
            "answer_image_url_text": val("Answer Image URL Text"),
            "answer_extra_info": val("Answer Extra Info"),
            "validation_status": val("Validation Status") or constants.VALIDATION_STATUS_DRAFT,
            "visibility": val("Visibility") or constants.VISIBILITY_PUBLIC,
            "category": category,
            "category_string": val("Category String"),
            "author": author,
            "author_string": val("Author String"),
            "validator": validator,
            "validator_string": val("Validator String"),
            "quiz_list": quiz_ids,
        }

        if author_agree is not None:
            fields["author_agree_commercial_use"] = author_agree
        if author_certify is not None:
            fields["author_certify_necessary_rights"] = author_certify
        if created:
            fields["created"] = created
        if validation_date:
            fields["validation_date"] = validation_date

        # --- Create or update ---
        try:
            question = Question.objects.get(id=question_id)
            for k, v in fields.items():
                setattr(question, k, v)
            question.save()
            question.tags.set(tags_qs)
            question.tag_list = list(tags_qs.values_list("name", flat=True))
            question.save()
            results["updated"].append({"id": question_id, "text": text[:60]})
        except Question.DoesNotExist:
            question = Question(id=question_id, **fields)
            question.save()
            question.tags.set(tags_qs)
            question.tag_list = list(tags_qs.values_list("name", flat=True))
            question.save()
            results["created"].append({"id": question_id, "text": text[:60]})

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_curly_list(s):
        """Parse {Tag1,"Tag with space",Tag2} into a list of strings."""
        if not s:
            return []
        s = s.strip()
        if not (s.startswith("{") and s.endswith("}")):
            raise ValueError(f"Format de liste invalide : « {s} » (attendu : {{item1,item2}})")
        inner = s[1:-1].strip()
        if not inner:
            return []
        items = []
        for m in re.finditer(r'"([^"]*)"|((?:[^,{}"\\])+)', inner):
            if m.group(1) is not None:
                items.append(m.group(1).strip())
            elif m.group(2) is not None:
                v = m.group(2).strip()
                if v:
                    items.append(v)
        return items

    @staticmethod
    def _parse_curly_list_int(s):
        """Parse {1,2,78} into a list of ints."""
        items = QuestionImportODSView._parse_curly_list(s)
        try:
            return [int(x) for x in items if x]
        except ValueError as e:
            raise ValueError(f"Valeur non-entière dans la liste : {e}")
