from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options to run in headless mode (no UI)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Provide path to your WebDriver (Make sure the chromedriver is installed)
driver_path = "C:/Users/8858s/Downloads/chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# Function to login to LinkedIn
def linkedin_login(username, password):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    # Find the username and password input fields and log in
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Function to search for IIT graduates and scrape job-related data
def scrape_iit_grads_data():
    # Load the LinkedIn search page (you can customize this to search for IIT grads)
    driver.get("https://www.linkedin.com/search/results/people/?keywords=IIT%20graduate")
    
    # Wait for search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))

    # Scroll down the page to load more results (optional, you can customize the scroll logic)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    profiles = driver.find_elements(By.CLASS_NAME, "search-result__info")
    profile_data = []

    for profile in profiles:
        try:
            # Extract job titles, current companies, and industries
            job_title = profile.find_element(By.XPATH, ".//div[@class='actor-name']").text
            company_name = profile.find_element(By.XPATH, ".//p[@class='subline-level-1']").text
            industry = profile.find_element(By.XPATH, ".//p[@class='subline-level-2']").text

            profile_data.append({
                "Job Title": job_title,
                "Company": company_name,
                "Industry": industry
            })
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue
    
    return profile_data

# Function to write the data to a CSV file
def write_to_csv(data):
    with open('linkedin_iit_grads.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Job Title", "Company", "Industry"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print("Data written to linkedin_iit_grads.csv")

# Main function to run the script
def main():
    
    username = "your_email@example.com" #Use your own username
    password = "your_password" #Your own password

    try:
        linkedin_login(username, password)
        time.sleep(3)  # Wait for the login to complete

        # Scrape IIT graduate data
        data = scrape_iit_grads_data()
        write_to_csv(data)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()  # Close the browser once done

# Run the script
if __name__ == "__main__":
    main()
