from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import unittest
import time


class TestPurbeurre(unittest.TestCase):

    URL = "http://127.0.0.1:8000/"

    def setUp(self):
        self.driver = webdriver.Chrome('chrome_driver/chromedriver.exe')
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(self.URL)
        self.email = "fake_email@email.fr"
        self.password1 = "fake_password1"
        self.password2 = "fake_password1"

    def tearDown(self):
        self.driver.close()

    def click_on_button(self, name):
        button = self.driver.find_element_by_name(name)
        button.click()

    def click_on_link(self, name):
        link = self.driver.find_element_by_name(name)
        link.click()

    def click_on_link_text(self, text):
        text = self.driver.find_element_by_link_text(text)
        text.click()

    def write_user_text(self, name, user_text):
        element = self.driver.find_element_by_name(name)
        element.clear()
        element.send_keys(user_text)

    # def test_result_page_show(self):
    #     self.driver
    #     self.assertEqual(
    #         self.driver.title,
    #         "Pur Beurre - Plateforme pour amateur de nutella"
    #     )

    def test_ajax_search(self):
        element = self.driver.find_element_by_id("query")
        self.assertNotIn("Sélectionner", self.driver.page_source)
        element.clear()
        element.send_keys("pizza")
        time.sleep(1)
        button = self.driver.find_element_by_id("submitQuery")
        button.click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, f"{self.URL}")
        # modal display result (select product)
        self.assertIn("Sélectionner", self.driver.page_source)
        time.sleep(1)

        # close modal
        close_modal = self.driver.find_element_by_class_name("btn-close")
        close_modal.click()
        time.sleep(1)
        element.clear()
        element.send_keys("voiture")
        time.sleep(1)
        button.click()
        time.sleep(1)
        self.assertIn("Aucun résultat", self.driver.page_source)

    # def test_Signup(self):
    #     self.click_on_link("login")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}accounts/login/"
    #     )
    #     self.click_on_link_text("Pas encore inscrit?")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}accounts/signup/"
    #     )
    #     self.write_user_text("email", self.email)
    #     self.write_user_text("password1", self.password1)
    #     self.write_user_text("password2", self.password2)
    #     self.click_on_button("submit_form")
    #     time.sleep(1)
    #     # errorlist = user already exists
    #     self.assertTrue(self.driver.find_element_by_class_name("errorlist"))

    # def test_Login_Logout(self):
    #     self.click_on_link("login")
    #     self.write_user_text("username", self.email)
    #     self.write_user_text("password", self.password1)
    #     self.click_on_button("validate")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}"
    #     )
    #     self.click_on_link("myprofile")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}accounts/profile/"
    #     )
    #     time.sleep(0.5)
    #     self.click_on_link("logout")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}"
    #     )

    # def test_search_top_nutella(self):
    #     element = self.driver.find_element_by_id("query_top")
    #     element.clear()
    #     element.send_keys("nutella")
    #     element.send_keys(Keys.RETURN)
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}search_product?query=nutella"
    #     )

    # def test_search_nutella(self):
    #     element = self.driver.find_element_by_id("query")
    #     element.clear()
    #     element.send_keys("nutella")
    #     element.send_keys(Keys.RETURN)
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}search_product?query=nutella"
    #     )

    # def test_search_pizza_key_enter(self):
    #     element = self.driver.find_element_by_id("query")
    #     element.clear()
    #     element.send_keys("pizza" + Keys.ENTER)
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}search_product?query=pizza"
    #     )

    # def test_select_product_and_save(self):
    #     self.driver.get(f"{self.URL}substitute?query=80762003")
    #     self.click_on_link_text("Se connecter")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}accounts/login/?next=/substitute?query=80762003"
    #     )
    #     self.write_user_text("username", self.email)
    #     self.write_user_text("password", self.password1)
    #     self.click_on_button("validate")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}substitute?query=80762003"
    #     )
    #     self.click_on_link_text("Sauvegarder")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}product_save?substitute=3111902100082"
    #     )

    def test_Profile(self):
        self.click_on_link("login")
        self.assertEqual(
            self.driver.current_url,
            f"{self.URL}accounts/login/"
        )
        self.write_user_text("username", self.email)
        self.write_user_text("password", self.password1)
        self.click_on_button("validate")
        self.assertEqual(
            self.driver.current_url,
            f"{self.URL}"
        )
        self.click_on_link("myprofile")
        self.assertEqual(
            self.driver.current_url,
            f"{self.URL}accounts/profile/"
        )
        time.sleep(1)

        # click edit avatar
        popup = self.driver.find_element_by_class_name("popup-container")
        element = self.driver.find_element_by_id("editAvatar")
        self.assertEqual(popup.value_of_css_property("display"), "none")
        element.click()

        # display popup
        self.assertEqual(popup.value_of_css_property("display"), "flex")
        time.sleep(1)

        close_popup = self.driver.find_element_by_class_name("popup-btn")
        close_popup.click()
        self.assertEqual(popup.value_of_css_property("display"), "none")

    # def test_myfood(self):
    #     self.click_on_link("login")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}accounts/login/"
    #     )
    #     self.write_user_text("username", self.email)
    #     self.write_user_text("password", self.password1)
    #     self.click_on_button("validate")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}"
    #     )
    #     self.click_on_link("myfood")
    #     self.assertEqual(
    #         self.driver.current_url,
    #         f"{self.URL}myfood"
    #     )


if __name__ == '__main__':
    unittest.main()
