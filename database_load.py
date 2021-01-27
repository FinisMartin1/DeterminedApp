from random import randint, triangular, choice, random
from passlib.hash import pbkdf2_sha256
from datetime import datetime
import argparse
import sqlite3
import names
import json

def main():
    """Fills the database with courses and random values for student_work_products

    This should only be used on a empty database, re-running it will cause duplicates.
    SQL insert statements are commented out for that reason.
    """

    #Courses
    years = [2016, 2017, 2018, 2019, 2020]
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE "course" (
            "course_number"	int NOT NULL,
            "dept_id"	varchar(4) NOT NULL,
            "title"	varchar(100) NOT NULL,
            "instructor_fname"	varchar(35) DEFAULT NULL,
            "instructor_lname"	varchar(35) DEFAULT NULL,
            "student_work_products"	json DEFAULT NULL,
            `term` varchar(7) NOT NULL,
            `year` int NOT NULL,
            PRIMARY KEY("course_number", "term", "year")) 
            """
        )
        conn.commit()
    courses = [
        (1370, "CPSC", "Computer Literacy", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (1375, "CPSC", "Programming I", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2376, "CPSC", "Intro to Game Programming", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2380, "CPSC", "Algorithms", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2482, "CPSC", "Computer Organization", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3377, "CPSC", "Advanced Game Programming", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3380, "CPSC", "Operating Systems", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3383, "CPSC", "Programming Languages", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3384, "CPSC", "Computer Networks", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer"),
        (4360, "CPSC", "Computer Security", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer")
    ]
    #Adding years
    upload_courses = []
    for year in years:
        upload_courses += [x + (year,) for x in courses]
    #Making a few instructors teach multiple course
    new_courses = [
        (4557, "CPSC", "Natural Language Processing", ),
        (2375, "CPSC", "Programming II",),
        (2776, "CPSC", "Data Structures and Algorithms",),
        (4862, "CPSC", "Image Recognition", ),
    ]
    for i in range(0,len(new_courses)):
        year = choice(years)
        for y in range(0,2): #Number of  times new course is taught
            c = upload_courses[i]
            new_data = (c[3], c[4], c[5], choice(["Fall", "Spring", "Summer"]), year+y)
            data = new_courses[i] + new_data
            upload_courses.append(data)
    #Adding solo instructors and solo courses
    upload_courses += [
        (4672, "CPSC", "Programming Memes", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring", choice(years)),
        (1872, "CPSC", "Information Systems", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer", choice(years)),
        (1123, "CPSC", "Microsoft Office", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall", choice(years))
        ]

    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.executemany('''INSERT INTO course (course_number, dept_id, title, instructor_fname, instructor_lname, student_work_products, term, year)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', upload_courses)
        conn.commit()

    #SWP
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE `student_work_product` (
            `id` INTEGER PRIMARY KEY,
            `product` varchar(250) NOT NULL,
            `course_id` int NOT NULL,
            `dept_id` int NOT NULL,
            `student_fname` varchar(35) NOT NULL,
            `student_lname` varchar(35) NOT NULL,
            `student_outcome` int DEFAULT NULL,
            `score` int DEFAULT NULL,
            `term` varchar(7) NOT NULL,
            `year` int NOT NULL,
            CONSTRAINT `course` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_number`)
            CONSTRAINT `course` FOREIGN KEY (`dept_id`) REFERENCES `course` (`dept_id`)
            )
            """
        )
        conn.commit()
   
    swps = []
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("Select * from course")
        records = [dict(x) for x in c.fetchall()]
        #Generating 20 student records for each swp in each course
        for i, course in enumerate(records):
            student_names = []
            for _ in range(20):
                student_names.append({'fname': names.get_first_name(),
                                        'lname': names.get_last_name()})
            for product in json.loads(course['student_work_products'])['swp']:
                for student in student_names:
                    if i%7 == 0:
                        score = int(triangular(50, 85))
                    else:
                        score = int(triangular(50, 100))
                    if score >= 90: outcome = 4
                    elif score >= 80: outcome = 3
                    elif score >= 70: outcome = 2
                    elif score >= 60: outcome = 1
                    else: outcome = 0 
                    swps.append((
                        product,
                        course['course_number'],
                        "CPSC",
                        student['fname'],
                        student['lname'],
                        outcome,
                        score, 
                        course['term'], 
                        course['year']
                    ))
        
        c.executemany('''INSERT INTO student_work_product (product, course_id, dept_id, student_fname, student_lname, student_outcome, score, term, year)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', swps)
        conn.commit()

def generate_users():
    num_users = 10
    users = []
    for i in range(0,num_users):
        fname = names.get_first_name()
        lname = names.get_last_name()
        access_level = choice(['Administrator', 'Instructor'])
        is_admin = '0' if access_level=='Instructor' else '1'
        password = pbkdf2_sha256.hash(fname + lname + "Password1")
        data_joined = datetime.now()
        u = (fname + f"{i}@example.com",fname,lname,access_level,password,
            is_admin,'0',fname + " " + lname, data_joined, data_joined)
        users.append(u)
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.executemany('''INSERT INTO users_user 
            (email, first_name, last_name, access_level, password, is_admin,
                is_active, name, data_joined, last_login)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?,?, ?)''', users)
        conn.commit()

def database_refresh():
     #Courses
    years = [2016, 2017, 2018, 2019, 2020]
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM student_work_product;""")
        conn.commit()
        c.execute("""DELETE FROM course;""")
        conn.commit()

    courses = [
        (1370, "CPSC", "Computer Literacy", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (1375, "CPSC", "Programming I", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2376, "CPSC", "Intro to Game Programming", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2380, "CPSC", "Algorithms", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall"),
        (2482, "CPSC", "Computer Organization", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3377, "CPSC", "Advanced Game Programming", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3380, "CPSC", "Operating Systems", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3383, "CPSC", "Programming Languages", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring"),
        (3384, "CPSC", "Computer Networks", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer"),
        (4360, "CPSC", "Computer Security", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer")
    ]
    #Adding years
    upload_courses = []
    for year in years:
        upload_courses += [x + (year,) for x in courses]
    #Making a few instructors teach multiple course
    new_courses = [
        (4557, "CPSC", "Natural Language Processing", ),
        (2375, "CPSC", "Programming II",),
        (2776, "CPSC", "Data Structures and Algorithms",),
        (4862, "CPSC", "Image Recognition", ),
    ]
    for i in range(0,len(new_courses)):
        year = choice(years)
        for y in range(0,2): #Number of  times new course is taught
            c = upload_courses[i]
            new_data = (c[3], c[4], c[5], choice(["Fall", "Spring", "Summer"]), year+y)
            data = new_courses[i] + new_data
            upload_courses.append(data)
    #Adding solo instructors and solo courses
    upload_courses += [
        (4672, "CPSC", "Programming Memes", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Spring", choice(years)),
        (1872, "CPSC", "Information Systems", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Summer", choice(years)),
        (1123, "CPSC", "Microsoft Office", names.get_first_name(), names.get_last_name(), json.dumps({"swp": ["Midterm", "Final Exam", "Project 1"]}), "Fall", choice(years))
        ]

    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.executemany('''INSERT INTO course (course_number, dept_id, title, instructor_fname, instructor_lname, student_work_products, term, year)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)''', upload_courses)
        conn.commit()

    #SWP
    swps = []
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("Select * from course")
        records = [dict(x) for x in c.fetchall()]
        #Generating 20 student records for each swp in each course
        for i, course in enumerate(records):
            student_names = []
            for _ in range(20):
                student_names.append({'fname': names.get_first_name(),
                                        'lname': names.get_last_name()})
            for product in json.loads(course['student_work_products'])['swp']:
                for student in student_names:
                    if i%7 == 0:
                        score = int(triangular(50, 85))
                    else:
                        score = int(triangular(50, 100))
                    if score >= 90: outcome = 4
                    elif score >= 80: outcome = 3
                    elif score >= 70: outcome = 2
                    elif score >= 60: outcome = 1
                    else: outcome = 0 
                    swps.append((
                        product,
                        course['course_number'],
                        "CPSC",
                        student['fname'],
                        student['lname'],
                        outcome,
                        score, 
                        course['term'], 
                        course['year']
                    ))
        
        c.executemany('''INSERT INTO student_work_product (product, course_id, dept_id, student_fname, student_lname, student_outcome, score, term, year)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)''', swps)
        conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill database with example data")
    parser.add_argument('-m', '--mode', help="create to create tables, refresh to refresh data", required=True)
    args = vars(parser.parse_args())
    if args['mode'].lower() == 'create':
        main()
        generate_users()
        print("Finished!")
    elif args['mode'].lower() == 'refresh':
        database_refresh()
        print("Data Tables Refreshed!")
    else:
        print("No valid argument given")
    
