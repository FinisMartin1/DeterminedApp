import sqlite3
import random
import json

def university_swp():
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("""Select course_id, title, student_work_product.term, student_work_product.year, avg(student_outcome) as avg from student_work_product 
            join course on course_id=course_number
            group by course_id, student_work_product.term, student_work_product.year 
			order by student_work_product.year, student_work_product.term""")
        student_outcome_avgs = [dict(x) for x in c.fetchall()] 
        c.execute("""Select term, year from course
            group by term, year
            order by year, term""")
        label_dict = [dict(x) for x in c.fetchall()] 
    #Creating table lables
    labels = []
    for item in label_dict:
        labels.append(f"{item['term']} {item['year']}")
    #Getting graph data for each course
    data = {}
    for r in student_outcome_avgs:
        if r['course_id'] in data:
            data[r['course_id']]['data'].append({
                'x':f"{r['term']} {r['year']}", 
                'y': round(r['avg'], 3) if r['avg'] else 0
            })
        else:
            data[r['course_id']] = {
                'data': [{
                    'x':f"{r['term']} {r['year']}", 
                    'y': round(r['avg'], 3) if r['avg'] else 0
                    }], 
                'name': r['title']}
    #Getting colors
    colors = ['#3A3B0A', '#9BEFE7', '#EB953C', '#0A18DB', '#756F80', '#C5E0A2', '#480704', '#4F070D', '#4A8CDA', '#DBD3C3', '#F89B85', '#85079F', '#A27FEF', '#15C8F2', '#1CF07A', '#58EC0C', '#952F74', '#906264', '#FCABB0', '#0D4BC1']
    dataset = []
    for _, v in data.items():
        color = colors.pop(0)
        dataset.append(
            {"label": v['name'], "fill": False, "data": v['data'], "backgroundColor": color, "borderColor": color}
        )
    graph_html = json.dumps({"type": "line",
                  "data": {"labels": labels, "datasets": dataset},
                  "options": {"hover":{"mode":"point"}, "maintainAspectRatio": False, "legend": {"display": True, "position":"bottom"}, "title": {}, "scales": {"xAxes": [{"gridLines": {"color": "rgb(234, 236, 244)", "zeroLineColor": "rgb(234, 236, 244)", "drawBorder": False, "drawTicks": False, "borderDash": ["2"], "zeroLineBorderDash":["2"], "drawOnChartArea":False, "tyep": "category"}, "ticks":{"fontColor": "#858796", "padding": 20}}], "yAxes": [{"gridLines": {"color": "rgb(234, 236, 244)", "zeroLineColor": "rgb(234, 236, 244)", "drawBorder": False, "drawTicks": False, "borderDash": ["2"], "zeroLineBorderDash":["2"]}, "ticks":{"fontColor": "#858796", "padding": 20, }}]}}})
    return graph_html

def university_instructors():
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("""Select instructor_fname || " " || instructor_lname as title, 
            student_work_product.term, student_work_product.year, avg(student_outcome) as avg 
            from student_work_product 
            join course on course_id=course_number
            group by title, student_work_product.term, student_work_product.year 
            order by student_work_product.year, student_work_product.term""")
        student_outcome_avgs = [dict(x) for x in c.fetchall()] 
        c.execute("""Select term, year from course
            group by term, year
            order by year, term""")
        label_dict = [dict(x) for x in c.fetchall()] 
    #Creating table lables
    labels = []
    for item in label_dict:
        labels.append(f"{item['term']} {item['year']}")
    #Getting graph data for each course
    data = {}
    for r in student_outcome_avgs:
        if r['title'] in data:
            data[r['title']]['data'].append({
                'x':f"{r['term']} {r['year']}", 
                'y': round(r['avg'], 3)
            })
        else:
            data[r['title']] = {
                'data': [{
                    'x':f"{r['term']} {r['year']}", 
                    'y': round(r['avg'], 3)
                    }], 
                'name': r['title']}
    #Getting colors
    colors = ['#3A3B0A', '#9BEFE7', '#EB953C', '#0A18DB', '#756F80', '#C5E0A2', '#480704', '#4F070D', '#4A8CDA', '#DBD3C3', '#F89B85', '#85079F', '#A27FEF', '#15C8F2', '#1CF07A', '#58EC0C', '#952F74', '#906264', '#FCABB0', '#0D4BC1']
    dataset = []
    for _, v in data.items():
        color = colors.pop(0)
        dataset.append(
            {"label": v['name'], "fill": False, "data": v['data'], "backgroundColor": color, "borderColor": color}
        )
    graph_html = json.dumps({"type": "line",
                  "data": {"labels": labels, "datasets": dataset},
                  "options": {"hover":{"mode":"point"}, "maintainAspectRatio": False, "legend": {"display": True, "position":"bottom"}, "title": {}, "scales": {"xAxes": [{"gridLines": {"color": "rgb(234, 236, 244)", "zeroLineColor": "rgb(234, 236, 244)", "drawBorder": False, "drawTicks": False, "borderDash": ["2"], "zeroLineBorderDash":["2"], "drawOnChartArea":False, "tyep": "category"}, "ticks":{"fontColor": "#858796", "padding": 20}}], "yAxes": [{"gridLines": {"color": "rgb(234, 236, 244)", "zeroLineColor": "rgb(234, 236, 244)", "drawBorder": False, "drawTicks": False, "borderDash": ["2"], "zeroLineBorderDash":["2"]}, "ticks":{"fontColor": "#858796", "padding": 20, }}]}}})
    return graph_html

