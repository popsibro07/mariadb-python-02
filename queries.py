"""
#!/usr/bin/env python3

Backend SQL query handler
"""

# Core Modules
import mariadb


class QueryData:
    """
    Main class for mariadb query handling.
    """

    def __init__(self, host: str = 'localhost', user: str = 'mariadb_admin', password: str = 'root',
                 database: str = 'mariadb_oop_2', **kwargs):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.connect = mariadb.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.cursor = self.connect.cursor()

        super().__init__(**kwargs)

        self.init_tables()

    @property
    def host(self) -> str:
        return self.__host

    @property
    def user(self) -> str:
        return self.__user

    @property
    def password(self) -> str:
        return self.__password

    @property
    def database(self) -> str:
        return self.__database

    @staticmethod
    def default_user_setup() -> str:
        """
        Returns the query of user_data table
        :return: user_data table SQL query"""

        return f"""
        
        CREATE TABLE IF NOT EXISTS `user_data` ( 
        `uid` VARCHAR(200) NOT NULL , 
        `name` TEXT NOT NULL , 
        `password` VARCHAR(300) NOT NULL , 
        `secured` VARCHAR(50) NOT NULL , 
        PRIMARY KEY (`uid`(200))) ENGINE = MyISAM;
        """

    @staticmethod
    def default_key_setup() -> str:

        return f"""
        
        CREATE TABLE IF NOT EXISTS `user_keys` ( 
        `uid` VARCHAR(200) NOT NULL , 
        `pass_key` VARCHAR(200) NOT NULL , 
        PRIMARY KEY (`uid`(200))) ENGINE = MyISAM;
        """

    @staticmethod
    def default_user_logger_setup() -> str:

        return f"""
    
        CREATE TABLE IF NOT EXISTS `user_log` ( 
        `uid` VARCHAR(200) NOT NULL , 
        `last_login_date` VARCHAR(50) NOT NULL , 
        `last_login_time` VARCHAR(50) NOT NULL ,
        `process_count` INT(50) NOT NULL ,
        `description` TEXT(150) NOT NULL ,
        PRIMARY KEY (`uid`(200))) ENGINE = MyISAM;
        """

    @staticmethod
    def default_legacy_user_setup() -> str:

        return f"""

        CREATE TABLE IF NOT EXISTS `legacy_users` ( 
        `uid` VARCHAR(200) NOT NULL , 
        `name` TEXT NOT NULL , 
        `password` VARCHAR(200) NOT NULL ,
        `pass_key` VARCHAR(200) NOT NULL ,  
        `last_login` VARCHAR(50) NOT NULL , 
        PRIMARY KEY (`uid`(200))) ENGINE = MyISAM;
        """

    def execute(self, func: object = None, output: bool = False):

        if func is not None:

            self.cursor.execute(func)
            self.connect.commit()

            if output:
                return self.cursor.fetchall()

        else:
            raise Exception("No specified function.")

    def init_tables(self) -> None:
        self.cursor.execute(self.default_user_setup())
        self.cursor.execute(self.default_key_setup())
        self.cursor.execute(self.default_user_logger_setup())
        self.cursor.execute(self.default_legacy_user_setup())

    @staticmethod
    def read_all_queries(table_name: str) -> str:

        return f"""
        SELECT *
        FROM {table_name};
        """

    @staticmethod
    def read_user_data_fields(table_name: str, columns: str) -> str:

        return f"""
        SELECT {columns}
        FROM {table_name};
        """

    @staticmethod
    def read_user_specific_field(table_name: str, filter_expression: str, column: str) -> str:

        return f"""
        SELECT {column}
        FROM {table_name}
        WHERE {filter_expression};
        """

    @staticmethod
    def create_row_query(table_name: str, data_list: list) -> str:
        values_string = ", ".join(map(str, data_list))

        return f"""
        INSERT INTO {table_name}
        VALUES ({values_string});
        """

    @staticmethod
    def update_rows_query(table_name: str, column_value_pair: str, filter_expression: str) -> str:

        return f"""
        UPDATE {table_name}
        SET {column_value_pair}
        WHERE {filter_expression};
        """

    @staticmethod
    def delete_rows(table_name: str, filter_expression: str) -> str:

        return f"""
        DELETE FROM {table_name}
        WHERE {filter_expression};
        """

    @staticmethod
    def read_using_inner_join(table_columns: str, join_table_1: str, join_table_2: str,
                              common_column: str, table_filter_expression: str) -> str:

        return f"""
        SELECT {table_columns}
        FROM {join_table_1} INNER JOIN {join_table_2} 
        ON {join_table_1}.{common_column} = {join_table_2}.{common_column}
        WHERE {table_filter_expression};
        """
