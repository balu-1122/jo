from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os

app = Flask(__name__, template_folder='templates')

# Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'santhosh'
app.config['MYSQL_PASSWORD'] = 'Balu@123580'
app.config['MYSQL_DB'] = 'DEMO'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Define upload path
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST', 'GET'])
def generate_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        education = request.form.get('education')

        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                skills TEXT NOT NULL,
                experience TEXT NOT NULL,
                education TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO resume (name, email, phone, skills, experience, education)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, email, phone, skills, experience, education))

        conn.commit()
        cursor.close()

        return render_template('resume.html', name=name, email=email, phone=phone, skills=skills, experience=experience, education=education)
    
    return render_template('create_resume.html')

@app.route('/job_posting', methods=['POST', 'GET'])
def post_job():
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        company_name = request.form.get('company_name')
        job_description = request.form.get('job_description')
        location = request.form.get('location')
        job_type = request.form.get('job_type')
        salary = request.form.get('salary')
        no_of_vacancies = int(request.form.get('no_of_vacancies'))

        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(100) NOT NULL,
                company_name VARCHAR(100) NOT NULL,
                job_description TEXT NOT NULL,
                location VARCHAR(100) NOT NULL,
                job_type VARCHAR(50) NOT NULL,
                salary VARCHAR(50) NOT NULL,
                no_of_vacancies INT NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO jobs (job_title, company_name, job_description, location, job_type, salary, no_of_vacancies)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (job_title, company_name, job_description, location, job_type, salary, no_of_vacancies))

        conn.commit()
        cursor.close()

        return render_template('job_post.html', job_title=job_title, company_name=company_name, job_description=job_description, location=location, job_type=job_type, salary=salary, no_of_vacancies=no_of_vacancies)
    
    return render_template('job_posting.html')

@app.route('/job_listing')
def job_listing():
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT id, job_title, company_name, location, salary FROM jobs")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('job_listing.html', jobs=jobs)



# Define additional job category routes with corrections
@app.route('/software_dev', methods=['GET'])
def software_dev():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('software developer', 'web developer', 'software engineer')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('software_dev.html', jobs=jobs)


@app.route('/data_science',methods=['GET'])
def data_science():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('data scientist', 'data analytics')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('data_science.html', jobs=jobs)

@app.route('/u_design',methods=['GET'])
def u_design():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('UX', 'UI', 'UI/UX design')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('u_design.html', jobs=jobs)

@app.route('/product_man',methods=['GET'])
def product_manager():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('product manager', 'product designer')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('product_man.html', jobs=jobs)

@app.route('/customer_support',methods=['GET'])
def customer_support():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('customer support', 'customer care')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('customer_support.html', jobs=jobs)

@app.route('/sales_ex',methods=['GET'])
def sales_ex():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('sales person', 'sales executive')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('sales_ex.html', jobs=jobs)

@app.route('/teacher',methods=['GET'])
def teaching():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('tutor', 'teaching')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('teacher.html', jobs=jobs)

@app.route('/human_res',methods=['GET'])
def human_res():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title = 'human resources'")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('human_res.html', jobs=jobs)

@app.route('/business_dev', methods=['GET'])
def business_dev():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, job_title, company_name, job_description, location, job_type, salary, no_of_vacancies FROM jobs WHERE job_title IN ('business adviser', 'business development')")
    jobs = cursor.fetchall()
    cursor.close()
    return render_template('business_dev.html', jobs=jobs)

def allowed_file(filename):
    allowed_extensions = {'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route for job application form
@app.route('/apply/<int:id>', methods=['GET', 'POST'])
def apply(id):
    conn = mysql.connection
    cursor = conn.cursor()

    # Fetch job details for the job ID
    cursor.execute("SELECT job_title, company_name FROM jobs WHERE id = %s", (id,))
    job = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Get form data
        applicant_name = request.form.get('name')
        applicant_email = request.form.get('email')
        applicant_phone = request.form.get('phone')
        resume_file = request.files.get('resume')

        # Check if the file is uploaded
        if resume_file and resume_file.filename:
            # Check file type
            if allowed_file(resume_file.filename):
                filename = secure_filename(resume_file.filename)
                resume_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Save application in the database
                conn = mysql.connection
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO applications (job_id, name, email, phone, resume)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (id, applicant_name, applicant_email, applicant_phone, filename))

                conn.commit()
                cursor.close()

                # Return a confirmation message to the user
                return render_template('application_success.html', job_title=job[0], company_name=job[1])

        return "Invalid file type. Only PDF, DOC, and DOCX files are allowed.", 400

    return render_template('apply.html', job_id=id, job=job)


if __name__ == '__main__':
    app.run(debug=True)
