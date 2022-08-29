from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() and char.islower() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre minuscule',
                code='password_no_letters')
        if not any(char.isalpha() and char.isupper() for char in password):
            raise ValidationError(
                'Le mot de passe doit contenir au moins une lettre majuscule',
                code='password_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir ' \
               'au moins une lettre majuscule et une lettre minuscule.'
