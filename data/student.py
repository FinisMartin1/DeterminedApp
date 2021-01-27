from collections import OrderedDict
import sqlite3
import json



def swp_dropdowns(dept, course, term, swp):
    if not course.isdigit():
        course = course.split()[0]
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #Dept Id
        c.execute("SELECT DISTINCT(dept_id) from course")
        dept_ids = [x['dept_id'] for x in c.fetchall()]
        #Courses
        if dept == 'All':
            c.execute("SELECT course_number, title from course order by title",)
        else:
            c.execute("SELECT course_number, title from course where dept_id=? order by title", (dept,))
        courses = list(set([f"{r['course_number']} {r['title']}" for r in c.fetchall()]))
        courses.sort()
        #Terms
        if dept == 'All' and course=="All":
            c.execute('''SELECT term, year from course group by term, year order by year desc,  
                case when term="Spring" then 0 
                when term="Summer" then 1 
                when term="Fall" then 2 end;''')
        elif dept=="All" and course != "All":
            c.execute('''SELECT term, year from course where course_number=? group by term, year
            order by year desc, case when term="Spring" then 0 
            when term="Summer" then 1 when term="Fall" then 2 end;''', (course,))
        elif course=="All" and dept != "All":
            c.execute('''SELECT term, year from course where dept_id=? group by term, year
            order by year desc, case when term="Spring" then 0 
            when term="Summer" then 1 when term="Fall" then 2 end;''', (dept,))
        else:
            c.execute('''SELECT term, year from course where course_number=? and dept_id=? 
                group by term, year
                order by year desc, case when term="Spring" then 0 
                when term="Summer" then 1 when term="Fall" then 2 end;''', (course,dept))
        records = c.fetchall()
        if records:
            terms =[f"{r['term']} {r['year']}" for r in records]
        else:
            course = int(courses[0][:4])
            c.execute('''SELECT term, year from course where course_number=? group by term, year
                order by year desc, case when term="Spring" then 0 
                when term="Summer" then 1 when term="Fall" then 2 end;''', (course))
            terms = [f"{r['term']} {r['year']}" for r in c.fetchall()]
        term = term if term in terms else terms[0]
        semester, year = term.split()[0], term.split()[1]
        #SWP
        swp = set()
        if course == 'All' or term== "All":
            if course == "All" and term == "All":
                c.execute("SELECT student_work_products from course")
            elif course == "All":
                c.execute("SELECT student_work_products from course where term=? and year=?",
                    (semester, year))
            elif term == "All":
                c.execute("SELECT student_work_products from course where course_number=?",
                    (course,))
            records = c.fetchall()
            for r in records:
                swps = json.loads(r['student_work_products'])['swp']
                for p in swps: swp.add(p)
        else:
            c.execute("SELECT student_work_products from course where course_number=? and term=? and year=?",
                (course, semester, year))
            record = c.fetchone()
            swp = json.loads(record['student_work_products'])['swp']
    return {'dept_ids': dept_ids, "courses": courses, "terms":terms, 'swp':swp}

def swp_redirect(dept, course, term, swp, dropdowns):
    if (term in dropdowns['terms'] or term == "All") and \
        (course in dropdowns["courses"] or course == 'All') and \
        (swp in dropdowns['swp'] or swp=="All"):
        return None
    if term not in dropdowns['terms'] and term != "All":
        term = dropdowns["terms"][0]
    if course not in dropdowns["courses"] and course != "All":
        course = dropdowns["courses"][0]
    if swp not in dropdowns["swp"] and swp != "All":
        swp = dropdowns["swp"][0]      
    return f'../students/?dept={dept}&course={course}&term={term}&swp={swp}'

def filter_swp_data(dept, course, term, swp):
    #Building query based on All keyword
    query = "Select * from student_work_product" 
    where_cluase, data = "", tuple()
    if dept != "All": 
        if where_cluase: where_cluase += " and "
        where_cluase += "dept_id=?"
        data += (dept,)
    if course != "All":
        if where_cluase: where_cluase += " and "
        where_cluase += "course_id=?"
        course_num = course.split()[0]
        data += (course_num,)
    if term != "All":
        if where_cluase: where_cluase += " and "
        where_cluase += "term=? and year=?"
        semester = term.split()[0]
        year = term.split()[1]
        data += (semester,year)
    if swp != "All":
        if where_cluase: where_cluase += " and "
        where_cluase += "product=?"
        data += (swp,)
    if where_cluase:
        query += " where "+ where_cluase + ''' order by year desc, 
            case when term="Spring" then 0 when term="Summer" then 1 
            when term="Fall" then 2 end, student_lname, student_fname;'''
    #Getting data
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute (query, data)
        records = c.fetchall()
    return records

