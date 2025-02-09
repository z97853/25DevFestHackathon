#!/usr/bin/env python3

# Required: pip install pyobjc-framework-Cocoa
import time
import webbrowser
import sys
import signal
from AppKit import (NSWorkspace, NSRunningApplication, NSApplication,
                NSApplicationActivateAllWindows, NSApplicationActivateIgnoringOtherApps)
import logging

def focus_browser():
    """Focus the browser window using AppKit."""
    try:
        # Get all running applications
        running_apps = NSWorkspace.sharedWorkspace().runningApplications()
        
        # Extended list of common browsers and their variants
        browsers = [
            'Safari', 'Google Chrome', 'Firefox', 'Chromium', 
            'Microsoft Edge', 'Opera', 'Brave Browser'
        ]
        
        for app in running_apps:
            app_name = app.localizedName()
            logging.debug(f"Checking application: {app_name}")
            
            if any(browser.lower() in app_name.lower() for browser in browsers):
                logging.info(f"Found browser: {app_name}")
                # Activate the browser window with proper options
                activation_options = NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
                success = app.activateWithOptions_(activation_options)
                
                if success:
                    logging.info(f"Successfully activated {app_name}")
                    return True
                else:
                    logging.warning(f"Failed to activate {app_name}")
            
        logging.warning("No supported browsers found running")
        return False
        
    except Exception as e:
        logging.error(f"Error focusing browser window: {str(e)}", exc_info=True)
        return False

def keep_tab_active(url, interval=30):
    """
    Keep a browser tab active by periodically bringing it to front.
    
    Args:
        url (str): The URL to keep active
        interval (int): Seconds between focus attempts
    """
    # Handle Ctrl+C gracefully
    def signal_handler(signum, frame):
        print("\nShutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        # Open the URL in the default browser
        logging.info(f"Opening URL: {url}")
        # webbrowser.open(url)
        time.sleep(2)  # Wait for browser to open

        print(f"Keeping tab active. Press Ctrl+C to stop.")
        while True:
            if focus_browser():
                logging.info("Successfully focused browser window")
            else:
                logging.warning("Failed to focus browser window - retrying in {interval} seconds")

            time.sleep(interval)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    keep_tab_active("https://chatgpt.com/", interval=2)

    # # OLD 1267357128903871265378921763213
    # # Handle Ctrl+C gracefully
    # def signal_handler(signum, frame):
    #     print("\nShutting down...")
    #     sys.exit(0)
    
    # signal.signal(signal.SIGINT, signal_handler)

    # # Configure logging
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s - %(levelname)s - %(message)s'
    # )

    # try:
    #     # Open the URL in the default browser
    #     # logging.info(f"Opening URL: {url}")
    #     # webbrowser.open(url)

    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #     driver.get(url)
    #     time.sleep(2)  # Wait for browser to open

    #     print(f"Keeping tab active. Press Ctrl+C to stop.")
    #     while True:
    #         print(driver.current_url)
    #         if focus_browser():
    #             logging.info("Successfully focused browser window")
    #         else:
    #             logging.warning("Failed to focus browser window - retrying in {interval} seconds")

    #         # if driver.current_url == url:
    #         #     print(driver.current_url)
    #         #     logging.info("Successfully focused tab")
    #         # else:
    #         #     logging.warning("Failed to focus tab")

    #         time.sleep(interval)

            
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     sys.exit(1)

        # Handle Ctrl+C gracefully
    # def signal_handler(signum, frame):
    #     print("\nShutting down...")
    #     if 'driver' in locals():
    #         driver.quit()
    #     sys.exit(0)
    
    # signal.signal(signal.SIGINT, signal_handler)

    # # Configure logging
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s - %(levelname)s - %(message)s'
    # )

    # try:
    #     # Set up Chrome options
    #     chrome_options = Options()
    #     chrome_options.add_argument('--start-maximized')
        
    #     # Initialize the driver
    #     driver = webdriver.Chrome(
    #         service=Service(ChromeDriverManager().install()),
    #         options=chrome_options
    #     )

    #     # Open the URL
    #     logging.info(f"Opening URL: {url}")
    #     driver.get(url)
        
    #     # Store the target tab handle
    #     target_tab = driver.current_window_handle

    #     def normalize_url(url):
    #         """Normalize URL for comparison"""
    #         return url.rstrip('/').replace('http://', '').replace('https://', '')

    #     def find_target_tab():
    #         """Find the tab containing our target URL, create it if not found"""
    #         target_url = normalize_url(url)
            
    #         try:
    #             # First check if current tab is target
    #             if normalize_url(driver.current_url) == target_url:
    #                 return driver.current_window_handle

    #             # Check all tabs
    #             for handle in driver.window_handles:
    #                 driver.switch_to.window(handle)
    #                 if normalize_url(driver.current_url) == target_url:
    #                     return handle

    #             # If not found, create new tab
    #             driver.switch_to.new_window('tab')
    #             driver.get(url)
    #             return driver.current_window_handle

    #         except WebDriverException as e:
    #             logging.error(f"Error finding target tab: {e}")
    #             return None

    #     print(f"Keeping tab active. Press Ctrl+C to stop.")
    #     last_switch_time = 0
    #     while True:
    #         try:
    #             current_time = time.time()
                
    #             # Find the target tab
    #             target_handle = find_target_tab()
                
    #             if target_handle:
    #                 # Only switch if we're not already on the target tab
    #                 if driver.current_window_handle != target_handle:
    #                     # Switch to target tab
    #                     driver.switch_to.window(target_handle)
    #                     logging.info("Switched back to target tab")
                    
    #                 # Ensure we're at the right URL
    #                 current_url = normalize_url(driver.current_url)
    #                 target_url = normalize_url(url)
                    
    #                 if current_url != target_url:
    #                     driver.get(url)
    #                     logging.info("Navigated back to target URL")
    #                 else:
    #                     logging.info("Target tab is active")
                    
    #             else:
    #                 # If target tab was lost somehow, recreate it
    #                 logging.warning("Target tab lost - creating new tab")
    #                 driver.switch_to.new_window('tab')
    #                 driver.get(url)
    #                 target_tab = driver.current_window_handle
                
    #             time.sleep(interval)

    #         except WebDriverException as e:
    #             logging.error(f"Browser error: {e}")
    #             # Try to recover by reopening the browser
    #             try:
    #                 driver.quit()
    #                 driver = webdriver.Chrome(
    #                     service=Service(ChromeDriverManager().install()),
    #                     options=chrome_options
    #                 )
    #                 driver.get(url)
    #                 target_tab = driver.current_window_handle
    #             except Exception as e:
    #                 logging.error(f"Failed to recover: {e}")
    #                 sys.exit(1)

    # except Exception as e:
    #     logging.error(f"An error occurred: {e}")
    #     if 'driver' in locals():
    #         driver.quit()
    #     sys.exit(1)
