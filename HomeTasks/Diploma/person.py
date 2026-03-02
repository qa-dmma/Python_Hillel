import utils


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
        self.users = []
        self._id_counter = 0

    def __str__(self):
        result = ""
        for user in getattr(self, "users", []):
            result += "\n".join(f"{key}: {value}" for key, value in user.items())
            result += "\n\n"
        return result

    def add_person(self, birth_date, first_name, fathers_name='', last_name='', death_date=''):
        self.user = {}
        self._id()
        self._add_first_name(first_name)
        self._add_last_name(last_name)
        self._fathers_name(fathers_name)
        self._birth_date(birth_date)
        self._death_date(death_date)
        self._age()
        self._sex(first_name, fathers_name)
        self.users.append(self.user)

    def _add_first_name(self, first_name):
        if len(first_name) >= 2:
            self.user['First_Name'] = first_name
            return first_name
        else:
            return f'First name should be 2 or more characters'

    def _add_last_name(self, last_name):
        self.user['Last_Name'] = last_name
        return last_name

    def _fathers_name(self, fathers_name):
        self.user['Fathers_Name'] = fathers_name
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

    def _id(self):
        if not hasattr(self, "users"):
            self.users = []

        if not self.users:
            new_id = 1
        else:
            last_id = max(user['Id'] for user in self.users)
            new_id = last_id + 1

        self.user['Id'] = new_id
        return new_id


rec = Record()
rec.add_person("22.03.1992", "Дмитро","Батькович", "Призвищенко" )
rec.add_person("20.03.1990", "Микола", "", "")
rec.add_person("11 10 2000", "Іванка", "", "","02 10 2010")
rec.add_person("12.10.1980", "Євген", "Михайлович", "Крут","11.10.2001")
rec.add_person("01/02/1995", "Євгенія", "", "","12 10 2001")
rec.add_person("3-9-2007", "Дмитро", "Євгенович", "","02 10 2010")
print(rec)
