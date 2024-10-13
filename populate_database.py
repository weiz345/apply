import os
import sqlite3

def read_files_from_folder(folder_path):
    documents = []
    filenames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
                filenames.append(filename)
    return documents, filenames

def create_database():
    conn = sqlite3.connect('resumes_postings.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_into_database(table_name, filenames, documents):
    conn = sqlite3.connect('resumes_postings.db')
    cursor = conn.cursor()

    for filename, content in zip(filenames, documents):
        cursor.execute(f'''
            INSERT INTO {table_name} (filename, content)
            VALUES (?, ?)
        ''', (filename, content))

    conn.commit()
    conn.close()

def main():
    # Paths to the folders containing resumes and job postings
    resume_folder = 'gen_res'
    posting_folder = 'gen_posting'

    # Read resumes and job postings
    resumes, resume_filenames = read_files_from_folder(resume_folder)
    postings, posting_filenames = read_files_from_folder(posting_folder)

    # Create the database and tables
    create_database()

    # Insert resumes into the database
    insert_into_database('resumes', resume_filenames, resumes)

    # Insert postings into the database
    insert_into_database('postings', posting_filenames, postings)

    print("Database 'resumes_postings.db' has been populated with resumes and job postings.")

if __name__ == '__main__':
    main()
