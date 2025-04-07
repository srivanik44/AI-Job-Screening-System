import sqlite3

# Function to create a new SQLite database and tables
def create_database():
    conn = sqlite3.connect('job_screening_system.db')  # You can change the database name if you prefer
    cursor = conn.cursor()

    # Create job descriptions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create candidates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        cv_filename TEXT,
        match_score REAL,
        job_id INTEGER,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES job_descriptions(id)
    )
    ''')

    # Create interviews table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        interview_date TEXT,
        status TEXT,
        scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to insert a job description
def insert_job_description(title, description):
    conn = sqlite3.connect('job_screening_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO job_descriptions (title, description)
    VALUES (?, ?)
    ''', (title, description))

    conn.commit()
    conn.close()

# Function to insert a candidate
def insert_candidate(name, email, cv_filename, match_score, job_id):
    conn = sqlite3.connect('job_screening_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO candidates (name, email, cv_filename, match_score, job_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, cv_filename, match_score, job_id))

    conn.commit()
    conn.close()

# Function to schedule an interview
def schedule_interview(candidate_id, interview_date, status="Scheduled"):
    conn = sqlite3.connect('job_screening_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO interviews (candidate_id, interview_date, status)
    VALUES (?, ?, ?)
    ''', (candidate_id, interview_date, status))

    conn.commit()
    conn.close()

# Function to fetch candidates that need interviews (match score > 20%)
def get_candidates_for_interview(min_score=20):
    conn = sqlite3.connect('job_screening_system.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT candidates.name, candidates.email, candidates.match_score, job_descriptions.title
    FROM candidates
    JOIN job_descriptions ON candidates.job_id = job_descriptions.id
    WHERE candidates.match_score >= ?
    ''', (min_score,))

    candidates = cursor.fetchall()
    conn.close()

    return candidates
