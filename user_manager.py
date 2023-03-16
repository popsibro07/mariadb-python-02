"""#!/usr/bin/env python3"""

# Core Modules
# import os
# import time
import uuid
# import datetime

# External Modules
import mariadb
from cryptography.fernet import Fernet

# Classes
from queries import QueryData


# ---------------------------------------------------------------------------------------------------------------------

# TODO: Create user data access authorization methods.
# TODO: Create verified user deleting methods.

# TODO: Update legacy user data structure to include a public key.

# TODO: Streamline the user logging methods. (Too slow)
# TODO: Add threading for multi-user input processing. (Too slow)

# TODO: Read data_file method
# TODO: Create, Update, Delete file

# TODO: user_data_file encrypting and decrypting methods
# TODO: database file encrypting & decrypting methods

# ---------------------------------------------------------------------------------------------------------------------


class UserManager:

    def __init__(self, name: str, password: str, pass_key: bytes = None, uid: str = None,
                 verification: bool = False):

        self.__name = name
        self.__password = password
        self.__pass_key = pass_key
        self.__uid = uid
        self.__verification = verification

        super(UserManager, self).__init__()

        try:
            QueryData()
        except (mariadb.OperationalError, mariadb.ProgrammingError):
            raise Exception("Database Connection Error.")

        self.user_cred_verification()

        # tables.init_tables()
        # self.user_access_log()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def pass_key(self) -> bytes:
        return self.__pass_key

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def verification(self) -> bool:
        return self.__verification

    """

    @name.setter
    def name(self, value: str):
        self.__name = value

    @password.setter
    def password(self, value: str):
        self.__password = value

    @verification.setter
    def verification(self, value: bool):
        self.__verification = value

    @uid.setter
    def uid(self, value: str):
        self.__uid = value
    
    @pass_key.setter
    def pass_key(self, value: bytes):
        self.__pass_key = value
        
    """

    def add_user(self) -> None:

        if not self.verify_user_name():

            raise Exception("Username already exists.")

        else:
            self.__uid = uuid.uuid4()

            self.__pass_key = Fernet.generate_key()
            temp_key = self.__pass_key.decode()

            secure_password = Fernet(self.__pass_key).encrypt(self.__password.encode())
            temp_password = secure_password.decode()

            data_list1 = [f"'{self.__uid}'", f"'{self.__name}'", f"'{temp_password}'", f"'1'"]
            data_list2 = [f"'{self.__uid}'", f"'{temp_key}'"]

            user_instance = QueryData()
            user_instance.execute(func=QueryData.create_row_query(
                    table_name='user_data',
                    data_list=data_list1
            ))
            user_instance.execute(func=QueryData.create_row_query(
                    table_name='user_keys',
                    data_list=data_list2
            ))

            self.user_cred_verification()

    def update_user(self, username: str = None, password: str = None) -> None:

        # -------------------------------------------------------------------------------------------------------------
        if self.__verification:

            if username is None and password is None:
                raise Exception("Either username or password parameter must be filled to update user data.")

            # ---------------------------------------------------------------------------------------------------------
            if username is not None:

                if username != self.__name:

                    user_instance = QueryData()
                    user_instance.execute(func=QueryData.update_rows_query(
                            table_name='user_data',
                            column_value_pair=f"name='{username}'",
                            filter_expression=f"name='{self.__name}'"
                    ))

                    self.__name = username

                else:
                    raise Exception("New username is the same username as before.")

            # ---------------------------------------------------------------------------------------------------------
            if password is not None:

                if password != self.__password:

                    self.get_user_pass_key()

                    encoded_password = password.encode()
                    encrypted_password = Fernet(self.__pass_key).encrypt(encoded_password)
                    decoded_secure_password = encrypted_password.decode()

                    user_instance = QueryData()
                    user_instance.execute(func=QueryData.update_rows_query(
                            table_name='user_data',
                            column_value_pair=f"password='{decoded_secure_password}'",
                            filter_expression=f"uid='{self.__uid}'"
                    ))

                    self.__password = password

                else:
                    raise Exception("You can't reuse the same password.")

        else:
            raise Exception("User credentials does not match.")

        self.user_cred_verification()

    def delete_user(self):

        if self.__verification:

            self.get_user_id()

            user_instance = QueryData()
            user_instance.execute(func=QueryData.delete_rows(
                    table_name='user_data',
                    filter_expression=f"uid='{self.__uid}'"
            ))

            user_instance.execute(func=QueryData.delete_rows(
                    table_name='user_keys',
                    filter_expression=f"uid='{self.__uid}'"
            ))

        else:
            raise Exception("User credentials does not match.")

    def verify_user_name(self) -> bool:

        result = True
        temp_user_data = (self.__name,)

        instance = QueryData()
        sample_data = instance.execute(func=QueryData.read_user_data_fields(
                table_name='user_data',
                columns='name'
        ),
                output=True
        )

        for value in sample_data:

            if value == temp_user_data:
                result = False
            else:
                pass

        return result

    def security_check(self) -> bool:

        instance = QueryData()
        sample_data = instance.execute(func=QueryData.read_user_specific_field(
                column='secured',
                table_name='user_data',
                filter_expression=f"name='{self.__name}'"
        ),
                output=True
        )

        if len(sample_data) > 0:

            if sample_data[0][0] == '1':

                return True

            else:
                return False
        else:
            return False

    def get_user_id(self):

        instance = QueryData()
        sample_id = instance.execute(func=QueryData.read_user_specific_field(
                column='uid',
                table_name='user_data',
                filter_expression=f"name='{self.__name}'"
        ),
                output=True
        )

        if len(sample_id) > 0:

            self.__uid = sample_id[0][0]

        else:
            raise Exception("No user record available.")

    def get_user_pass_key(self):

        self.get_user_id()

        instance = QueryData()
        sample_key = instance.execute(func=QueryData.read_user_specific_field(
                column='pass_key',
                table_name='user_keys',
                filter_expression=f"uid='{self.__uid}'"
        ),
                output=True
        )

        decoded_key = sample_key[0][0]
        self.__pass_key = decoded_key.encode()

    def verify_user_password(self) -> bool:

        # -------------------------------------------------------------------------------------------------------------
        if not self.verify_user_name():

            self.get_user_id()

            instance = QueryData()
            sample_password = instance.execute(func=QueryData.read_user_specific_field(
                    column='password',
                    table_name='user_data',
                    filter_expression=f"uid='{self.__uid}'"
            ),
                    output=True
            )

            decoded_password = sample_password[0][0]

            # ---------------------------------------------------------------------------------------------------------
            if self.security_check():

                self.get_user_pass_key()

                encrypted_password = decoded_password.encode()
                decrypted_password = Fernet(self.__pass_key).decrypt(encrypted_password)
                temp_password = decrypted_password.decode()

                if temp_password == self.__password:
                    return True
                else:
                    return False

            # ---------------------------------------------------------------------------------------------------------
            else:

                if decoded_password == self.__password:
                    return True
                else:
                    return False

        # -------------------------------------------------------------------------------------------------------------
        else:
            return False

    def user_cred_verification(self) -> None:

        if self.verify_user_password():

            self.__verification = True
            # print(self.__name, self.verification)
        else:
            self.__verification = False
            # print(self.__name, self.verification)

    def __repr__(self) -> str:
        pass_data = ""

        for _ in self.__password:
            pass_data = f"{pass_data}*"

        return f"{self.__class__.__name__}(name='{self.__name}', password='{pass_data}')"