def verify_swp_table(form_data):
    data = []
    for i in range(0, len(form_data.getlist('CourseId'))):
        #Id
        try:
            RowId = int(form_data.getlist('RowId')[i])
        except ValueError: #New row
            RowId = None
        #Course Number
        CourseNum = int(form_data.getlist('CourseId')[i])
        if not 999 < CourseNum < 10000: raise ValueError("Course Number can only be 4 digets")
        #Department ID
        DeptId = form_data.getlist('DeptId')[i].upper().strip()
        if len(DeptId) != 4: raise ValueError("Department ID can only be 4 characters")
        #Product
        Product = form_data.getlist('Product')[i].replace("\n", "").strip()
        # Product = ' '.join(word[0].upper() + word[1:] for word in Title.split())
        if len(Product) > 250:raise ValueError("Title can only be 100 characters")
        elif not Product: raise ValueError("Title can not be blank")
        #First Name
        Fname = form_data.getlist('Fname')[i].title().strip()
        if len(Fname) > 35: raise ValueError("First Name can only be 100 characters")
        elif not Fname: raise ValueError("First Name can not be blank")
        #Last Name
        Lname = form_data.getlist('Lname')[i].title().strip()
        if len(Lname) > 35: raise ValueError("Last Name can only be 100 characters")
        elif not Lname: raise ValueError("Last Name can not be blank")
        #Outcome
        Outcome = int(form_data.getlist('Outcome')[i])
        if not 0 <= Outcome <= 4: raise ValueError("The student Outcome can only between 0-4")
        #Score
        Score = int(form_data.getlist('Score')[i])
        if not 0 <= Score <= 100: raise ValueError("The student Score can only between 0-100")
        #Term
        Term = form_data.getlist('Term')[i].title().strip()
        if not Fname: raise ValueError("Term can not be blank")
        elif Term not in ['Fall', 'Spring', 'Summer']: raise ValueError("Term can can only be Fall, Spring, or Summer")
        #Year
        Year = int(form_data.getlist('Year')[i])
        #Append data
        data.append((RowId, Product, CourseNum, DeptId, Fname, Lname, Outcome, Score, Term, Year))
    return data

def update_students(data, original_data):
    #Getting data modification types
    o_data = [
        (x['id'], x['product'], x['course_id'], x['dept_id'],
         x['student_fname'], x['student_lname'], x['student_outcome'],
         x['score'], x['term'], x['year']) for x in original_data]
    original_ids = [x[0] for x in o_data]
    data_ids = [x[0] for x in data]
    deleted_rows = [x for x in original_ids if x not in data_ids]
    modified_rows = [x[0] for x in o_data if x not in data and x[0] not in deleted_rows]
    new_rows = [x for x in data if x[0] == None]
    #SQL Connection
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #Modifing rows
        for r_id in modified_rows:
            d = next(x for x in data if r_id == x[0])
            o = next(x for x in o_data if r_id == x[0])
            #If course does not exist -> stop
            if not course_exists(d): return d
            #If product is changed -> update course swp's
            if d[1] != o[1]: update_course_swp(d)
            #Updating student record
            c.execute('''UPDATE student_work_product SET product=?,
                    course_id=?, dept_id=?, student_fname=?, student_lname=?,
                    student_outcome=?, score=?, term=?, year=?
                    where id=?''', d[1:]+(d[0],))
            conn.commit()
        #New rows
        for r in new_rows:
            #If course does not exist -> stop
            if not course_exists(r): return r
            #If product is changed -> update course swp's
            update_course_swp(r)
            #Updating student record
            c.execute('''INSERT INTO student_work_product (product,
                    course_id, dept_id, student_fname, student_lname,
                    student_outcome, score, term, year)
                    VALUES(?,?,?,?,?,?,?,?,?);''', (r[1:]))
            conn.commit()
        #Deleting rows
        for r_id in deleted_rows:
            query = "DELETE FROM student_work_product WHERE id=?"
            c.execute(query, (r_id,))
            conn.commit()
    return None

def course_exists(data):
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        c.execute('''Select course_number from course
                        where dept_id=? and course_number=?
                        and term=? and year=?''', (data[3], data[2], data[8], data[9]))
        record = c.fetchone()
    if record: return True
    else: False

