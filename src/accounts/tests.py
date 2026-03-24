from django.test import TestCase
from django.contrib.auth import get_user_model


class UserRoleModelTests(TestCase):
    def test_role_default_matches_field_default(self):
        """
        Ensure that a newly created user instance gets the default role
        defined on the model field.
        """
        User = get_user_model()
        role_field = User._meta.get_field("role")
        default_role = role_field.default

        user = User()

        self.assertEqual(
            getattr(user, "role"),
            default_role,
            "User.role should default to the field's configured default.",
        )

    def test_get_role_display_uses_choice_label(self):
        """
        Ensure that get_role_display returns the human-readable label
        from the role field's choices.
        """
        User = get_user_model()
        role_field = User._meta.get_field("role")

        # Only run this test meaningfully if choices are defined.
        self.assertTrue(
            role_field.choices,
            "Role field should define choices for get_role_display to use.",
        )

        # Take the first available choice for testing.
        choice_value, choice_label = role_field.choices[0]

        user = User()
        setattr(user, "role", choice_value)

        self.assertEqual(
            user.get_role_display(),
            choice_label,
            "get_role_display() should return the label for the current role value.",
        )
