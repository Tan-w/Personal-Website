from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'portal_secret_key'  # Updated secret for this portal

# Updated Apps List with URL links
apps = [
    {"name": "Smart Book Summarizer", 
     "desc": "Summarize books and generate bulk summaries", 
     "url": "https://smart-book-summarizer-with-bulk-summaries-177992425368.us-west1.run.app/"
    },
    {"name": "Excel to XML Conversion", 
     "desc": "Excel to XML Conversion", 
     "url": "https://toc-xml-transformer-agent-328911865014.us-west1.run.app/"
    },
    {"name": "Code Visualizer", 
     "desc": "Transform and preview code snippets quickly", 
     "url": "https://codeanim-engine-618449220226.us-west1.run.app/"
    },
    {"name": "Personalized Learning", 
     "desc": "Personalized Content Generate", 
     "url": "https://studio--studio-5470227012-af7ba.us-central1.hosted.app/"
    }
]

# # Mock Database for work allocation
# tasks = [
#     {
#         'id': 1, 'name': 'Intro to Python', 'duration': '320 Pages', 
#         'req_time': '32 Mins', 'priority': '0-Regular', 'course_code': '170345',
#         'round': 'Final QA', 'product': 'E-Book', 'status': 'Available'
#     }

# Advanced Mock Database
tasks = []
completed_data = []

@app.route('/add_task', methods=['POST'])
def add_task():
    if session.get('user') != 'Admin':
        return redirect(url_for('home'))
    
    # Calculate Required Time: Duration * Multiplier
    duration = float(request.form.get('duration', 0))
    multiplier = float(request.form.get('multiplier', 1))
    req_time = duration * multiplier

    new_task = {
        'id': len(tasks) + 1,
        'asset_id': request.form.get('asset_id'),
        'product_type': request.form.get('product_type'),
        'priority': request.form.get('priority'),
        'duration': duration,
        'multiplier': multiplier,
        'req_time': req_time,
        'round': request.form.get('round'),
        'status': 'Available',
        'vendor': request.form.get('vendor'),
        'received_date': request.form.get('received_date'),
        'picked_by': None,
        'picked_time': None,
        'edits': 0
    }
    tasks.append(new_task)
    return redirect(url_for('work_allocation'))

@app.route('/assign/<int:task_id>')
def assign(task_id):
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = 'In Progress'
            t['picked_by'] = session.get('user')
            t['picked_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return redirect(url_for('work_allocation'))

@app.route('/complete/<int:task_id>', methods=['GET', 'POST'])
def complete(task_id):
    # Accept GET or POST: prefer form value, fallback to query or 0
    num_edits = request.values.get('num_edits', 0)
    try:
        num_edits = int(num_edits)
    except Exception:
        num_edits = 0

    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            t['status'] = 'Completed'
            t['edits'] = num_edits
            t['completed_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            # Move to historical reporting
            completed_data.append(t)
            tasks.pop(i)
            break
    return redirect(url_for('work_allocation'))


@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', apps=apps, user=session['user'])
    return render_template('login.html')  # Show login if not authenticated


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Serve login page on GET, handle authentication on POST
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # Simple logic: Admin or Team role based on password
    if password == 'admin123':
        session['user'] = 'Admin'
        return redirect(url_for('home'))
    elif password == 'team123':
        session['user'] = 'Team Member'
        return redirect(url_for('home'))

    return "Invalid Credentials"  # You can make this a pretty error later


@app.route('/logout')
def logout():
    # session.clear() removes ALL data from the session
    session.clear()
    return redirect(url_for('home'))


@app.route('/work_allocation')
def work_allocation():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    # Separate tasks for the columns
    available = [t for t in tasks if t['status'] == 'Available']
    wip = [t for t in tasks if t['status'] == 'In Progress']
    
    return render_template('work_allocation.html', 
                           available=available, 
                           wip=wip, 
                           user_role=session.get('user'),
                           today=datetime.now().strftime("%A, %B %d, %Y"))


# Note: duplicate simple assign/complete handlers removed to avoid endpoint collisions.


@app.route('/summarizer')
def summarizer():
    return "Smart Book Summarizer App Page"


# About page
@app.route('/about_me')
def about_me():
    # Render About page; if not logged in still show general info
    if 'user' in session:
        return render_template('about_me.html', apps=apps, user=session['user'])
    return render_template('about_me.html', apps=apps, user=None)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/work_allocation')
def work_allocation():
    if 'user' not in session:
        return redirect(url_for('home'))

    # Get only tasks that are NOT assigned yet
    available_tasks = [t for t in tasks if t['status'] == 'Available']
    
    # Get tasks assigned to the current logged-in user
    my_tasks = [t for t in tasks if t['status'] == 'In-Progress' and t['picked_by'] == session['user']]

    return render_template('work_allocation.html', 
                           available=available_tasks, 
                           wip=my_tasks, 
                           user_role=session.get('user'))
@app.route('/assign/<int:task_id>')
def assign(task_id):
    if 'user' not in session:
        return redirect(url_for('home'))
        
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = 'In-Progress'
            t['picked_by'] = session['user']
            t['picked_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
    # Redirect back to the In-Progress tab
    return redirect(url_for('work_allocation', tab='progress'))