def update_course_swp(data):
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''Select student_work_products from course
                        where dept_id=? and course_number=?
                        and term=? and year=?''', (data[3], data[2], data[8], data[9]))
        record = c.fetchone()
        swps = json.loads(record['student_work_products'])['swp']
        #If new product -> update
        if data[1] in swps: return
        else:
            swps.append(data[1])
            j_swps = json.dumps({"swp": swps})
            c.execute('''UPDATE course SET student_work_products=?
            where dept_id=? and course_number=?
            and term=? and year=?''', (j_swps, data[3], data[2], data[8], data[9]))
            conn.commit()
            add_students_on_new_swp(data)

def add_students_on_new_swp(data, new_swp=None):
    #Course
    if len(data) == 8:
        new_swp=new_swp
        dept_id, course_id, term, year = data[1], data[0], data[6], data[7]
    #Student work prodcut
    elif len(data) == 10:
        new_swp = data[1]
        dept_id, course_id, term, year = data[3], data[2], data[8], data[9]
    else: 
        raise ValueError("Unknow data passed in. We are expecting data from update_course_swp() or update_courses()")
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''Select student_fname, student_lname from student_work_product
            where dept_id=? and course_id=? and term=? and year=?
            group by student_fname, student_lname;''', (dept_id, course_id, term, year))
        records = c.fetchall()
        #Creating new student data
        new_student_vales = [
            (new_swp, course_id, dept_id, x['student_fname'], x['student_lname'], term, year)
            for x in records]
        c.executemany('''INSERT INTO student_work_product (product,
                    course_id, dept_id, student_fname, student_lname,
                    term, year) VALUES (?,?,?,?,?,?,?);''', new_student_vales)
        conn.commit()
    return

def check_student_product_sync(course, dept_id, term):
    """Checks if there are students missing in a swp of a course

    Args:
        course ([str]): 0-4 is course number, rest can be course title
        dept_id ([str]): 4 letter department ID
        term ([str]): 'semester year'

    Returns:
        [boolean]: True  = students are synced, no update needed
                   False = students are not synced, update available 
    """
    course_num = int(course[:4])
    term, year = term.split()
    year = int(year)
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        # Checking uneven student numbers in swp table
        c.execute('''select DISTINCT(product), count(product) from student_work_product 
            where dept_id=? and course_id=? and term=? and year=?
            group by product''', (dept_id, course_num, term, year, ))
        records = c.fetchall()
        if not records: return True #No students, nothing to sync
        if not len(set([x[1] for x in records]))==1: return False
        #Checking course swp not in student_work_product
        c.execute('''select student_work_products from course 
            where dept_id=? and course_number=? and term=? and year=?''',
            (dept_id, course_num, term, year, ))
        course_swps = json.loads(c.fetchone()[0])
        if set([x[0] for x in records]) != set(course_swps['swp']): return False
    return True

def sync_students(course, dept_id, term):
    course_num = int(course[:4])
    term, year = term.split()
    year = int(year)
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        #swp Products
        c.execute('''select DISTINCT(product) from student_work_product 
            where dept_id=? and course_id=? and term=? and year=?''', 
            (dept_id, course_num, term, year, ))
        all_products = set([x[0] for x in c.fetchall()])
        c.execute('''select student_work_products from course 
            where dept_id=? and course_number=? and term=? and year=?''', 
            (dept_id, course_num, term, year, ))
        course_swps = json.loads(c.fetchone()[0])
        for swp in course_swps['swp']: all_products.add(swp)
        c.execute('''select student_fname, student_lname, product from student_work_product 
            where dept_id=? and course_id=? and term=? and year=?
            group by student_fname, student_lname, product''', 
            (dept_id, course_num, term, year, ))
        students = c.fetchall()
        data = {}
        for s in students:
            name = s[0] + " " + s[1]
            if name in data:
                data[name].append(s[2])
            else: 
                data[name] = [s[2]]
        s_to_sync = [k for k,v in data.items() if set(v)!= all_products]
        for s in s_to_sync:
            fname, lname = s.split()
            products_missing = list(all_products - set(data[s]))
            for p in products_missing:
                c.execute('''INSERT INTO student_work_product (product,
                    course_id, dept_id, student_fname, student_lname,
                    term, year) VALUES(?,?,?,?,?,?,?);''', 
                    (p, course_num, dept_id, fname, lname, term, year))
                conn.commit()
    return

