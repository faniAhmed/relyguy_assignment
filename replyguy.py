import toml
from playwright.sync_api import sync_playwright, ViewportSize

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()

        page.goto("https://www.reddit.com/login", timeout=0)
        page.set_viewport_size(ViewportSize(width=1920, height=1080))
        page.wait_for_load_state()
        page.wait_for_timeout(5000)  # Adjusted timeout for waiting


        # Wait for the username field to be ready and fill it in
        page.wait_for_selector("input#login-username")
        page.locator("input#login-username").fill(
            config["reddit"]["creds"]["username"]
        )


        # Wait for the password field to be ready and fill it in
        page.wait_for_selector("input#login-password")
        page.locator("input#login-password").fill(
            config["reddit"]["creds"]["password"]
        )


        # Click the login button using the updated selector based on the provided HTML structure
        login_button_selector = "button.login:has-text('Log In')"
        page.wait_for_selector(login_button_selector)
        page.click(login_button_selector)


        page.wait_for_timeout(5000)


        login_error_div = page.locator(".AnimatedForm__errorMessage").first
        if login_error_div.is_visible():
            login_error_message = login_error_div.inner_text()
            if login_error_message.strip() == "":
                # The div element is empty, no error
                pass
            else:
                # The div contains an error message
                print("Your reddit credentials are incorrect! Please modify them accordingly in the config.toml file.")
                exit()
        else:
            pass


        page.wait_for_load_state()
        # Get the thread screenshot
        reddit_object = config['reddit']
        page.goto(reddit_object["thread_url"], timeout=0)
        page.wait_for_load_state()
        page.wait_for_timeout(5000)

        comment_selector = "//*[@noun='add_comment_button']"
        page.wait_for_selector(comment_selector)
        page.click(comment_selector)
        comment_selector = "//comment-composer-host//p"
        page.locator(comment_selector).fill(
            "Hello"
        )
        page.click("//button[@rpl and @type='submit']")
        print("Comment Posted.")


if __name__ == '__main__':
    with open('settings.toml', 'r') as f:
        config = toml.load(f)
    main()
