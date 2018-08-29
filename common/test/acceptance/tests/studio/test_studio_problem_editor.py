"""
Acceptance tests for Problem component in studio
"""
from common.test.acceptance.tests.studio.base_studio_test import ContainerBase
from common.test.acceptance.fixtures.course import XBlockFixtureDesc
from common.test.acceptance.pages.studio.container import ContainerPage
from common.test.acceptance.pages.studio.utils import add_component
from common.test.acceptance.pages.studio.probelm_editor import ProblemXBlockEditorView


class ProblemComponentEditor(ContainerBase):
    """
    Feature: CMS.Component Adding
    As a course author, I want to be able to add and edit Problem
    """

    def setUp(self, is_staff=True):
        """
        Create a course with a section, subsection, and unit to which to add the component.
        """
        super(ProblemComponentEditor, self).setUp(is_staff=is_staff)
        self.component = 'Blank Common Problem'
        self.unit = self.go_to_unit_page()
        self.container_page = ContainerPage(self.browser, None)
        # Add Discussion component
        add_component(self.container_page, 'problem', self.component)
        self.component = self.unit.xblocks[1]
        self.container_page.edit()
        self.problem_editor = ProblemXBlockEditorView(self.browser, self.component.locator)

    def populate_course_fixture(self, course_fixture):
        """
        Adds a course fixture
        """
        course_fixture.add_children(
            XBlockFixtureDesc('chapter', 'Test Section').add_children(
                XBlockFixtureDesc('sequential', 'Test Subsection').add_children(
                    XBlockFixtureDesc('vertical', 'Test Unit')
                )
            )
        )

    def test_user_can_view_metadata(self):
        """
        Scenario: User can view metadata
        Given I have created a Blank Common Problem
        When I edit and select Settings
            Then I see the advanced settings and their expected values
            And Edit High Level Source is not visible
        """
        default_settings =[
            ('Display Name', 'Blank Common Problem'),
            ('Matlab API key', ''),
            ('Maximum Attempts', ''),
            ('Problem Weight', ''),
            ('Randomization', 'Never'),
            ('Show Reset Button', 'False'),
            ('Timer Between Attempts', '0')
        ]
        self.problem_editor.open_settings()
        settings = self.problem_editor.settings()
        self.assertEqual(settings, default_settings)
        self.assertFalse(self.problem_editor.is_latex_comiler_present())