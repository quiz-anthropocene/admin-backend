from django.test import TestCase
from django.urls import reverse

from contributions.factories import CommentFactory
from contributions.models import Comment
from core import constants
from users import constants as user_constants
from users.factories import DEFAULT_PASSWORD, UserFactory


CONTRIBUTIONS_DETAIL_URLS = [
    "contributions:detail_view",
    "contributions:detail_edit",
    "contributions:detail_reply_create",
]


class CommentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("contributions:list")
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.comment_1 = CommentFactory()
        cls.comment_2 = CommentFactory()

    def test_only_contributor_can_access_comment_list(self):
        # anonmyous
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/?next=", response.url)
        # simple user
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        # contributor
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["comments"]), 2)


class CommentDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.comment_1 = CommentFactory()
        cls.comment_2 = CommentFactory()

    def test_anonymous_user_cannot_access_comment_detail(self):
        for detail_url in CONTRIBUTIONS_DETAIL_URLS:
            url = reverse(detail_url, args=[self.comment_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/accounts/login/?next=", response.url)

    def test_contributor_can_access_comment_detail(self):
        self.client.login(email=self.user.email, password=DEFAULT_PASSWORD)
        for detail_url in CONTRIBUTIONS_DETAIL_URLS:
            url = reverse(detail_url, args=[self.comment_1.id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["comment"].id, self.comment_1.id)


class CommentEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.user_admin = UserFactory(roles=[user_constants.USER_ROLE_ADMINISTRATOR])
        cls.comment = CommentFactory(
            text="comment", type=constants.COMMENT_TYPE_COMMENT_QUESTION, status=constants.COMMENT_STATUS_PENDING
        )
        cls.comment_with_reply = CommentFactory()
        cls.comment_reply = CommentFactory(
            text="reply", author=cls.user_contributor, type=constants.COMMENT_TYPE_REPLY, parent=cls.comment_with_reply
        )

    def test_contributor_can_access_comment_edit(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_edit_comment(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.comment.id])
        response = self.client.post(url, data={"status": constants.COMMENT_STATUS_PROCESSED})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).status, constants.COMMENT_STATUS_PROCESSED)

    def test_contributor_cannot_edit_comment(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.comment.id])
        response = self.client.post(url, data={"text": "comment edited as contributor"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).text, "comment")
        # cannot edit 'publish' either
        response = self.client.post(url, data={"text": "comment edited again as contributor", "publish": True})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).publish, False)

    def test_contributor_can_edit_comment_text_if_author(self):
        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.comment_reply.id])
        response = self.client.post(url, data={"text": "reply edited as author"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment_reply.id).text, "reply edited as author")

    def test_administrator_can_edit_comment(self):
        self.client.login(email=self.user_admin.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_edit", args=[self.comment.id])
        response = self.client.post(
            url, data={"text": "comment edited as admin", "status": constants.COMMENT_STATUS_PROCESSED}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).text, "comment edited as admin")
        # can also edit 'publish'
        url = reverse("contributions:detail_edit", args=[self.comment.id])
        response = self.client.post(
            url,
            data={
                "text": "comment edited again as admin",
                "status": constants.COMMENT_STATUS_PROCESSED,
                "publish": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).publish, True)
        # can also edit replies
        url = reverse("contributions:detail_edit", args=[self.comment_reply.id])
        response = self.client.post(url, data={"text": "reply edited as admin"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment_reply.id).text, "reply edited as admin")


class CommentReplyCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(roles=[])
        cls.user_contributor = UserFactory()
        cls.comment = CommentFactory()
        cls.comment_with_reply = CommentFactory()
        cls.comment_reply = CommentFactory(parent=cls.comment_with_reply)

    def test_contributor_can_access_comment_reply_create(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contributor_can_create_reply_to_comment(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.comment.id])
        response = self.client.post(url, data={"text": "Une réponse", "type": constants.COMMENT_TYPE_REPLY})
        self.assertEqual(response.status_code, 302)  # 201
        self.assertEqual(Comment.objects.count(), 3 + 1)
        self.assertTrue(Comment.objects.get(id=self.comment.id).has_replies)

    def test_contributor_cannot_access_comment_with_reply_reply_create(self):
        self.client.login(email=self.user_contributor.email, password=DEFAULT_PASSWORD)
        url = reverse("contributions:detail_reply_create", args=[self.comment_reply.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/{self.comment_with_reply.id}/", response.url)
