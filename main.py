from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Function to initialize the driver (either Chrome or Edge)
def get_driver(use_chrome):
    if use_chrome:
        return webdriver.Chrome()
    else:
        return webdriver.Edge()

# List of IDs
url_ids = [
 890253005299351552, 890401381814870016, 890491475363938305, 890504639896072193
]

# Base URL template
base_url = "https://x.com/twitter/status/{}"

# Open the URL
urls = [base_url.format(url_id) for url_id in url_ids]

# Save the generated URLs to a text file
with open("generated_urls.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")

print("Generated URLs have been saved to generated_urls.txt")

# Start with Chrome
use_chrome = True
driver = get_driver(use_chrome)

# Initialize count for batch control
count = 0

# List to collect usernames
usernames = []  

# Loop through each URL to fetch the final redirected URL and extract data
for url in urls:
    count += 1
    try:
        # Every 50 URLs, switch browser (Chrome/Edge)
        if count > 50:
            count = 0
            time.sleep(20)  # Pause for 20 seconds after 50 URLs
            
            # Switch between Chrome and Edge after every batch of 50 URLs
            use_chrome = not use_chrome
            driver.quit()  # Close the previous browser session
            driver = get_driver(use_chrome)  # Reinitialize driver with the opposite browser

        print(f"Processing URL: {url}")

        # Open the URL
        driver.get(url)

        # Wait for the page to fully load using explicit wait
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Optionally, wait a few more seconds to handle redirects
        time.sleep(5)  # You can adjust this based on how long the redirect takes

        # Get the final URL after any redirects
        final_url = driver.current_url
        print("Final URL after redirect:", final_url)

        # Use regex to extract the username and status ID from the URL
        match = re.search(r'https?://x\.com/([^/]+)/status/(\d+)', final_url)
        if match:
            username = match.group(1)  # The username is captured in the first group
            usernames.append(username)  # Add the username to the list
        else:
            print("Username not found in the final URL.")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Save all usernames, each on a new line, to a file
with open("numbers.txt", "a") as output_file:  # Open in append mode
    output_file.write(f"[")
    for username in usernames:
        output_file.write(f"{username},")  # Write each username on a new line
    output_file.write(f"]")
# Close the browser at the end
driver.quit()

print("Processing complete. Usernames have been saved to final_results.txt")
