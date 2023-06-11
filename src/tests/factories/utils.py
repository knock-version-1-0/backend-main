from datetime import datetime
import faker

fake = faker.Faker()

def get_unique_email():
    email = f'{fake.unique.first_name_male()}.{fake.unique.last_name()}@email.com'
    return email

timestamp = int(datetime.now().strftime('%s'))
emailCode = '000000'
