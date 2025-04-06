from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


def fetch_ai_call(url: str, access_by: By, access_key: str, element_value=None, element_text=None) -> str:
    driver = webdriver.Chrome()
    driver.get(url=url)

    element = driver.find_element(access_by, access_key)
    
    # Set value of element
    if not element_value is None:
        driver.execute_script(f"arguments[0].value = {element_value}", element)

    # Set text of element
    if not element_text is None:
        driver.execute_script(f"arguments[0].innerText = {element_text}", element_text)

    element.send_keys(Keys.RETURN)

    # driver.close()  # Terminate 1 tab
    driver.quit()  # Terminate all tabs

def fetch_free_ChatGPT(access_by: By, access_key: str, element_value=None, element_text=None, timeout=10) -> str:
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (optional)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flag

    print(f"Finish preparing options")

    driver = webdriver.Chrome(options=options)
    print(f"Driver created")
    driver.get(url="https://chatgpt.com/")
    print(f"url got")

    # Wait until element appears
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))

    element = driver.find_element(access_by, access_key)
    
    # Set value of element
    if not element_value is None:
        driver.execute_script(f"arguments[0].value = {element_value}", element)

    # Set text of element
    if not element_text is None:
        # add_child_code = """
        # let parentDiv = arguments[0];
        # let newChild = document.createElement('p');
        # newChild.innerHTML = arguments[1];
        # parentDiv.appendChild(newChild);
        # """
        # driver.execute_script(add_child_code, element, element_text)
        action = ActionChains(driver)
        action.move_to_element(element).click().send_keys("your text here").perform()

        # Wait until element appears
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "composer-submit-button")))
        submit_element = driver.find_element(By.ID, "composer-submit-button")
        action.move_to_element(submit_element).click().perform()
        # element.send_keys(element_text)
    
    # time.sleep(5)
    # element.send_keys(Keys.RETURN)

    # ChatGPT stopped responding

    # id: composer-submit-button
    time.sleep(timeout)  # Wait for a period of time so that the server can reply

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-message-author-role='assistant']")))  # div

    response_element = driver.find_element(By.XPATH, "//*[@data-message-author-role='assistant']")
    print(f"response_element: {response_element.text}")

    content = response_element.get_attribute("innerHTML")

    # driver.close()  # Terminate 1 tab
    driver.quit()  # Terminate all tabs

    return content

if __name__ == "__main__":
    response = fetch_free_ChatGPT(access_by=By.ID, access_key="prompt-textarea", element_text="Please reply", timeout=20)

    print(f"reponse: {response}")
    print(f"Programme terminated ...")