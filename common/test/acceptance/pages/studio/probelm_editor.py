from xblock_editor import XBlockEditorView


class ProblemXBlockEditorView(XBlockEditorView):

    editor_mode_css = '.edit-xblock-modal .editor-modes .editor-button'
    settings_mode = '.settings-button'
    ordered_setting_values = ["Blank Common Problem", "", "", "", "Never", "Finished", "False", "0"]

    def open_settings(self):
        """
        Clicks on the settings button
        """
        self._click_button(self.settings_mode)

    def setting_keys(self):
        """
        Returns the list of all the keys
        """
        all_keys = self.q(css='.label.setting-label').text
        all_keys.pop()
        return all_keys

    def _click_button(self, button_name):
        """
        Click on a button as specified by `button_name`

        Arguments:
            button_name (str): button name

        """
        self.q(css=button_name).first.click()
        self.wait_for_ajax()

    def default_dropdown_values(self):
        dropdown_values = []
        elements = self.browser.find_elements_by_css_selector('.input.setting-input[name]')
        for dropdown in elements:
            value = dropdown.first_selected_option
            dropdown_values = dropdown_values.append(value)
            return dropdown_values

    def default_field_values(self):
        return self.q(css='.input.setting-input[value]').attrs('value')

    def ordered_setting_values(self):
        unordered_values = [self.default_field_values + self.default_dropdown_values]
        ordered_values = sorted(unordered_values, key=lambda x: self.ordered_setting_values.index(x))
        return ordered_values

    def settings(self):
        return zip(self.setting_keys(), self.ordered_setting_values())

    def is_latex_comiler_present(self):
        return self.q(css='.launch-latex-compiler').present
