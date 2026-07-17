import json
from abc import ABC, abstractmethod
from pathlib import Path

import streamlit as st

database = "school_data.json"

st.set_page_config(page_title="School Management", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

    .stApp {
        background: linear-gradient(160deg, #101418 0%, #1a1f26 100%);
        color: #eaeaea;
    }
    h1, h2, h3 { color: #f2c14e; font-weight: 600; }
    section[data-testid="stSidebar"] {
        background-color: #14181d;
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1c2229;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 6px;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #20262e !important;
        color: #eaeaea !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #f2c14e, #d99f2b);
        color: #1a1305;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.5em 1.3em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "data" not in st.session_state:
    if Path(database).exists():
        with open(database, 'r') as f:
            content = f.read()
            if content:
                st.session_state.data = json.loads(content)
            else:
                st.session_state.data = {'students': [], 'teachers': []}
    else:
        st.session_state.data = {'students': [], 'teachers': []}

data = st.session_state.data


def save():
    with open(database, 'w') as f:
        json.dump(data, f, indent=4)


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
        if "@" in email and "." in email:
            return True
        else:
            return 'mail is wrong'


class Student(Persons):
    def get_roles(self):
        return 'student'

    def register(self):
        st.subheader("Register Student")
        with st.form("student_register_form"):
            name = st.text_input('enter your name')
            age = st.number_input('tell your age', step=1, format="%d")
            email = st.text_input('tell your mail')
            rno = st.number_input('enter your roll no', step=1, format="%d")
            submitted = st.form_submit_button("Submit")

        if submitted:
            age = int(age)
            rno = int(rno)

            if not Persons.email_validation(email):
                st.write('invalid email')
                return

            for s in data['students']:
                if s['rno'] == rno:
                    st.write('student already exist')
                    return

            data['students'].append({
                'name': name,
                'age': age,
                'email': email,
                'rno': rno,
                'grades': {}})

            save()
            st.success("Student registered.")

    def show_details(self):
        st.subheader("Show Student Details")
        roll_no = st.number_input('Enter roll no: ', step=1, format="%d", key="show_stud_rno")

        if st.button("Show"):
            roll_no = int(roll_no)
            found = False
            for s in data['students']:
                if s['rno'] == roll_no:
                    found = True
                    grades = s['grades']
                    avg = sum(grades.values()) / len(grades) if grades else 0

                    st.write(f"\n  Name    : {s['name']}")
                    st.write(f"  Roll no : {s['rno']}")
                    st.write(f"  Grades  : {grades}")
                    st.write(f"  Average : {avg:.1f}")
                    break

            if not found:
                st.write("Student not found")

    def add_grad(self):
        st.subheader("Add Grade")
        roll_no = st.number_input('tell the rno', step=1, format="%d", key="grade_rno")
        subject = st.text_input('enter subject')
        marks = st.number_input('enter marks', format="%f")

        if st.button("Add Grade"):
            roll_no = int(roll_no)
            for i in data['students']:
                if i['rno'] == roll_no:
                    i['grades'][subject] = marks
                    save()
                    st.write('grade added')
                    return


class Teachers(Persons):
    def get_roles(self):
        return 'teachers'

    def register(self):
        st.subheader("Register Teacher")
        with st.form("teacher_register_form"):
            name = st.text_input('enter your name')
            age = st.number_input('tell your age', step=1, format="%d")
            email = st.text_input('tell your mail')
            emp_id = st.number_input('enter your employee no', step=1, format="%d")
            subject = st.text_input('enter your subject')
            submitted = st.form_submit_button("Submit")

        if submitted:
            age = int(age)
            emp_id = int(emp_id)

            if not Persons.email_validation(email):
                st.write('invalid email')
                return

            for s in data['teachers']:
                if s['emp_id'] == emp_id:
                    st.write('teacher already exist')
                    return

            data['teachers'].append({
                'name': name,
                'age': age,
                'email': email,
                'emp_id': emp_id,
                'subject': subject})

            save()
            st.success("Teacher registered.")

    def show_details(self):
        st.subheader("Show Teacher Details")
        st.write(data['teachers'])  # Debug

        emp_id = st.number_input('enter employ no', step=1, format="%d", key="show_teach_id")

        if st.button("Show"):
            emp_id = int(emp_id)
            for s in data['teachers']:
                if s['emp_id'] == emp_id:
                    st.write(f"\n  Name    : {s['name']}")
                    st.write(f"  Emp ID  : {s['emp_id']}")
                    st.write(f"  Subject : {s['subject']}")
                    st.write(f"  Email   : {s['email']}")
                    st.write(f"  Age     : {s['age']}")


st.title("🎓 School Management System")

st.write('press1 for registering a student  \n press2 for registering a teacher  \n press3 to add grades  \n press4 to show details of student  \n press5 to show a teacher detail')

with st.sidebar:
    st.header("Menu")
    choice = st.radio(
        "please tell your choice",
        [1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "1 - Register Student",
            2: "2 - Register Teacher",
            3: "3 - Add Grades",
            4: "4 - Show Student Details",
            5: "5 - Show Teacher Details",
        }[x],
    )

stud = Student()
teach = Teachers()

if choice == 1:
    stud.register()
elif choice == 2:
    teach.register()
elif choice == 3:
    stud.add_grad()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    teach.show_details()