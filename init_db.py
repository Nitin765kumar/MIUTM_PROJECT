import os
import sqlite3

def initialize_production_database():
    if not os.path.exists('database'):
        os.makedirs('database')
        
    connection = sqlite3.connect('database/university.db')
    cursor = connection.cursor()
    
    # FORCE RESET: Drop legacy tables to apply the new schema containing 'department'
    print("[...] Clearing out old database schemas to apply structural updates...")
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS courses')
    cursor.execute('DROP TABLE IF EXISTS admissions')
    cursor.execute('DROP TABLE IF EXISTS contact_messages')
    cursor.execute('DROP TABLE IF EXISTS news_events')
    cursor.execute('DROP TABLE IF EXISTS faculty')
    
    # Re-build Core Infrastructure Tables
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'administrator'
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL UNIQUE,
        course_code TEXT NOT NULL UNIQUE,
        duration TEXT NOT NULL,
        eligibility TEXT NOT NULL,
        fees INTEGER NOT NULL,
        seats INTEGER NOT NULL,
        department TEXT NOT NULL,
        description TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_no TEXT NOT NULL UNIQUE,

    full_name TEXT NOT NULL,
    father_name TEXT NOT NULL,
    mother_name TEXT NOT NULL,

    gender TEXT NOT NULL,
    dob TEXT NOT NULL,

    email TEXT NOT NULL,
    phone TEXT NOT NULL,

    category TEXT,
    nationality TEXT DEFAULT 'Indian',

    qualification TEXT NOT NULL,
    percentage REAL NOT NULL,

    course_name TEXT NOT NULL,

    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    pincode TEXT NOT NULL,

    status TEXT NOT NULL DEFAULT 'Pending',

    remarks TEXT,

    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    ''')
    
    cursor.execute('''
    CREATE TABLE contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE news_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        publish_date TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        department TEXT NOT NULL,
        specialization TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')
    
    # Seed Admin Account
    cursor.execute("INSERT INTO users (id, username, password, role) VALUES (1, 'miutm_admin', 'MauryaSecure2026', 'administrator')")
    
    # Seed Courses with complete structural descriptions and department mappings
    courses_data = [
    (
        'Bachelor of Computer Applications', 'BCA', '3 Years',
        '10+2 standard with Mathematics or Computer Science, minimum 50% aggregate marks.',
        95000, 120, 'School of Computing Sciences',
        'Comprehensive program focusing on advanced software development, database architectures, full-stack frameworks, cloud computing, Artificial Intelligence, Cyber Security fundamentals, Advanced Python programming, and modern web & application development.'
    ),
    (
        'Bachelor of Business Administration', 'BBA', '3 Years',
        '10+2 standard across any structural academic stream with minimum 50% aggregate marks.',
        105000, 120, 'School of Management Studies',
        'Designed to cultivate leadership metrics, financial literacy, corporate strategy layouts, and entrepreneurial venture creation frameworks.'
    ),
    (
        'Bachelor of Technology (Computer Science & Engineering)', 'BTECH-CSE', '4 Years',
        '10+2 standard with clear passes in Physics, Chemistry, and Mathematics, minimum 60% baseline.',
        185000, 180, 'School of Engineering & Applied Technology',
        'Immersive engineering program specializing in Artificial Intelligence, Machine Learning, Cyber Security & Ethical Hacking, Advanced Python, Full Stack Development, Cloud Computing, Data Science, Distributed Systems, and Hardware Systems Architecture.'
    ),
    (
        'Master of Computer Applications', 'MCA', '2 Years',
        'Passed BCA / Bachelor Degree in Computer Science Engineering or equivalent with minimum 55% marks.',
        110000, 60, 'School of Computing Sciences',
        'Post-graduate curriculum emphasizing enterprise software design, Artificial Intelligence, Cyber Security, Advanced Python, Full Stack Development, Big Data Analytics, DevOps lifecycles, and Cloud-Native Application Development.'
    ),
    (
        'Master of Business Administration', 'MBA', '2 Years',
        'Graduation across any technical or non-technical discipline with minimum 50% marks alongside valid national entrance scorecard.',
        145000, 90, 'School of Management Studies',
        'Elite executive incubation curriculum specializing in global operational models, human capital strategy, predictive market analytics, and corporate governance architectures.'
    ),

    # ==========================
    # NEW TECHNOLOGY COURSES
    # ==========================

    (
        'Bachelor of Artificial Intelligence', 'BAI', '4 Years',
        '10+2 with Physics, Chemistry & Mathematics or Computer Science with minimum 55% aggregate marks.',
        165000, 120, 'School of Artificial Intelligence',
        'Comprehensive undergraduate program covering Machine Learning, Deep Learning, Generative AI, Natural Language Processing, Computer Vision, Robotics, Python Programming, Data Science, and AI Model Deployment.'
    ),

    (
        'Diploma in Cyber Security & Ethical Hacking', 'DCSEH', '1 Year',
        '10+2 or equivalent from any recognized board.',
        85000, 60, 'School of Cyber Security',
        'Industry-oriented program covering Network Security, Ethical Hacking, Penetration Testing, Digital Forensics, Malware Analysis, Kali Linux, SIEM Tools, Incident Response, and Cyber Laws.'
    ),

    (
        'Advanced Python Programming', 'APP', '6 Months',
        'Basic knowledge of programming or Python fundamentals.',
        35000, 80, 'School of Computing Sciences',
        'Professional certification focusing on Advanced Python, Object-Oriented Programming, Automation, APIs, Django, Flask, Data Analysis, Web Scraping, Multithreading, and AI application development.'
    ),

    (
        'Full Stack Development', 'FSD', '6 Months',
        'Basic understanding of HTML, CSS and programming fundamentals.',
        45000, 100, 'School of Computing Sciences',
        'Hands-on program covering HTML5, CSS3, JavaScript, Bootstrap, React.js, Node.js, Express.js, REST APIs, MongoDB, SQL Databases, Git, Docker, Deployment, and modern full-stack application development.'
    ),

    (
        'Cyber Security & Ethical Hacking (Advanced)', 'CSEH-ADV', '1 Year',
        'Graduation or Diploma in Computer Science/IT or equivalent knowledge.',
        95000, 60, 'School of Cyber Security',
        'Advanced specialization in Ethical Hacking, Red Teaming, Blue Teaming, Penetration Testing, Cloud Security, Threat Intelligence, Security Operations Center (SOC), Digital Forensics, and Vulnerability Assessment.'
    )
]
    
    cursor.executemany('''
    INSERT INTO courses (course_name, course_code, duration, eligibility, fees, seats, department, description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', courses_data)
    
    # Seed Dynamic Institutional Bulletins
    news_data = [
        (
            'Global Synergy: MIUTM Signs Strategic Research MOU with Silicon Valley Labs', 'Academic Exchange', 
            'Maurya International University of Technology & Management has signed a landmark international research agreement focusing on quantum computing frameworks and scalable edge solutions.', 
            'July 05, 2026'
        ),
        (
            'Placement Excellence 2026: Institutional Record Shattered with 94.2% Early Offers', 'Corporate Relations', 
            'The Department of Training & Placement proudly registers an exceptional phase-1 recruitment campaign, yielding unprecedented packages from elite Fortune 500 corporations.', 
            'July 12, 2026'
        ),
        (
            'Research Grant: Government Allocates Funding for Advanced AI and Sustainability Cell', 'Research & Development', 
            'The National Science & Innovation Council has approved a major research grant targeting the engineering of smart-grid automation models led by our core faculty blocks.', 
            'July 18, 2026'
        )
    ]
    
    cursor.executemany('INSERT INTO news_events (title, category, description, publish_date) VALUES (?, ?, ?, ?)', news_data)
    
    # Seed Full Faculty Infrastructure
    faculty_data = [
        ('Dr. Arindam Chaudhury', 'Senior Professor & Dean', 'School of Engineering & Applied Technology', 'Distributed Systems & Neural Networks', 'a.chaudhury@miutm.edu.in'),
        ('Prof. Sarah Mathew', 'Head of Department', 'School of Management Studies', 'Strategic Global Marketing & Corporate Valuation', 's.mathew@miutm.edu.in'),
        ('Dr. Rajeev N. Verma', 'Director of Research', 'School of Computing Sciences', 'Cryptographic Protocols & Blockchain Architecture', 'r.verma@miutm.edu.in'),
        ('Dr. Elena Rostova', 'Associate Professor', 'School of Engineering & Applied Technology', 'Stochastic Optimization & Quantum Physics Models', 'e.rostova@miutm.edu.in')
    ]
    
    cursor.executemany('INSERT INTO faculty (name, designation, department, specialization, email) VALUES (?, ?, ?, ?, ?)', faculty_data)
    
    connection.commit()
    connection.close()
    print("[✔] Production database generated and verified successfully.")

if __name__ == '__main__':
    initialize_production_database()