from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_zillow_data():
    url = "https://www.zillow.com/research/"

    # Using Selenium to start a browser
    driver = webdriver.Chrome()  # Make sure you have the correct path to the ChromeDriver

    # Access the web page
    driver.get(url)

    # Wait for the element to be present before proceeding
    wait = WebDriverWait(driver, 20)  # Increased waiting time to 20 seconds
    element_present = EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'The Numbers')]"))
    wait.until(element_present)

    # Get the specified data
    typical_home_value = driver.find_element(By.XPATH,
                                             "//div[contains(text(), 'The Numbers')]/following-sibling::div").text
    change_in_home_value = driver.find_element(By.XPATH,
                                               "//div[contains(text(), 'Change in Typical Home Value')]/following-sibling::div").text
    typical_monthly_rent = driver.find_element(By.XPATH,
                                               "//div[contains(text(), 'Typical Monthly Rent')]/following-sibling::div").text
    change_in_rent = driver.find_element(By.XPATH,
                                         "//div[contains(text(), 'Change in Typical Rent')]/following-sibling::div").text

    # Close the browser
    driver.quit()

    # Print the results
    print("The Numbers JUNE 2023 U.S. Typical Home Value:", typical_home_value)
    print("JUNE 2023 Change in Typical Home Value From Last Month:", change_in_home_value)
    print("JUNE 2023 U.S. Typical Monthly Rent:", typical_monthly_rent)
    print("JUNE 2023 Change in Typical Rent From Last Year:", change_in_rent)


if __name__ == "__main__":
    get_zillow_data()
