from datetime import datetime

from fastapi import HTTPException, status


async def convert_date(date):
    try:
        today = datetime.today()
        years = today.year - date.year
        months = today.month - date.month
        # days = today.day - date.day

        # if days < 0:
        #     months -= 1
        #     days += (date.replace(month=date.month + 1, day=1) - date).days

        if months < 0:
            years -= 1
            months += 12

        age_str = []
        if years > 0:
            age_str.append(f"{years} year{'s' if years != 1 else ''}")
        if months > 0:
            age_str.append(f"{months} month{'s' if months != 1 else ''}")
        # if days > 0:
        #     age_str.append(f"{days} day{'s' if days != 1 else ''}")

        return ', '.join(age_str)
    except ValueError:
        return 'Invalid date format. Please use YYYY-MM-DD.'


async def validate_date(schema):

    current_date = datetime.now().date()
    try:
        if (current_date.year, current_date.month, current_date.day) < (
            int(schema.year),
            int(schema.month),
            int(schema.day),
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Date values incorrect',
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Date values incorrect',
        ) from e

    return f"{schema.year}-{schema.month}-{schema.day}"
