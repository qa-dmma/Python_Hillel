class Human:

    def __init__(self, gender, age, first_name, last_name):
        self.gender = gender
        self.age = age
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'Gender: {self.gender}, Age: {self.age}, Name: {self.first_name}, Last Name: {self.last_name}'


class Student(Human):

    def __init__(self, gender, age, first_name, last_name, record_book):
        super().__init__(gender, age, first_name, last_name)
        self.record_book = record_book

    def __str__(self):
        return f'{super().__str__()}, Record: {self.record_book}'


class Group:

    def __init__(self, number):
        self.number = number
        self.group = set()

    def __str__(self):
        all_students = f'Number: {self.number}\n'
        for student in self.group:
            all_students += f'{student}\n'
        return all_students

    def _group_limit(self):
        if len(self.group) >= 10:
            raise UserException("Group is full")

    def add_student(self, student):
        self._group_limit()
        self.group.add(student)

    def delete_student(self, last_name):
        student = self.find_student(last_name)
        if student:
            self.group.remove(student)

    def find_student(self, last_name):
        for student in self.group:
            if student.last_name == last_name:
                return student
        return None


class UserException(Exception):
    pass


students_data = [
    ('Male', 30, 'Steve', 'Jobs', 'AN142'),
    ('Female', 25, 'Liza', 'Taylor', 'AN143'),
    ('Male', 22, 'John', 'Smith', 'AN144'),
    ('Female', 21, 'Anna', 'Brown', 'A145'),
    ('Male', 23, 'Mike', 'Johnson', 'AN146'),
    ('Female', 24, 'Sara', 'Wilson', 'AN147'),
    ('Male', 26, 'David', 'Lee', 'AN148'),
    ('Female', 20, 'Emma', 'White', 'AN149'),
    ('Male', 27, 'Chris', 'Green', 'AN150'),
    ('Female', 28, 'Olivia', 'Black', 'AN151'),
]

gr = Group('PD1')

for data in students_data:
    student_info = Student(*data)
    gr.add_student(student_info)

assert len(gr.group) == 10, 'Test1'

try:
    st1 = Student('Male', 35, 'Steven', 'Jobstic', 'AN152')
    gr.add_student(st1)
except UserException as e:
    print(f"Custom exception: {e}")

assert len(gr.group) == 10, 'Test2'
