import os
import uuid

import requests
from django.conf import settings
from django.core.management import BaseCommand

from core.utils import s3
from questions.models import Question
from quizs.models import Quiz


IMAGE_RAW_PREFIX = "https://raw.githubusercontent.com/quiz-anthropocene/public-frontend/master"


class Command(BaseCommand):
    """
    One-shot command to migrate images hosted on Github to the new S3 destination
    """

    def handle(self, *args, **options):
        self.transfer_question_images()
        self.transfer_quiz_images()

    def transfer_question_images(self):
        for question in Question.objects.all():
            image_url = question.answer_image_url
            if image_url.startswith(IMAGE_RAW_PREFIX):
                image_filename = image_url.split("/")[-1]
                image_extension = image_filename.split(".")[1]
                print(question.id, image_filename)
                # download image
                response = requests.get(image_url, allow_redirects=True)
                # store image
                open(image_filename, "wb").write(response.content)
                # s3 upload
                bucket = s3.get_bucket(settings.S3_BUCKET_NAME)
                s3_image_filename = f"{str(question.id).zfill(6)}-{str(uuid.uuid4())[:4]}.{image_extension}"
                image_key = f"{settings.STORAGE_UPLOAD_KINDS['question_answer_image']['key_path']}/{s3_image_filename}"
                print(image_key)
                s3_presigned_post = s3.create_presigned_post(bucket, image_key)
                with open(image_filename, "rb") as f:
                    files = {"file": (image_filename, f)}
                    response = requests.post(s3_presigned_post["url"], data=s3_presigned_post["fields"], files=files)
                # s3 upload alternative (access denied with current bucket policy)
                # response = s3.upload_object(bucket, image_filename, image_key)
                # print(response)
                # update question
                s3_image_url = f"{s3_presigned_post['url']}/{image_key}"
                print(s3_image_url)
                Question.objects.filter(id=question.id).update(answer_image_url=s3_image_url)
                # delete local image
                os.remove(image_filename)

    def transfer_quiz_images(self):
        for quiz in Quiz.objects.all():
            image_url = quiz.image_background_url
            print(quiz.id, image_url)
            if image_url.startswith(IMAGE_RAW_PREFIX):
                image_filename = image_url.split("/")[-1]
                image_extension = image_filename.split(".")[1]
                print(quiz.id, image_filename)
                # download image
                response = requests.get(image_url, allow_redirects=True)
                # store image
                open(image_filename, "wb").write(response.content)
                # s3 upload
                bucket = s3.get_bucket(settings.S3_BUCKET_NAME)
                s3_image_filename = f"{str(quiz.id).zfill(6)}-{str(uuid.uuid4())[:4]}.{image_extension}"
                image_key = f"{settings.STORAGE_UPLOAD_KINDS['quiz_image_background']['key_path']}/{s3_image_filename}"
                print(image_key)
                s3_presigned_post = s3.create_presigned_post(bucket, image_key)
                with open(image_filename, "rb") as f:
                    files = {"file": (image_filename, f)}
                    response = requests.post(s3_presigned_post["url"], data=s3_presigned_post["fields"], files=files)
                # s3 upload alternative (access denied with current bucket policy)
                # response = s3.upload_object(bucket, image_filename, image_key)
                # print(response)
                # update quiz
                s3_image_url = f"{s3_presigned_post['url']}/{image_key}"
                print(s3_image_url)
                Quiz.objects.filter(id=quiz.id).update(image_background_url=s3_image_url)
                # delete local image
                os.remove(image_filename)
