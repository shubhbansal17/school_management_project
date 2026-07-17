import json
from  abc import ABC,abstractmethod
from pathlib import  Path

database= "school_data.json"
data = {'students' : [] , 'teachers' : []}


if Path(database).exists():
    with open(database,'r') as f:
        content=f.read()
        if content:
            data = json.loads(content)
def save():
    with open(database,'w') as f:
        json.dump(data,f,indent=4)

class Persons(ABC):

    @abstractmethod
    def get_roles(self):
        pass

    @abstractmethod
    def register(self):
        pass
    @abstractmethod
    def show_details(self):
        pass
    @staticmethod
    def email_validation(email):
        if  "@" in email and "." in email:
            return True
        else:
            return 'mail is wrong'


class Student(Persons):
    def get_roles(self):
        return 'student'
    
    def register(self):
        name=input('enter your name')
        age=int(input('tell your age'))
        email=input('tell your mail')
        rno=int(input('enter your roll no'))

        if not Persons.email_validation(email):
            print('invalid email')
            return
        for s in data['students']:
            if s['rno'] ==rno:
                print('student already exist')
                return
        data['students'].append({
            'name':name ,
             'age':age,
             'email' :email,
             'rno': rno,
             'grades': {}})
        
        save()
    def show_details(self):
        roll_no = int(input('Enter roll no: '))

        for s in data['students']:
            if s['rno'] == roll_no:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\n  Name    : {s['name']}")
                print(f"  Roll no : {s['rno']}")
                print(f"  Grades  : {grades}")
                print(f"  Average : {avg:.1f}")
                return

        print("Student not found")
    def add_grad(self):
        roll_no=int(input('tell the rno'))
        subject=input('enter subject')
        marks=float(input('enter marks'))
        for i in data['students']:
            if i['rno']==roll_no:
                i['grades'][subject]=marks
                save()
                print('grade added')
                return

class Teachers(Persons):
    def get_roles(self):
        return 'teachers'
    
    def register(self):
        name=input('enter your name')
        age=int(input('tell your age'))
        email=input('tell your mail')
        
        emp_id=int(input('enter your employee no'))
        subject=input('enter your subject')

        if not Persons.email_validation(email):
            print('invalid email')
            return
        for s in data['teachers']:
            if s['emp_id'] ==emp_id:
                print('teacher already exist')
                return
        data['teachers'].append({
            'name':name ,
             'age':age,
             'email' :email,
             'emp_id': emp_id,
             'subject': subject})
        
        save()
    def show_details(self):
            print(data['teachers'])  # Debug

        

            emp_id=int(input('enter employ no'))
            for s in data['teachers']:
                if s['emp_id'] == emp_id:
                    print(f"\n  Name    : {s['name']}")
                    print(f"  Emp ID  : {s['emp_id']}")
                    print(f"  Subject : {s['subject']}")
                    print(f"  Email   : {s['email']}")
                    print(f"  Age     : {s['age']}")

        


print('press1 for registering a student \n press2 for registering a teacher \n press3 to add grades \n press4 to show details of student \n press5 to show a teacher detail ')
choice=int(input('please tell your choice'))
stud=Student()
teach=Teachers()
if choice == 1:
    stud.register()
    
elif choice == 2:
    teach.register()
elif choice == 3:
    stud.add_grad()

elif choice ==4:
    stud.show_details()
elif choice == 5:
    teach.show_details()
