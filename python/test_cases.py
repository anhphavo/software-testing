import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from testrail_api import TestRailAPI

# Thiết lập thông tin TestRail
TESTRAIL_URL = "https://testermstra24.testrail.io"
TESTRAIL_USERNAME = "Vo Anh Pha"
TESTRAIL_PASSWORD = "Apap@2407"
PROJECT_ID = 1
SUITE_ID = 1

# Kết nối TestRail API
testrail = TestRailAPI(TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_PASSWORD)

class TestDashboardApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://127.0.0.1:5500/trainning-anh-pha/account-dashboard-app/admin-dashboard/dash-board.html")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_add_account(self):
        driver = self.driver
        add_account_button = driver.find_element(By.ID, "button-add-account")
        add_account_button.click()

        account_data = {
            "accountName": "anhpha",
            "areaCode": "29",
            "email": "annphhaa@gmail.com",
            "firstName": "Phavovan",
            "lastName": "Anhpha",
            "password": "Ph123a@khong",
            "phoneNumber": "234301278",
            "subject": "Student",
        }

        driver.find_element(By.ID, "accountName").send_keys(account_data["accountName"])
        driver.find_element(By.ID, "areaCodeip").send_keys(account_data["areaCode"])
        driver.find_element(By.ID, "email").send_keys(account_data["email"])
        driver.find_element(By.ID, "firstName").send_keys(account_data["firstName"])
        driver.find_element(By.ID, "lastName").send_keys(account_data["lastName"])
        driver.find_element(By.ID, "password").send_keys(account_data["password"])
        driver.find_element(By.ID, "confirmPassword").send_keys(account_data["password"])
        driver.find_element(By.ID, "inputNumber").send_keys(account_data["phoneNumber"])
        driver.find_element(By.ID, "subject").send_keys(account_data["subject"])

        save_button = driver.find_element(By.ID, "registerButton")
        save_button.click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "confirmationMessage"))
            )
            confirmation_message = driver.find_element(By.ID, "confirmationMessage").text
            self.assertIn("Your account was created successfully!", confirmation_message, "Không nhận được thông báo tạo tài khoản thành công!")
            ok_button = driver.find_element(By.ID, "closeMessage")
            ok_button.click()
            print("Đã xác nhận thông báo tạo tài khoản thành công!")
            # Ghi kết quả kiểm thử lên TestRail
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC003", 1, "Test passed")
        except Exception as e:
            # Ghi kết quả kiểm thử lên TestRail
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC003", 5, f"Test failed: {str(e)}")
            self.fail(f"Không nhận được thông báo tạo tài khoản thành công! {str(e)}")

    def test_search(self):
        driver = self.driver
        search_box = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        search_box.send_keys("Quangminh")
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        if len(rows) <= 1:
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC001", 5, "Không tìm thấy kết quả phù hợp cho 'Quangminh'.")
            self.fail("Không tìm thấy kết quả phù hợp cho 'Quangminh'.")
        else:
            for row in rows[1:]:
                if "Quangminh" in row.text:
                    print("Tìm kiếm hoạt động chính xác. Kết quả hiển thị: Quangminh.")
                    testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC001", 1, "Test passed")
                    return
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC001", 5, "Tìm kiếm không chính xác. Quangminh không hiển thị trong kết quả.")
            self.fail("Tìm kiếm không chính xác. Quangminh không hiển thị trong kết quả.")

    def test_delete(self):
        driver = self.driver
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        user_found = False
        for row in rows:
            if "Firstname Lastname" in row.text:
                user_found = True
                delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-danger")
                delete_button.click()
                break

        if user_found:
            alert = driver.switch_to.alert
            self.assertIn("Are you sure that you want to delete the user \"Firstname Lastname\"?", alert.text, "Nội dung thông báo không đúng!")
            alert.accept()
            time.sleep(2)
            rows_after_delete = driver.find_elements(By.CSS_SELECTOR, "table tr")
            self.assertFalse(any("Firstname Lastname" in row.text for row in rows_after_delete), "Tài khoản Firstname Lastname chưa bị xóa!")
            print("Xóa tài khoản hoạt động chính xác.")
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC002", 1, "Test passed")
        else:
            testrail.add_result_for_case(testrail.get_run_id(PROJECT_ID, SUITE_ID), "TC002", 5, "Firstname Lastname không tồn tại trong danh sách.")
            print("Firstname Lastname không tồn tại trong danh sách.")

if __name__ == "__main__":
    unittest.main()