def course_selection():
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("Select title, course_number, dept_id from course group by course_number order by title")
        records = [dict(x) for x in c.fetchall()] 
    courses = [{"name": f"{x['title']} - {x['dept_id']} {x['course_number']}", "id": x['course_number']} for x in records]
    return courses

def instructor_selection():
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ('''Select distinct(instructor_fname || " " || instructor_lname) as title 
            from course order by title''')
        records = [dict(x) for x in c.fetchall()] 
    instructors = [{"name": x['title']} for x in records]
    return instructors

def course_graphs(course_id):
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #SWP
        c.execute ("""Select term, year, avg(student_outcome) as avg from student_work_product
            where course_id=?
            group by term, year order by year, term""", (course_id, ))
        records = [dict(x) for x in c.fetchall()]
        labels = [f"{x['term']} {x['year']}" for x in records]
        data = [f"{round(x['avg'], 3)}" for x in records] 
        swp_graph = json.dumps({"type":"line","data":{"labels":labels,"datasets":[{"label":"Average SWP","fill":False,"data":data,"backgroundColor":"rgba(78, 115, 223, 0.05)","borderColor":"rgba(78, 115, 223, 1)"}]},"options":{"maintainAspectRatio":False,"legend":{"display":False},"title":{},"scales":{"xAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"],"drawOnChartArea":False},"ticks":{"fontColor":"#858796","padding":20}}],"yAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"]},"ticks":{"fontColor":"#858796","padding":20, 'suggestedMin': 0, "suggestedMax":4}}]}}})
        
        #Pass / Fail
        c.execute ("""SELECT (select count(*) as fail from (select avg(score) as avg_score from student_work_product
            group by student_fname, student_lname 
            having avg_score < 70 and course_id = ?)) as fail, 
            (select count(*) as pass from (select avg(score) as avg_score from student_work_product
            group by student_fname, student_lname 
            having avg_score >= 70 and course_id = ?)) as pass""", (course_id, course_id))
        records = [dict(x) for x in c.fetchall()][0]
        pass_fail_graph = json.dumps({"type":"doughnut","data":{"labels":["Pass","Fail"],"datasets":[{"label":"","backgroundColor":["#4edf5c","#cc3675"],"borderColor":["#ffffff","#ffffff"],"data":[records['pass'],records['fail']]}]},"options":{"maintainAspectRatio":False,"legend":{"display":False,"reverse":False},"title":{}}})
        
        #SWP Count
        c.execute ("""select student_outcome, count(student_outcome)as count from student_work_product
            where course_id=?
            group by student_outcome""", (course_id, ))
        records = [dict(x) for x in c.fetchall()]
        labels = ["No Credit", "Poor", "Good", "Very Good", "Excellent" ]
        data = [x['count'] for x in records]
        swp_count_graph = json.dumps({"type":"bar","data":{"labels":labels,"datasets":[{"label":"Average SWP","backgroundColor":"rgba(78, 115, 223, 1)","borderColor":"rgba(78, 115, 223, 1)","data":data}]},"options":{"maintainAspectRatio":False,"legend":{"display":False},"title":{},"scales":{"xAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"],"drawOnChartArea":False},"ticks":{"fontColor":"#858796","padding":20}}],"yAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"]},"ticks":{"fontColor":"#858796","padding":20}}]}}})
        
        #Grade Scatter
        c.execute ("""select score, count(score)as count from student_work_product
            where course_id=?
            group by score
            """, (course_id, ))
        records = [dict(x) for x in c.fetchall()]
        data = [{'x': x['score'], 'y': x['count']} for x in records]
        grade_graph = json.dumps({"type": "scatter", "data": {"datasets": [{"label": "", "backgroundColor": "rgba(78, 115, 223, 1)", "borderColor": "rgba(78, 115, 223, 1)", "data": data}]}, "options": {"maintainAspectRatio": False, "legend": {"display": False, "reverse": False}, "title": {}, "scales": {'yAxes': [{"scaleLabel": {"display": True,"labelString": 'Count'}}], 'xAxes': [{"scaleLabel": {"display": True,"labelString": 'Grade'}}]}}})
    return swp_graph, pass_fail_graph, swp_count_graph, grade_graph


