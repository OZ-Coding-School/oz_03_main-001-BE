from django.test import TestCase

from django.test import TestCase
from django.contrib.auth import get_user_model  # AbstracBaseUser 상속을 받는다


# TDD: Test Driven Development (테스트 주도 개발) => 채용공고 => 우대사항: TDD
class UserTestCase(TestCase):
    # 회원가입을 가정하고 => 회원가입 함수 테스트 코드를 작성하려고 합니다.
    # 이메일과 패스워드를 입력받고, 회원가입이 정상적으로 잘 이뤄졌는지 체크

    def test_create_user(self):  # 일반 유저 생성 테스트 함수
        email = "giung@gmail.com"
        password = "password123"

        user = get_user_model().objects.create_user(email=email, password=password)

        # 유저가 정상적으로 잘 만들어졌는지 확인
        self.assertEqual(user.email, email)

        # self.assertEqual(user.check_password(password), True)
        self.assertTrue(user.check_password(password))

        # self.assertEqual(user.is_superuser, False)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):  # 슈퍼 유저 생성 테스트 함수
        email = "giung_super@gmail.com"
        password = "password123"

        super_user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
