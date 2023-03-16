"""
Testing module for user_manager.py and queries.py
"""

# Core Modules
# from time import sleep

# from queries import QueryData as Qd
from user_manager import UserManager

test_user_1 = UserManager(name='test_user_1', password='test_pwd_1')
test_user_2 = UserManager(name='test_user_2', password='test_pwd_2')
test_user_3 = UserManager(name='test_user_3', password='test_pwd_3')
test_user_4 = UserManager(name='test_user_4', password='test_pwd_4')
test_user_5 = UserManager(name='test_user_5', password='test_pwd_5')
test_user_6 = UserManager(name='test_user_6', password='test_pwd_6')

# print(test_user_4.verification)
# print(test_user_5.verification)
# test_user_5.verification = True


# test_user_6.update_user()