def instructor_graphs(instructor_fname, instructor_lname):
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #SWP
        c.execute ("""Select course.term, course.year, avg(student_outcome) as avg 
            from student_work_product join course on 
            course_id=course_number and student_work_product.dept_id=course.dept_id
            and student_work_product.term=course.term and student_work_product.year=course.year
            where instructor_fname=? and instructor_lname=?
            group by course.term, course.year order by course.year, course.term""", (instructor_fname, instructor_lname))
        records = [dict(x) for x in c.fetchall()]
        labels = [f"{x['term']} {x['year']}" for x in records]
        data = [f"{round(x['avg'], 3)}" for x in records] 
        swp_graph = json.dumps({"type":"line","data":{"labels":labels,"datasets":[{"label":"Average SWP","fill":False,"data":data,"backgroundColor":"rgba(78, 115, 223, 0.05)","borderColor":"rgba(78, 115, 223, 1)"}]},"options":{"maintainAspectRatio":False,"legend":{"display":False},"title":{},"scales":{"xAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"],"drawOnChartArea":False},"ticks":{"fontColor":"#858796","padding":20}}],"yAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"]},"ticks":{"fontColor":"#858796","padding":20, 'suggestedMin': 0, "suggestedMax":4}}]}}})
        
        #Pass / Fail
        c.execute ("""SELECT (select count(*) as fail from (select avg(score) as avg_score 
            from student_work_product join course on 
            course_id=course_number and student_work_product.dept_id=course.dept_id
            and student_work_product.term=course.term and student_work_product.year=course.year
            where instructor_fname=? and instructor_lname=?
            group by student_fname, student_lname 
            having avg_score < 70)) as fail, 
            (select count(*) as pass from (select avg(score) as avg_score 
            from student_work_product join course on 
            course_id=course_number and student_work_product.dept_id=course.dept_id
            and student_work_product.term=course.term and student_work_product.year=course.year
            where instructor_fname=? and instructor_lname=?
            group by student_fname, student_lname 
            having avg_score >= 70)) as pass""", 
            (instructor_fname, instructor_lname, instructor_fname, instructor_lname))
        records = [dict(x) for x in c.fetchall()][0]
        pass_fail_graph = json.dumps({"type":"doughnut","data":{"labels":["Pass","Fail"],"datasets":[{"label":"","backgroundColor":["#4edf5c","#cc3675"],"borderColor":["#ffffff","#ffffff"],"data":[records['pass'],records['fail']]}]},"options":{"maintainAspectRatio":False,"legend":{"display":False,"reverse":False},"title":{}}})
        
        #SWP Count
        c.execute ("""select student_outcome, count(student_outcome)as count 
            from student_work_product join course on 
            course_id=course_number and student_work_product.dept_id=course.dept_id
            and student_work_product.term=course.term and student_work_product.year=course.year
            where instructor_fname=? and instructor_lname=?
            group by student_outcome""", (instructor_fname, instructor_lname))
        records = [dict(x) for x in c.fetchall()]
        labels = ["No Credit", "Poor", "Good", "Very Good", "Excellent" ]
        data = [x['count'] for x in records]
        swp_count_graph = json.dumps({"type":"bar","data":{"labels":labels,"datasets":[{"label":"Average SWP","backgroundColor":"rgba(78, 115, 223, 1)","borderColor":"rgba(78, 115, 223, 1)","data":data}]},"options":{"maintainAspectRatio":False,"legend":{"display":False},"title":{},"scales":{"xAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"],"drawOnChartArea":False},"ticks":{"fontColor":"#858796","padding":20}}],"yAxes":[{"gridLines":{"color":"rgb(234, 236, 244)","zeroLineColor":"rgb(234, 236, 244)","drawBorder":False,"drawTicks":False,"borderDash":["2"],"zeroLineBorderDash":["2"]},"ticks":{"fontColor":"#858796","padding":20}}]}}})
        
        #Grade Scatter
        c.execute ("""select score, count(score)as count 
            from student_work_product join course on 
            course_id=course_number and student_work_product.dept_id=course.dept_id
            and student_work_product.term=course.term and student_work_product.year=course.year
            where instructor_fname=? and instructor_lname=?
            group by score""", (instructor_fname, instructor_lname))
        records = [dict(x) for x in c.fetchall()]
        data = [{'x': x['score'], 'y': x['count']} for x in records]
        grade_graph = json.dumps({"type": "scatter", "data": {"datasets": [{"label": "", "backgroundColor": "rgba(78, 115, 223, 1)", "borderColor": "rgba(78, 115, 223, 1)", "data": data}]}, "options": {"maintainAspectRatio": False, "legend": {"display": False, "reverse": False}, "title": {}, "scales": {'yAxes': [{"scaleLabel": {"display": True,"labelString": 'Count'}}], 'xAxes': [{"scaleLabel": {"display": True,"labelString": 'Grade'}}]}}})
    return swp_graph, pass_fail_graph, swp_count_graph, grade_graph

def get_instructor_courses(instructor_fname, instructor_lname):
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''select course_number, title from course
            where instructor_fname=? and instructor_lname=?
            GROUP by course_number, title''', (instructor_fname, instructor_lname))
    return [{'id':x['course_number'],'name':f"{x['title']} - {x['course_number']}"} for x in c.fetchall()]

def get_course_instructors(course_number):
    with sqlite3.connect("determined.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('''select instructor_fname, instructor_lname from course
            where course_number=?
            group by instructor_fname, instructor_lname;''', (course_number,))
    return [f"{x['instructor_fname']} {x['instructor_lname']}" for x in c.fetchall()]