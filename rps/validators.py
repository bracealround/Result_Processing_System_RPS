from django.core.exceptions import ValidationError
from datetime import date


def validate_session(session):
    print("ffff")
    year = int(session[:4])
    print(year)
    last_two_digits = int(session[-2:])
    print(last_two_digits)
    if year < 2000 or year > 2099:
        raise ValidationError(
            "%(session) has to be with the range between 2000 and 2099",
            params={"session": session},
        )

    year = year - 2000

    if year - last_two_digits != 1:
        raise ValidationError(
            "%(session) is not of valid format",
            params={"session": session},
        )


def validate_registration_no(registration_no):
    pass
