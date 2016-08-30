import unittest

from selenium import webdriver


class SherlockFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get(u'http://localhost:5000')
        self.login("admin", "admin")

    def test_create_project(self):
        self.create_project("Blabla")

        page_source = self.driver.page_source
        assert "Project Created!" in page_source

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        username_input = self.driver.find_element_by_id("email")
        password_input = self.driver.find_element_by_id("password")
        sign_in_btn = self.driver.find_element_by_id("sign_in")
        username_input.send_keys(username)
        password_input.send_keys(password)
        sign_in_btn.click()

    def create_project(self, name):
        select_project = self.driver.find_element_by_link_text("Select your Project")
        select_project.click()
        new_project = self.driver.find_element_by_link_text("Create a new Project")
        new_project.click()
        project_name = self.driver.find_element_by_id("name")
        project_name.send_keys(name)
        create_btn = self.driver.find_element_by_id("btn_create_project")
        create_btn.click()

if __name__ == "__main__":
    unittest.main()
