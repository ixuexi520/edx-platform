"""
Pages page for a course.
"""
from common.test.acceptance.pages.common.utils import click_css, confirm_prompt
from common.test.acceptance.pages.studio.course_page import CoursePage
from bok_choy.promise import EmptyPromise, Promise
from selenium.webdriver import ActionChains


class PagesPage(CoursePage):
    """
    Pages page for a course.
    """

    url_path = "tabs"

    def is_browser_on_page(self):
        return self.q(css='body.view-static-pages').present

    def is_static_page_present(self):
        """
        Checks for static tab's presence
        Returns: True or False
        """
        return self.q(css='.wrapper.wrapper-component-action-header').present

    def add_static_page(self):
        """
        Adds a static page
        """
        total_tabs = len(self.q(css='.course-nav-list>li'))
        click_css(self, '.add-pages .new-tab', require_notification=False)
        self.wait_for(
            lambda: len(self.q(css='.course-nav-list>li')) == total_tabs + 1,
            description="Static tab is added",
            timeout=3
        )
        self.wait_for_element_visibility('.tab-list :nth-child({})'.format(total_tabs), 'Static tab is visible')
        self.wait_for_ajax()

    def delete_static_tab(self):
        """
        Deletes a static page
        """
        click_css(self, '.btn-default.delete-button.action-button', require_notification=False)
        confirm_prompt(self)

    def click_edit_static_page(self):
        """
        Clicks on edit button to open up the xblock modal
        """
        # click_css(self, '.edit-button', require_notification=False)
        self.q(css='.edit-button').first.click()
        EmptyPromise(
            lambda: self.q(css='.xblock-studio_view').present,
            'Wait for the Studio editor to be present'
        ).fulfill()
        # self.wait_for_element_visibility('.edit-xblock-modal', 'Edit xblock modal visible')
        # self.wait_for_ajax()

    def drag_and_drop_first_static_page_to_last(self):
        """
        Drags and drops the first the static page to the last
        """
        draggable_elements = self.q(css='.component .drag-handle').results
        source_element = draggable_elements[0]
        target_element = draggable_elements[-1]
        action = ActionChains(self.browser)
        action.click_and_hold(source_element)
        action.move_to_element_with_offset(target_element, 0, 50)
        action.release().perform()
        self.wait_for_ajax()

    @property
    def static_tab_titles(self):
        """
        Gets the static tab title
        """
        #return self.q(css='.component-header').text
        apple = self.browser.execute_script("return $(.component-header).text();")
        return apple

    def open_settings_tab(self):
        self.q(css='.editor-modes .settings-button').first.click()
        self.wait_for_ajax()

    def set_field_val(self, field_display_name, field_value):
        """
        If editing, set the value of a field.
        """
        selector = '.xblock-studio_view li.field label:contains("{}") + input'.format(field_display_name)
        script = "$(arguments[0]).val(arguments[1]).change();"
        self.browser.execute_script(script, selector, field_value)

    def save(self):
        """
        Clicks save button.
        """
        click_css(self, '.action-save')

    def refresh_and_wait_for_load(self):
        """
        Refresh the page and wait for all resources to load.
        """
        self.browser.refresh()
        self.wait_for_page()
