def get_text_contains(browser, text):
    return browser.find_elements_by_xpath(f"//*[text()[contains(.,'{text}')]]")
