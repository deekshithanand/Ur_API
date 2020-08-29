from wtforms import Form, fields, validators


pwd_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"


class UserSignup(Form):
    email_id = fields.StringField('Email',
                                  [validators.email('Email invalid'), validators.DataRequired(
                                      'Email Required')]

                                  )

    password = fields.PasswordField('Password',
                                    [validators.Regexp(pwd_regex,
                                                       message="Password invalid"
                                                       ), validators.DataRequired('Passowrd Required')]
                                    )

    confirm_password = fields.PasswordField(
        'Confirm Password',
        [validators.EqualTo('password',
                            message='password must match'
                            ), validators.DataRequired('Please Confirm your password!')]
    )


class UserLogin(Form):
    email_id = fields.StringField(
        'Email',
        [validators.Email(
            'Invalid email'
        ), validators.DataRequired("Email required")]
    )

    password = fields.PasswordField(
        'Password',
        [validators.DataRequired("Password Required")]
    )
