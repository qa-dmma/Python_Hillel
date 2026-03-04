from . import utils


class Human:

    def __init__(self, last_name, first_name, fathers_name):
        self.first_name = first_name
        self.last_name = last_name
        self.fathers_name = fathers_name

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.fathers_name}'


class Person(Human):

    def __init__(self, last_name, first_name, fathers_name, birth_date, death_date, sex):
        super().__init__(last_name, first_name, fathers_name)
        self.birth_date = birth_date
        self.death_date = death_date
        self.sex = sex

    def __str__(self):
        return f'{super().__str__()} {self.birth_date} {self.death_date} {self.sex}'


class Record:
    def __init__(self):
        self.user = None
        self.users = []

    def __str__(self):
        result = ""
        for user in getattr(self, "users", []):
            result += "\n".join(f"{key}: {value}" for key, value in user.items())
            result += "\n\n"
        return result

    def add_person(self, birth_date, first_name, fathers_name='', last_name='', death_date=''):
        self.user = {}
        self._add_first_name(first_name)
        self._add_last_name(last_name)
        self._fathers_name(fathers_name)
        self._birth_date(birth_date)
        self._death_date(death_date)
        self._age()
        self._sex(first_name, fathers_name)
        self.users.append(self.user)

    def save_to_db(self, db_source):
        for user in self.users:
            d_date = str(user['Death_Date']) if user['Death_Date'] else ""

            db_source.insert_user(
                sex=user['Sex'],
                last_name=user['Last_Name'] or "",
                first_name=user['First_Name'],
                fathers_name=user['Fathers_Name'] or "",
                birth_date=user['Birth_Date'],
                death_date=d_date,
                age=user['Age']
            )
        self.users = []

    def _add_first_name(self, first_name):
        if len(first_name) >= 2:
            self.user['First_Name'] = first_name
            return first_name
        else:
            return f'First name should be 2 or more characters'

    def _add_last_name(self, last_name):
        self.user['Last_Name'] = last_name if last_name else ""
        return last_name

    def _fathers_name(self, fathers_name):
        self.user['Fathers_Name'] = fathers_name if fathers_name else ""
        return fathers_name

    def _sex(self, name, fathers_name):
        formatted = utils.gender_define(name, fathers_name)
        self.user['Sex'] = formatted
        return formatted

    def _birth_date(self, birth_date):
        formatted = utils.parse_date(birth_date)
        self.user['Birth_Date'] = formatted
        return formatted

    def _death_date(self, death_date):
        formatted = utils.parse_date(death_date)
        self.user['Death_Date'] = formatted
        return formatted

    def _age(self):
        formatted = utils.age_count(self.user.get('Birth_Date'), self.user.get('Death_Date'))
        self.user['Age'] = formatted
        return formatted
