'''
Placement views
'''
from app import fapp
from app.query import gen_excel_sheets
# from app.controller import login_student, login_placementuser
import app.controller as control
from flask import send_from_directory, render_template, flash, redirect, \
        url_for, session, request
# from flask.ext.login import login_user, logout_user, current_user, login_required
from config import EXCEL_FILES_DIR
from functools import wraps
import json
import sys, os

def login_required_placement(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in_placement' in session:
            return f(*args, **kwargs)
        else:
            flash("Please Log In")
            return redirect(url_for('admin_login'))
    return wrap

@fapp.route('/admin')
@login_required_placement
def admin_index():
    return render_template('admin/index.html')
    # return render_template('index.html')

@fapp.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@fapp.route('/admin/forms')
def admin_forms():
    return render_template('admin/forms.html')

@fapp.route('/admin/summarize')
def admin_summarize():
    return render_template('admin/summarize.html')

@fapp.route('/admin/statistics')
def admin_statistics():
    return render_template('admin/statistics.html')

# @fapp.route('/companies.html')
# @login_required_placement
# def admin_companies():
#     return render_template('companies.html')

@fapp.route('/placement/login', methods=['POST'])
def placement_login():
    username = request.form['username']
    password = request.form['password']
    if not control.login_placementuser(username, password):
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('index'))
    # login_user(registered_user)
    session['username'] = username
    session['logged_in_placement'] = True
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('placement_dashboard'))

# @fapp.route('/placement/dashboard')
# @login_required_placement
# def placement_dashboard():
#     return render_template('404.html') # Placement dashboard

@fapp.route("/placement/generate", methods=['GET'])
# @login_required_placement
def get_excel():
    comp_id = request.args.get('id')
    filename = gen_excel_sheets(comp_id)
    if filename:
        return send_from_directory(EXCEL_FILES_DIR, filename, as_attachment=True)

@fapp.route("/placement/get_new_registrants", methods=['GET'])
# @login_required_placement
def get_new_registrants():
    data = control.get_new_registrants()
    return json.dumps(data)

@fapp.route("/placement/add_student", methods=['POST'])
# @login_required_placement
def add_student():
    data = request.get_json()
    # data = request.data
    print('data stu', data)
    # control.add_student(**data)
    control.add_student(data['usn'], data['name'], data['stream'],
                data['age'], data['per10'], data['per12'], data['CGPA'],
                data['email_id'], data['resume_link'])
    return ""

@fapp.route("/placement/add_company", methods=['POST'])
# @login_required_placement
def add_company():
    # data = json.loads(request.data)
    # data = request.get_json()
    try:
        data = request.form
        # print('data com', data)
        b = control.add_company(data['name'], data['cgpa'])
        # if b:
        #     return redirect('/admin/pages/forms.html')
    except:
        print(sys.exc_info())
    return redirect('/admin/pages/forms.html')

# @fapp.route("/dashboard/add_company", methods=['POST'])
# def add_comp():
#     name = request.form('name')
#     company_id = request.form('company_id')
#     cutoff_gpa = request.form('cutoff_gpa')
#     register_date = request.form('register_date')
#     test_date = request.form('test_date')
#     interview_date = request.form('interview_date')
#     tier = request.form('tier')
#     website = request.form('website')
#     postal_address = request.form('postal_address')
#     company_sector = request.form('company_sector')

@fapp.route("/placement/send_mail")
def call_php():
    with open('file.txt', 'w') as f:
        print(request.args.get('message'), file=f)
    from subprocess import call
    call(["php", "-f", "app/templates/send.php"])
    # os.system("php -f app/templates/send.php")
    return 'ok'
