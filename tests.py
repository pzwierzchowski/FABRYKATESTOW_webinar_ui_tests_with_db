import unittest
import pymysql
from selenium import webdriver
import helper

new_todo_input = 'newTodoInput'
new_todo_add_button = 'addTodoBtn'
url = 'http://localhost:3000'
mark_as_done_button = "//ul[@id='incompletes']//i[@class='far fa-square']"
delete_task_from_completed_list_button = "//ul[@id='completes']//i[@class='fas fa-times']"


class Tests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='todos_db',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

    def tearDown(self):
        self.driver.quit()

    def test1_add_new_task(self):

        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM todos where task='test'"
                cursor.execute(sql)

        finally:
            self.connection.commit()

        self.driver.find_element_by_id(new_todo_input).send_keys('test')
        self.driver.find_element_by_id(new_todo_add_button).click()

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT task,done FROM todos where task = 'test'"
                cursor.execute(sql)
                result = cursor.fetchone()
                assert result == {'task': 'test', 'done': 0}, 'ups, mamy problem'
                print('response: ' + str(result))
        finally:
            self.connection.commit()

    def test2_mark_task_as_done(self):

        helper.wait_for_visibility_of_element(self.driver, mark_as_done_button)
        self.driver.find_element_by_xpath(mark_as_done_button).click()

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT task,done FROM todos where task = 'test'"
                cursor.execute(sql)
                result = cursor.fetchone()
                assert result == {'task': 'test', 'done': 1}, 'ups, mamy problem'
                print('response: ' + str(result))
        finally:
            self.connection.commit()

    def test3_delete_task(self):

        helper.wait_for_visibility_of_element(self.driver, delete_task_from_completed_list_button)
        self.driver.find_element_by_xpath(delete_task_from_completed_list_button).click()

        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT count(1) FROM todos where task = 'test'"
                cursor.execute(sql)
                result = cursor.fetchone()
                assert result == {'count(1)': 0}, 'ups, mamy problem'
                print('response: ' + str(result))
        finally:
            self.connection.close()


if __name__ == '__main__':
    unittest.main()
