from common.test.acceptance.pages.studio.utils import type_in_codemirror
from xblock_editor import XBlockEditorView
from common.test.acceptance.pages.common.utils import click_css


class HtmlXBlockEditorView(XBlockEditorView):
    """
    Represents the rendered view of an HTML component editor.
    """

    editor_mode_css = '.edit-xblock-modal .editor-modes .editor-button'
    settings_tab = '.editor-modes .settings-button'
    save_settings_button = '.action-save'

    def set_content_and_save(self, content, raw=False):
        """Types content into the html component and presses Save.

        Arguments:
            content (str): The content to be used.
            raw (bool): If true, edits in 'raw HTML' mode.
        """
        if raw:
            self.set_raw_content(content)
        else:
            self.set_content(content)

        self.save()

    def set_content_and_cancel(self, content, raw=False):
        """Types content into the html component and presses Cancel to abort.

        Arguments:
            content (str): The content to be used.
            raw (bool): If true, edits in 'raw HTML' mode.
        """
        if raw:
            self.set_raw_content(content)
        else:
            self.set_content(content)

        self.cancel()

    def set_content(self, content):
        """Sets content in the html component, leaving the component open.

        Arguments:
            content (str): The content to be used.
        """
        self.q(css=self.editor_mode_css).click()
        self.browser.execute_script("tinyMCE.activeEditor.setContent('%s')" % content)

    def set_raw_content(self, content):
        """Types content in raw html mode, leaving the component open.
        Arguments:
            content (str): The content to be used.
        """
        self.q(css=self.editor_mode_css).click()
        self.q(css='[aria-label="Edit HTML"]').click()
        self.wait_for_element_visibility('.mce-title', 'Wait for CodeMirror editor')
        # Set content in the CodeMirror editor.
        type_in_codemirror(self, 0, content)

        self.q(css='.mce-foot .mce-primary').click()

    def open_settings_tab(self):
        """
        Clicks settings button on the modal
        """
        self._click_button(self.settings_tab)

    def save_settings(self):
        self._click_button(self.save_settings_button)

    def open_link_plugin(self):
        self.q(css='[aria-label="Insert/edit link"]').click()

    def save_static_link(self, static_link):
        self.q(css='.mce-combobox .mce-textbox').fill(static_link)
        self.q(css='.mce-btn.mce-primary').click()

    def get_href(self):
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        return self.q(css="#tinymce>p>a").attrs('href')[0]

    def get_default_settings(self):
        display_name_setting = self.q(css='.wrapper-comp-setting input[type="text"]:nth-child(2)').attrs('value')[0]
        editor_setting = self.q(css='.wrapper-comp-setting .input.setting-input :nth-child(1)').text[0]
        return [display_name_setting, editor_setting]

    def get_keys(self):
        return self.q(css='.label.setting-label[for]').text

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
        click_css(self, '.save-button')

    def _click_button(self, button_name):
        """
        Click on a button as specified by `button_name`

        Arguments:
            button_name (str): button name

        """
        self.q(css=button_name).first.click()
        self.wait_for_ajax()

