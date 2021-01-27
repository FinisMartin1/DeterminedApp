from collections import Counter
import sqlite3
import json

from data.student import add_students_on_new_swp

def get_all_courses():
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("Select * from course order by year, term asc")
        records = c.fetchall()
    data = []
    for r in records:
        d = dict(r)
        d['swp'] = ", ".join(json.loads(r['student_work_products'])['swp'])
        data.append(d)
    data.reverse()
    return data

def update_courses(data, original):
    if not data: return 
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if original:
            for i in range(0, len(data)):
                d, o = data[i], original[i]
                #Updating course table
                query = '''UPDATE course SET
                        course_number=?, dept_id=?, title=?, instructor_fname=?, 
                        instructor_lname=?, student_work_products=?, term=?, year=?
                        where course_number=? and term=? and year=?;
                        '''
                values = d + (o[0], o[6], o[7])
                c.execute(query, values)
                conn.commit()
                #Checking if forign keys were updated, if so modify student_work_prodcut table
                #Checking (course_num, dept_id, swp, term, year)
                if (d[0], d[1], d[5], d[6], d[7]) != (o[0], o[1], o[5], o[6], o[7]):
                    #If primary keys change -> check if there will be a conflict -> return bad row
                    if (d[0], d[1], d[6], d[7]) != (o[0], o[1], o[6], o[7]):
                        failed = check_course_pk(d)
                        if failed: return failed
                    #Updating SWP's
                    swp_matchup = {} #old swp : new swp
                    old_swps, new_swps = json.loads(o[5])['swp'], json.loads(d[5])['swp']
                    #Adding students if new swps
                    for swp in new_swps[len(old_swps):]: 
                        add_students_on_new_swp(d, swp)
                    for i, swp in enumerate(old_swps):
                        try:
                            swp_matchup[swp] = new_swps[i]
                        except IndexError:
                            swp_matchup[swp] = None
                    #Getting students that need to be modified/deleted
                    c.execute("""SELECT id, product from student_work_product
                        where course_id=? and dept_id=? and term=? and year=?""", (o[0], o[1], o[6], o[7]))
                    students = c.fetchall()
                    modify_students, delete_students = [], []
                    for s in students:
                        if s['product'] not in swp_matchup:
                            pass #Newly created students b/c of new swp
                        elif swp_matchup[s['product']]:
                            modify_students.append((swp_matchup[s['product']], d[0], d[1], d[6], d[7], s['id']))
                        else: delete_students.append((s['id'],))
                    if modify_students:
                        c.executemany('''UPDATE student_work_product SET
                            product=?, course_id=?, dept_id=?, term=?, year=?
                            where id=?''', modify_students)
                        conn.commit()
                    if delete_students:
                        c.executemany('''DELETE FROM student_work_product WHERE id=?''', delete_students)
                        conn.commit()    
        #New Course
        else: 
            query = '''
                INSERT into course (course_number, dept_id, title, instructor_fname, instructor_lname, student_work_products, term, year)
                VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(course_number, term, year) DO UPDATE SET
                course_number=?, dept_id=?, title=?, instructor_fname=?, instructor_lname=?, student_work_products=?, term=?, year=?;
            '''
            data = [x+x for x in data]
            c.executemany(query, data)
            conn.commit()
    return None

def delete_course(data):
    if not data: return
    #(course_num, dept_id, term, year)
    values = [(x[0], x[1], x[6], x[7]) for x in data]
    with sqlite3.connect("determined.db") as conn:
        c = conn.cursor()
        query = "DELETE FROM course WHERE course_number=? and dept_id=? and term=? and year=?"
        c.executemany(query, values)
        conn.commit()
        query = "DELETE FROM student_work_product WHERE course_id=? and dept_id=? and term=? and year=?"
        c.executemany(query, values)
        conn.commit()
    return 

def check_course_pk(data):
    #(course_num, dept_id, term, year)
    new_keys = set([(x[0], x[1], x[6], x[7]) for x in data])
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("Select course_number, dept_id, term, year from course")
        records = c.fetchall()
    existing_keys = set([(x['course_number'], x['dept_id'], x['term'], x['year']) for x in records])
    return [x for x in new_keys if x in existing_keys]


def filter_course_term(courses, term):
    term, year = term.split()
    return [x for x in courses if x['term'] == term and x['year'] == int(year)] 

def verify_course_table(form_data):
    data = []
    for i in range(0, len(form_data.getlist('CourseNum'))):
        #Course Number
        CourseNum = int(form_data.getlist('CourseNum')[i])
        if not 999 < CourseNum < 10000: raise ValueError("Course Number can only be 4 digets")
        #Department ID
        DeptId = form_data.getlist('DeptId')[i].upper().strip()
        if len(DeptId) != 4: raise ValueError("Department ID can only be 4 characters")
        #Title
        Title = form_data.getlist('Title')[i].replace("\n", "").strip()
        Title = ' '.join(word[0].upper() + word[1:] for word in Title.split())
        if len(Title) > 100:raise ValueError("Title can only be 100 characters")
        elif not Title: raise ValueError("Title can not be blank")
        #First Name
        Fname = form_data.getlist('Fname')[i].title().strip()
        if len(Fname) > 35: raise ValueError("First Name can only be 100 characters")
        elif not Fname: raise ValueError("First Name can not be blank")
        #Last Name
        Lname = form_data.getlist('Lname')[i].title().strip()
        if len(Lname) > 35: raise ValueError("Last Name can only be 100 characters")
        elif not Lname: raise ValueError("Last Name can not be blank")
        #SWP
        SWP = form_data.getlist('SWP')[i].replace("\n", "").strip().split(", ")
        if len(SWP) == 0:raise ValueError("SWP can not be blank")
        SWP_json = json.dumps({"swp":SWP})
        #Term
        Term = form_data.getlist('Term')[i].title().strip()
        if not Fname: raise ValueError("Term can not be blank")
        elif Term not in ['Fall', 'Spring', 'Summer']: raise ValueError("Term can can only be Fall, Spring, or Summer")
        #Year
        Year = int(form_data.getlist('Year')[i])
        #Append data
        data.append((CourseNum, DeptId, Title, Fname, Lname, SWP_json, Term, Year))
    return data
        
def course_difference(courses, form_data):
    items = Counter([tuple(v.values())[:-1] for v in courses] + form_data)
    deleted, modified, original = [], [], []
    for k,v in items.items():
        if v==1:
            if k in form_data:
                modified.append(k)
            else: 
                deleted.append(k)
                original.append(k)

    #removing modified items from deleted
    for x in deleted:
        if any([y for y in modified if y[0] == x[0]]):
            deleted.remove(x)
        else: 
            original.remove(x)
    return modified, deleted, original