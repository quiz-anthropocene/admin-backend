import pandas as pd
from django.core.management import BaseCommand
from django.db.models import F
from django.utils import timezone

from core import constants
from core.models import Configuration
from questions.models import Question
from quizs.models import Quiz
from stats.models import (  # QuestionAggStat,; QuizAggStat,
    DailyStat,
    QuestionAnswerEvent,
    QuestionFeedbackEvent,
    QuizAnswerEvent,
    QuizFeedbackEvent,
)


configuration = Configuration.get_solo()


class Command(BaseCommand):
    """
    Usage:
    python manage.py generate_daily_stats

    Daily stats
    - total number of answers
    - total number of answers from questions
    - total number of answers from quizs
    - total number of quizs played
    - total number of feedbacks (like/dislike)
    answers per hour ?


    Why pandas ?
    to do queries in memory instead of querying the database each time
    """

    help = """Generate Daily stats and clean (Question) Event stats"""

    def handle(self, *args, **kwargs):
        print("=== generate_daily_stats running")
        print("it will only run on QuestionAnswerEvent, QuizAnswerEvent & QuestionFeedbackEvent")
        self.cleanup_question_answer_events()
        self.cleanup_question_feedback_events()
        self.sumup_quiz_answer_events()
        self.sumup_quiz_feedback_events()

        # update configuration
        configuration.daily_stat_last_aggregated = timezone.now()
        configuration.save()

    def cleanup_question_answer_events(self):
        """
        loop on QuestionAnswerEvent
        - update QuestionAggStat 'answer_count' and 'answer_success_count'
        - update DailyStat
            - global 'question_answer_count' and 'question_answer_from_quiz_count'
            - hour split 'question_answer_count' and 'question_answer_from_quiz_count'

        Note: we don't delete QuestionAnswerEvent anymore
        """
        print("=== starting QuestionAnswerEvent cleanup")

        question_stats = (
            QuestionAnswerEvent.objects.select_related("question")
            .annotate(question_visibility=F("question__visibility"))
            .filter(created__gte=configuration.daily_stat_last_aggregated)
        )
        question_stats_df = pd.DataFrame.from_records(question_stats.values())
        print(f"{question_stats_df.shape[0]} new answers")

        if question_stats_df.shape[0]:
            # aggregate by question_id
            question_id_list = question_stats_df["question_id"].unique()
            print(f"{len(question_id_list)} unique questions")

            # loop on unique question ids
            for question_id in question_id_list:
                question = Question.objects.get(pk=question_id)
                question_id_df = question_stats_df[question_stats_df["question_id"] == question_id]
                # # get number of stats
                # question_id_stat_count = question_id_df.shape[0]
                # get number of stats per type
                question_id_answer_count = question_id_df.shape[0]
                question_id_answer_correct_count = question_id_df[
                    question_id_df["choice"] == question.answer_correct
                ].shape[0]
                # update question agg_stats
                question.agg_stats.answer_count += question_id_answer_count
                question.agg_stats.answer_success_count += question_id_answer_correct_count
                # save question agg_stats
                question.agg_stats.save()

            # aggregate by day / hour
            question_stats_df["created_date"] = [d.date() for d in question_stats_df["created"]]
            question_stats_df["created_hour"] = [d.time().hour for d in question_stats_df["created"]]
            # get list of unique dates
            date_list = question_stats_df["created_date"].unique()
            print(f"{len(date_list)} unique dates")

            # loop on unique dates
            for date_unique in date_list:
                daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
                date_df = question_stats_df[question_stats_df["created_date"] == date_unique]
                # get number of stats
                date_stat_count = date_df.shape[0]
                date_stat_public_count = date_df[date_df["question_visibility"] != constants.VISIBILITY_PRIVATE].shape[
                    0
                ]
                date_stat_from_quiz_count = date_df[date_df["source"] == "quiz"].shape[0]
                # update daily stat
                daily_stat.question_answer_count += date_stat_count
                daily_stat.question_public_answer_count += date_stat_public_count
                daily_stat.question_answer_from_quiz_count += date_stat_from_quiz_count

                # get list of unique date hours
                date_hour_list = date_df["created_hour"].unique()
                # loop on unique hours
                for date_hour_unique in date_hour_list:
                    date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                    # get number of stats
                    date_hour_stat_count = date_hour_df.shape[0]
                    date_hour_stat_from_quiz_count = date_hour_df[date_hour_df["source"] == "quiz"].shape[0]
                    # update daily stat hour count
                    daily_stat.hour_split[str(date_hour_unique)]["question_answer_count"] += date_hour_stat_count
                    daily_stat.hour_split[str(date_hour_unique)][
                        "question_answer_from_quiz_count"
                    ] += date_hour_stat_from_quiz_count

                # save daily stat
                daily_stat.save()

    def cleanup_question_feedback_events(self):
        """
        loop on QuestionFeedbackEvent
        - update QuestionAggStat 'like_count' and 'dislike_count'
        - update DailyStat
            - global 'question_feedback_count' and 'question_feedback_from_quiz_count'
            - hour split 'question_feedback_count' and 'question_feedback_from_quiz_count'

        Note: we don't delete QuestionFeedbackEvent anymore
        """
        print("=== starting QuestionFeedbackEvent cleanup")

        question_feedbacks = (
            QuestionFeedbackEvent.objects.select_related("question")
            .annotate(question_visibility=F("question__visibility"))
            .filter(created__gte=configuration.daily_stat_last_aggregated)
        )
        question_feedbacks_df = pd.DataFrame.from_records(question_feedbacks.values())
        print(f"{question_feedbacks_df.shape[0]} new feedbacks")

        if question_feedbacks_df.shape[0]:
            # aggregate by question_id
            question_id_list = question_feedbacks_df["question_id"].unique()
            print(f"{len(question_id_list)} unique questions")

            # loop on unique question ids
            for question_id in question_id_list:
                question = Question.objects.get(pk=question_id)
                question_id_df = question_feedbacks_df[question_feedbacks_df["question_id"] == question_id]
                # # get number of feedbacks
                # question_id_feedback_count = question_id_df.shape[0]
                # get number of feedbacks per type
                question_id_like_count = question_id_df[question_id_df["choice"] == "like"].shape[0]
                question_id_dislike_count = question_id_df[question_id_df["choice"] == "dislike"].shape[0]
                # update question agg_stats
                question.agg_stats.like_count += question_id_like_count
                question.agg_stats.dislike_count += question_id_dislike_count
                # save question agg_stats
                question.agg_stats.save()

            # aggregate by day / hour
            question_feedbacks_df["created_date"] = [d.date() for d in question_feedbacks_df["created"]]
            question_feedbacks_df["created_hour"] = [d.time().hour for d in question_feedbacks_df["created"]]
            # get list of unique dates
            date_list = question_feedbacks_df["created_date"].unique()
            print(f"{len(date_list)} unique dates")

            # loop on unique dates
            for date_unique in date_list:
                daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
                date_df = question_feedbacks_df[question_feedbacks_df["created_date"] == date_unique]
                # get number of feedbacks
                date_feedback_count = date_df.shape[0]
                date_feedback_from_quiz_count = date_df[date_df["source"] == "quiz"].shape[0]
                # update daily stat
                daily_stat.question_feedback_count += date_feedback_count
                daily_stat.question_feedback_from_quiz_count += date_feedback_from_quiz_count

                # get list of unique date hours
                date_hour_list = date_df["created_hour"].unique()
                # loop on unique hours
                for date_hour_unique in date_hour_list:
                    date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                    # get number of feedbacks
                    date_hour_feedback_count = date_hour_df.shape[0]
                    date_hour_feedback_from_quiz_count = date_hour_df[date_hour_df["source"] == "quiz"].shape[0]
                    # update daily stat hour count
                    daily_stat.hour_split[str(date_hour_unique)]["question_feedback_count"] += date_hour_feedback_count
                    daily_stat.hour_split[str(date_hour_unique)][
                        "question_feedback_from_quiz_count"
                    ] += date_hour_feedback_from_quiz_count

                # save daily stat
                daily_stat.save()

    def sumup_quiz_answer_events(self):
        """
        loop on QuizAnswerEvent
        - update QuizAggStat 'answer_count'
        - update DailyStat
            - global 'quiz_answer_count'
            - hour split 'quiz_answer_count'

        TODO: how to keep score ?
        """
        print("=== starting QuizAnswerEvent sumup")

        quiz_stats = (
            QuizAnswerEvent.objects.select_related("quiz")
            .annotate(quiz_visibility=F("quiz__visibility"))
            .filter(created__gte=configuration.daily_stat_last_aggregated)
        )
        quiz_stats_df = pd.DataFrame.from_records(quiz_stats.values())
        print(f"{quiz_stats_df.shape[0]} new answers")

        if quiz_stats_df.shape[0]:
            # aggregate by quiz_id
            quiz_id_list = quiz_stats_df["quiz_id"].unique()
            print(f"{len(quiz_id_list)} unique quizs")

            # loop on unique quiz ids
            for quiz_id in quiz_id_list:
                quiz = Quiz.objects.get(pk=quiz_id)
                quiz_id_df = quiz_stats_df[quiz_stats_df["quiz_id"] == quiz_id]
                # # get number of stats
                quiz_id_answer_count = quiz_id_df.shape[0]
                # update quiz agg_stats
                quiz.agg_stats.answer_count += quiz_id_answer_count
                # save quiz agg_stats
                quiz.agg_stats.save()

            # aggregate by day / hour
            quiz_stats_df["created_date"] = [d.date() for d in quiz_stats_df["created"]]
            quiz_stats_df["created_hour"] = [d.time().hour for d in quiz_stats_df["created"]]
            # get list of unique dates
            date_list = quiz_stats_df["created_date"].unique()
            print(f"{len(date_list)} unique dates")

            # loop on unique dates
            for date_unique in date_list:
                daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
                date_df = quiz_stats_df[quiz_stats_df["created_date"] == date_unique]
                # get number of stats
                date_stat_count = date_df.shape[0]
                date_public_stat_count = date_df[date_df["quiz_visibility"] != constants.VISIBILITY_PRIVATE].shape[0]
                # update daily stat
                daily_stat.quiz_answer_count += date_stat_count
                daily_stat.quiz_public_answer_count += date_public_stat_count

                # get list of unique date hours
                date_hour_list = date_df["created_hour"].unique()
                # loop on unique hours
                for date_hour_unique in date_hour_list:
                    date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                    # get number of stats
                    date_hour_stat_count = date_hour_df.shape[0]
                    # update daily stat hour count
                    daily_stat.hour_split[str(date_hour_unique)]["quiz_answer_count"] += date_hour_stat_count

                # save daily stat
                daily_stat.save()

    def sumup_quiz_feedback_events(self):
        """
        loop on QuizFeedbackEvent
        - update QuizAggStat 'like_count' and 'dislike_count'
        - update DailyStat
            - global 'quiz_feedback_count'
            - hour split 'quiz_feedback_count'

        TODO: how to keep score ?
        """
        print("=== starting QuizFeedbackEvent sumup")

        quiz_feedbacks = (
            QuizFeedbackEvent.objects.select_related("quiz")
            .annotate(quiz_visibility=F("quiz__visibility"))
            .filter(created__gte=configuration.daily_stat_last_aggregated)
        )
        quiz_feedbacks_df = pd.DataFrame.from_records(quiz_feedbacks.values())
        print(f"{quiz_feedbacks_df.shape[0]} new answers")

        if quiz_feedbacks_df.shape[0]:
            # aggregate by quiz_id
            quiz_id_list = quiz_feedbacks_df["quiz_id"].unique()
            print(f"{len(quiz_id_list)} unique quizs")

            # loop on unique quiz ids
            for quiz_id in quiz_id_list:
                quiz = Quiz.objects.get(pk=quiz_id)
                quiz_id_df = quiz_feedbacks_df[quiz_feedbacks_df["quiz_id"] == quiz_id]
                # get number of feedbacks per type
                quiz_id_like_count = quiz_id_df[quiz_id_df["choice"] == "like"].shape[0]
                quiz_id_dislike_count = quiz_id_df[quiz_id_df["choice"] == "dislike"].shape[0]
                # update quiz agg_stats
                quiz.agg_stats.like_count += quiz_id_like_count
                quiz.agg_stats.dislike_count += quiz_id_dislike_count
                # save quiz agg_stats
                quiz.agg_stats.save()

            # aggregate by day / hour
            quiz_feedbacks_df["created_date"] = [d.date() for d in quiz_feedbacks_df["created"]]
            quiz_feedbacks_df["created_hour"] = [d.time().hour for d in quiz_feedbacks_df["created"]]
            # get list of unique dates
            date_list = quiz_feedbacks_df["created_date"].unique()
            print(f"{len(date_list)} unique dates")

            # loop on unique dates
            for date_unique in date_list:
                daily_stat, created = DailyStat.objects.get_or_create(date=date_unique)
                date_df = quiz_feedbacks_df[quiz_feedbacks_df["created_date"] == date_unique]
                # get number of feedbacks
                date_stat_count = date_df.shape[0]
                # update daily stat
                daily_stat.quiz_feedback_count += date_stat_count

                # get list of unique date hours
                date_hour_list = date_df["created_hour"].unique()
                # loop on unique hours
                for date_hour_unique in date_hour_list:
                    date_hour_df = date_df[date_df["created_hour"] == date_hour_unique]
                    # get number of feedbacks
                    date_hour_stat_count = date_hour_df.shape[0]
                    # update daily stat hour count
                    daily_stat.hour_split[str(date_hour_unique)]["quiz_feedback_count"] += date_hour_stat_count

                # save daily stat
                daily_stat.save()
