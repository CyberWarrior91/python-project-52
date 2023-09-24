from django.core.exceptions import ValidationError


class ObjectFormTest():
    form = None
    correct_data = None
    wrong_data = None

    def test_form_valid(self):
        form = self.form(data=self.correct_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form = self.form(data=self.wrong_data)
        self.assertFalse(form.is_valid())
