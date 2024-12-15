from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_search(driver):
    search_box = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
    search_box.send_keys("Quangminh")
    search_box.send_keys(Keys.RETURN)

    # Chờ kết quả tìm kiếm hiển thị
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr"))
    )

    # Kiểm tra kết quả
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    if len(rows) <= 1:  # Nếu chỉ có tiêu đề bảng (hoặc không có hàng nào khác)
        print("Không tìm thấy kết quả phù hợp cho 'Quangminh'.")
    else:
        # Duyệt qua các hàng để kiểm tra kết quả tìm kiếm
        for row in rows[1:]:
            if "Quangminh" in row.text:
                print("Tìm kiếm hoạt động chính xác. Kết quả hiển thị: Quangminh.")
                return
        print("Tìm kiếm không chính xác. Quangminh không hiển thị trong kết quả.")



# def test_delete(driver):
#     # Tìm tài khoản "Quangmminh Nguyenn" trong bảng
#     rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
#     user_found = False
#     for row in rows:
#         if "Quangmminh Nguyenn" in row.text:
#             user_found = True
#             delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-danger")
#             delete_button.click()  # Nhấn nút xóa
#             break

#     if user_found:
#         alert = driver.switch_to.alert
#         assert "Are you sure that you want to delete the user \"Quangmminh Nguyenn\"?" in alert.text, "Nội dung thông báo không đúng!"
#         alert.accept()  # Nhấn "OK" để xác nhận xóa

#         # Chờ để cập nhật bảng
#         time.sleep(2)

#         # Kiểm tra xem "Quangmminh Nguyenn" đã bị xóa chưa
#         rows_after_delete = driver.find_elements(By.CSS_SELECTOR, "table tr")
#         assert not any("Quangmminh Nguyenn" in row.text for row in rows_after_delete), "Tài khoản Quangmminh Nguyenn chưa bị xóa!"
#         print("Xóa tài khoản hoạt động chính xác.")
#     else:
#         print("Quangmminh Nguyenn không tồn tại trong danh sách.")

def test_delete(driver):
    # Tìm tài khoản "Firstname Lastname" trong bảng
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    user_found = False
    for row in rows:
        if "Firstname Lastname" in row.text:
            user_found = True
            delete_button = row.find_element(By.CSS_SELECTOR, "button.btn-danger")
            delete_button.click()  # Nhấn nút xóa
            break

    if user_found:
        alert = driver.switch_to.alert
        assert "Are you sure that you want to delete the user \"Firstname Lastname\"?" in alert.text, "Nội dung thông báo không đúng!"
        alert.accept()  # Nhấn "OK" để xác nhận xóa

        # Chờ để cập nhật bảng
        time.sleep(2)

        # Kiểm tra xem "Firstname Lastname" đã bị xóa chưa
        rows_after_delete = driver.find_elements(By.CSS_SELECTOR, "table tr")
        assert not any("Firstname Lastname" in row.text for row in rows_after_delete), "Tài khoản Firstname Lastname chưa bị xóa!"
        print("Xóa tài khoản hoạt động chính xác.")
    else:
        print("Firstname Lastname không tồn tại trong danh sách.")

        
def test_add_account(driver):
    # Tìm và nhấn nút "Add Account" để mở form thêm tài khoản
    add_account_button = driver.find_element(By.ID, "button-add-account")
    add_account_button.click()

    # Nhập dữ liệu mẫu vào form
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

    # Nhấn nút "Save" để lưu tài khoản
    save_button = driver.find_element(By.ID, "registerButton")
    save_button.click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "confirmationMessage"))
        )
        confirmation_message = driver.find_element(By.ID, "confirmationMessage").text
        assert "Your account was created successfully!" in confirmation_message, "Không nhận được thông báo tạo tài khoản thành công!"
        # Nhấn OK trên confirmation message
        ok_button = driver.find_element(By.ID, "closeMessage")
        ok_button.click()
        print("Đã xác nhận thông báo tạo tài khoản thành công!")
    except:
        raise AssertionError("Không nhận được thông báo tạo tài khoản thành công!")


# Cập nhật lại phần main để chạy test_search trước
if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5500/trainning-anh-pha/account-dashboard-app/admin-dashboard/dash-board.html")

    print("Bắt đầu kiểm thử:")
    test_search(driver)
    test_delete(driver)
    test_add_account(driver)
    driver.quit()
    print("Tất cả kiểm thử đã hoàn thành.")

