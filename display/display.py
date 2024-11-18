from selenium import webdriver
import time

def setup_driver():
    """Initialize and configure the Firefox webdriver"""
    service = webdriver.FirefoxService(executable_path="/snap/bin/geckodriver")
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    options.page_load_strategy = "none"
    return webdriver.Firefox(service=service, options=options)

def main():
    """Main function to display the local webpage"""
    driver = None
    try:
        driver = setup_driver()
        local_url = "http://127.0.0.1:5000/"
        
        # Open the local webpage
        driver.get(local_url)
        
        # Keep the browser window open
        while True:
            # Optional: Add a refresh every X seconds if needed
            time.sleep(300)  # Refresh every 5 minutes
            driver.refresh()
            
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
