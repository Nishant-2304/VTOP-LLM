from playwright.sync_api import sync_playwright 
from blocks.login import login
from blocks.navigation.router import navigate
from blocks.assignments.router import fetch_assignment_details
from blocks.marks.router import display_marks

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Run login
        login(page)
        print("Login successful!")
        # Navigate to a specific page: Academics -> Digital Assignment Upload
        print("Navigating to Academics -> Digital Assignment Upload...")
        navigate(page, "academics", "digital_assignment_upload")
        print("Navigation successful!")
        # Fetch assignment details
        print("Fetching assignment details...")  
        fetch_assignment_details(page)
        print("Assignment details fetched successfully!") # Need to change these to reflect path where details are saved
        #Fetch marks
        print("Fetching Marks...")
        display_marks(page)
        print("Marks fetched successfully!")
        
        context.close()
        browser.close()