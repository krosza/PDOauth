#pylint: disable=unused-argument, invalid-name
from wtforms import validators
from flask.globals import session
from wtforms.validators import ValidationError

def csrfCheck(self, field):
    if not session.has_key('csrf_token'):
        raise ValidationError('csrf validation error')
    sessionid = session['csrf_token']
    if not sessionid == field.data:
        raise ValidationError('csrf validation error')

def optional(validator):
    return [validators.Optional()] + validator
credentialTypes = ['password', 'facebook', 'certificate']
credErr = '"credentialType: Invalid value, must be one of: {0}."'.format(", ".join(credentialTypes))

credentialValidator = [validators.AnyOf(values=credentialTypes)]
userNameValidator = [validators.Length(min=4, max=250)]
passwordValidator = [validators.Length(min=8),
                     validators.Regexp(".*[a-z].*", message="password should contain lowercase"),
                     validators.Regexp(".*[A-Z].*", message="password should contain uppercase"),
                     validators.Regexp(".*[0-9].*", message="password should contain digit")]
secretValidator = [validators.Length(min=8),
                     validators.Regexp(".*[a-z].*", message="password should contain lowercase"),
                     validators.Regexp(".*[0-9].*", message="password should contain digit")]
emailValidator = [validators.Email()]
digestValidator = [validators.Length(min=128, max=128), validators.regexp("[0-9A-Fa-f]*")]
assuranceValidator = [validators.Length(min=4, max=50)]
csrfValidator = [csrfCheck]
