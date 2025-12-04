from flask import Flask, render_template, jsonify, request
import mysql.connector
from datetime import datetime
import datetime as _datetime
from collections import defaultdict
import csv
import os
import random
import uuid

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def dump_table_to_csv(table_name, csv_filename):
    """Dump entire table to CSV file path under DATA_DIR."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        csv_path = os.path.join(DATA_DIR, csv_filename)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            for r in rows:
                writer.writerow(r)
        cursor.close()
        conn.close()
    except Exception:
        # don't interrupt main flow if CSV dump fails
        pass

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'library'
}

def get_connection():
    return mysql.connector.connect(**db_config)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response

# ==================== HOME ====================
@app.route('/')
def home():
    return render_template('library_management_frontend.html')

# ==================== BOOKS ====================
@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Books (title, isbn, genre, publisher_id, publication_year) VALUES (%s, %s, %s, %s, %s)",
            (data['title'], data.get('isbn', None), data['genre'], data['publisher_id'], data['publication_year'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Update a book
@app.route('/api/books/<int:isbn>', methods=['PUT'])
def update_book(isbn):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Books SET title=%s, publisher_id=%s, publication_year=%s, genre=%s WHERE isbn=%s",
            (data.get('title'), data.get('publisher_id'), data.get('publication_year'), data.get('genre'), isbn)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book updated', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete a book
@app.route('/api/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE isbn=%s", (isbn,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book deleted', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MEMBERS ====================
@app.route('/api/members', methods=['GET'])
def get_members():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Members")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert date objects to strings
        for member in data:
            if 'date_registered' in member and member['date_registered']:
                member['date_registered'] = str(member['date_registered'])
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members', methods=['POST'])
def add_member():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Members (first_name, last_name, email, address, phone, date_registered) VALUES (%s, %s, %s, %s, %s, CURDATE())",
            (data['first_name'], data['last_name'], data['email'], data['address'], data['phone'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Member added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Update member
@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Members SET first_name=%s, last_name=%s, email=%s, address=%s, phone=%s WHERE member_id=%s",
            (data.get('first_name'), data.get('last_name'), data.get('email'), data.get('address'), data.get('phone'), member_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Member updated', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete member
@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE member_id=%s", (member_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Member deleted', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== LOANS ====================
@app.route('/api/loans', methods=['GET'])
def get_loans():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Loans")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert date objects to strings
        for loan in data:
            for date_field in ['issue_date', 'due_date', 'return_date']:
                if date_field in loan and loan[date_field]:
                    loan[date_field] = str(loan[date_field])
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/loans', methods=['POST'])
def add_loan():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        # Insert loan (include fine_amount if provided). Sanitize fine_amount from frontend.
        fine_amount = data.get('fine_amount')
        if fine_amount is None or fine_amount == '':
            fine_amount = None
        else:
            # try to convert to float for DB insertion; if fails, treat as None
            try:
                fine_amount = float(fine_amount)
            except Exception:
                fine_amount = None

        if fine_amount is not None:
            cursor.execute(
                "INSERT INTO Loans (copy_id, member_id, issue_date, due_date, fine_amount) VALUES (%s, %s, %s, %s, %s)",
                (data['copy_id'], data['member_id'], data['issue_date'], data['due_date'], fine_amount)
            )
        else:
            cursor.execute(
                "INSERT INTO Loans (copy_id, member_id, issue_date, due_date) VALUES (%s, %s, %s, %s)",
                (data['copy_id'], data['member_id'], data['issue_date'], data['due_date'])
            )
        # Mark copy as On Loan
        cursor.execute(
            "UPDATE Book_Copies SET status = %s WHERE copy_id = %s",
            ('On Loan', data['copy_id'])
        )
        conn.commit()
        # Dump CSVs for Loans and Book_Copies to keep CSV entities updated
        try:
            dump_table_to_csv('Loans', 'loans.csv')
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Loan created successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Update loan
@app.route('/api/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Loans SET copy_id=%s, member_id=%s, issue_date=%s, due_date=%s, return_date=%s, fine_amount=%s WHERE loan_id=%s",
            (data.get('copy_id'), data.get('member_id'), data.get('issue_date'), data.get('due_date'), data.get('return_date'), data.get('fine_amount'), loan_id)
        )
        # If return_date is provided, update copy status back to Available
        if data.get('return_date'):
            cursor.execute("UPDATE Book_Copies SET status=%s WHERE copy_id=%s", ('Available', data.get('copy_id')))
        conn.commit()
        # update CSVs
        try:
            dump_table_to_csv('Loans', 'loans.csv')
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Loan updated', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete loan
@app.route('/api/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        # find loan to get copy_id
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT copy_id FROM Loans WHERE loan_id=%s", (loan_id,))
        row = cursor.fetchone()
        copy_id = row.get('copy_id') if row else None
        cursor.close()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Loans WHERE loan_id=%s", (loan_id,))
        # set copy to Available if it existed
        if copy_id:
            cursor.execute("UPDATE Book_Copies SET status=%s WHERE copy_id=%s", ('Available', copy_id))
        conn.commit()
        try:
            dump_table_to_csv('Loans', 'loans.csv')
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Loan deleted', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BOOK COPIES ====================
@app.route('/api/copies', methods=['GET'])
def get_copies():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Book_Copies")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/copies', methods=['POST'])
def add_copy():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Book_Copies (isbn, branch_id, status) VALUES (%s, %s, %s)",
            (data.get('isbn'), data.get('branch_id'), data.get('status', 'Available'))
        )
        conn.commit()
        try:
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Copy added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Edit a copy
@app.route('/api/copies/<int:copy_id>', methods=['PUT'])
def update_copy(copy_id):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Book_Copies SET isbn=%s, branch_id=%s, status=%s WHERE copy_id=%s",
            (data.get('isbn'), data.get('branch_id'), data.get('status'), copy_id)
        )
        conn.commit()
        try:
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Copy updated', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete a copy
@app.route('/api/copies/<int:copy_id>', methods=['DELETE'])
def delete_copy(copy_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Book_Copies WHERE copy_id=%s", (copy_id,))
        conn.commit()
        try:
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'message': 'Copy deleted', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BRANCHES ====================
@app.route('/api/branches', methods=['GET'])
def get_branches():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Library_Branches")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/branches', methods=['POST'])
def add_branch():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Library_Branches (name, location) VALUES (%s, %s)",
            (data['branch_name'], data['location'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Branch added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PUBLISHERS ====================
@app.route('/api/publishers', methods=['GET'])
def get_publishers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Publishers")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/publishers', methods=['POST'])
def add_publisher():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Publishers (name, address, phone) VALUES (%s, %s, %s)",
            (data['publisher_name'], data['address'], data['phone'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Publisher added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== BULK DELETE ENDPOINTS ====================
@app.route('/api/books/bulk_delete', methods=['POST'])
def bulk_delete_books():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # delete dependent rows: Loans -> Book_Copies -> Book_Authors -> Books
        # 1) Find copies for these books
        cursor.execute(f"SELECT copy_id FROM Book_Copies WHERE isbn IN ({placeholders})", tuple(ids))
        copy_rows = cursor.fetchall()
        copy_ids = [r[0] for r in copy_rows if r]
        if copy_ids:
            ph_c = ','.join(['%s'] * len(copy_ids))
            cursor.execute(f"DELETE FROM Loans WHERE copy_id IN ({ph_c})", tuple(copy_ids))
            cursor.execute(f"DELETE FROM Book_Copies WHERE copy_id IN ({ph_c})", tuple(copy_ids))
        # delete book_authors
        cursor.execute(f"DELETE FROM Book_Authors WHERE isbn IN ({placeholders})", tuple(ids))
        # finally delete books
        cursor.execute(f"DELETE FROM Books WHERE isbn IN ({placeholders})", tuple(ids))
        conn.commit()
        try:
            dump_table_to_csv('Books', 'books.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/members/bulk_delete', methods=['POST'])
def bulk_delete_members():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # delete dependent loans first
        cursor.execute(f"DELETE FROM Loans WHERE member_id IN ({placeholders})", tuple(ids))
        cursor.execute(f"DELETE FROM Members WHERE member_id IN ({placeholders})", tuple(ids))
        conn.commit()
        try:
            dump_table_to_csv('Members', 'members.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/loans/bulk_delete', methods=['POST'])
def bulk_delete_loans():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        # collect copy_ids for loans to set copies available
        placeholders = ','.join(['%s'] * len(ids))
        cursor.execute(f"SELECT copy_id FROM Loans WHERE loan_id IN ({placeholders})", tuple(ids))
        rows = cursor.fetchall()
        copy_ids = [r[0] for r in rows if r]
        # delete loans
        cursor.execute(f"DELETE FROM Loans WHERE loan_id IN ({placeholders})", tuple(ids))
        if copy_ids:
            ph = ','.join(['%s'] * len(copy_ids))
            # set copies to Available
            cursor.execute(f"UPDATE Book_Copies SET status=%s WHERE copy_id IN ({ph})", tuple(['Available'] + copy_ids))
        conn.commit()
        try:
            dump_table_to_csv('Loans', 'loans.csv')
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/copies/bulk_delete', methods=['POST'])
def bulk_delete_copies():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # delete loans referencing these copies first
        cursor.execute(f"DELETE FROM Loans WHERE copy_id IN ({placeholders})", tuple(ids))
        cursor.execute(f"DELETE FROM Book_Copies WHERE copy_id IN ({placeholders})", tuple(ids))
        conn.commit()
        try:
            dump_table_to_csv('Book_Copies', 'copies.csv')
        except Exception:
            pass
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/branches/bulk_delete', methods=['POST'])
def bulk_delete_branches():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # find copies in these branches and delete loans, then copies
        cursor.execute(f"SELECT copy_id FROM Book_Copies WHERE branch_id IN ({placeholders})", tuple(ids))
        rows = cursor.fetchall()
        copy_ids = [r[0] for r in rows if r]
        if copy_ids:
            ph = ','.join(['%s'] * len(copy_ids))
            cursor.execute(f"DELETE FROM Loans WHERE copy_id IN ({ph})", tuple(copy_ids))
            cursor.execute(f"DELETE FROM Book_Copies WHERE copy_id IN ({ph})", tuple(copy_ids))
        cursor.execute(f"DELETE FROM Library_Branches WHERE branch_id IN ({placeholders})", tuple(ids))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/publishers/bulk_delete', methods=['POST'])
def bulk_delete_publishers():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # find books for these publishers and cascade delete similar to books endpoint
        cursor.execute(f"SELECT isbn FROM Books WHERE publisher_id IN ({placeholders})", tuple(ids))
        rows = cursor.fetchall()
        isbns = [r[0] for r in rows if r]
        if isbns:
            ph_b = ','.join(['%s'] * len(isbns))
            # delete loans for copies of these books
            cursor.execute(f"SELECT copy_id FROM Book_Copies WHERE isbn IN ({ph_b})", tuple(isbns))
            copy_rows = cursor.fetchall()
            copy_ids = [r[0] for r in copy_rows if r]
            if copy_ids:
                ph_c = ','.join(['%s'] * len(copy_ids))
                cursor.execute(f"DELETE FROM Loans WHERE copy_id IN ({ph_c})", tuple(copy_ids))
                cursor.execute(f"DELETE FROM Book_Copies WHERE copy_id IN ({ph_c})", tuple(copy_ids))
            cursor.execute(f"DELETE FROM Book_Authors WHERE isbn IN ({ph_b})", tuple(isbns))
            cursor.execute(f"DELETE FROM Books WHERE isbn IN ({ph_b})", tuple(isbns))
        # finally delete publishers
        cursor.execute(f"DELETE FROM Publishers WHERE publisher_id IN ({placeholders})", tuple(ids))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/authors/bulk_delete', methods=['POST'])
def bulk_delete_authors():
    try:
        data = request.json or {}
        ids = data.get('ids') or []
        if not ids:
            return jsonify({'error': 'No ids provided'}), 400
        conn = get_connection()
        cursor = conn.cursor()
        placeholders = ','.join(['%s'] * len(ids))
        # delete book_author links first
        cursor.execute(f"DELETE FROM Book_Authors WHERE author_id IN ({placeholders})", tuple(ids))
        cursor.execute(f"DELETE FROM Authors WHERE author_id IN ({placeholders})", tuple(ids))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'deleted': len(ids)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== AUTHORS ====================
@app.route('/api/authors', methods=['GET'])
def get_authors():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Authors")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/authors', methods=['POST'])
def add_author():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Authors (first_name, last_name) VALUES (%s, %s)",
            (data['first_name'], data['last_name'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Author added successfully', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== SEED / SAMPLE DATA ====================
@app.route('/api/seed', methods=['POST'])
def seed_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        inserted = {'publishers': 0, 'authors': 0, 'books': 0, 'branches': 0, 'members': 0, 'copies': 0, 'loans': 0}

        # helper to check existence
        def exists(query, params=()):
            cursor.execute(query, params)
            row = cursor.fetchone()
            if not row:
                return False
            # if row is a tuple with count
            try:
                return int(row[0]) > 0
            except Exception:
                return True

        # Generate unique publisher names
        for _ in range(3):
            name = f"Publisher {uuid.uuid4().hex[:8]}"
            if not exists("SELECT COUNT(*) FROM Publishers WHERE name=%s", (name,)):
                cursor.execute("INSERT INTO Publishers (name, address, phone) VALUES (%s, %s, %s)", (name, f"{random.randint(1,999)} Publisher Rd", f"555-{random.randint(1000,9999)}"))
                inserted['publishers'] += 1

        # Generate unique authors
        first_names = ['Oliver','Emma','Liam','Ava','Noah','Sophia','Mason','Isabella']
        last_names = ['Brown','Wilson','Taylor','Anderson','Thomas','Moore','Martin','Lee']
        for _ in range(6):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            if not exists("SELECT COUNT(*) FROM Authors WHERE first_name=%s AND last_name=%s", (fn, ln)):
                cursor.execute("INSERT INTO Authors (first_name, last_name) VALUES (%s, %s)", (fn, ln))
                inserted['authors'] += 1

        # Ensure there are at least a couple of branches
        for bname in [f"Branch {uuid.uuid4().hex[:6]}", f"Branch {uuid.uuid4().hex[6:12]}"]:
            if not exists("SELECT COUNT(*) FROM Library_Branches WHERE name=%s", (bname,)):
                cursor.execute("INSERT INTO Library_Branches (name, location) VALUES (%s, %s)", (bname, 'Local'))
                inserted['branches'] += 1

        # Generate unique members
        for _ in range(6):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            email = f"{fn.lower()}.{ln.lower()}.{uuid.uuid4().hex[:6]}@example.com"
            if not exists("SELECT COUNT(*) FROM Members WHERE email=%s", (email,)):
                cursor.execute("INSERT INTO Members (first_name, last_name, email, address, phone, date_registered) VALUES (%s, %s, %s, %s, %s, CURDATE())",
                               (fn, ln, email, f"{random.randint(1,999)} Seed St", f"555-{random.randint(1000,9999)}"))
                inserted['members'] += 1

        # Fetch publisher ids to attach to books
        cursor.execute("SELECT publisher_id FROM Publishers")
        publishers = [r[0] for r in cursor.fetchall()]
        if not publishers:
            publishers = [1]

        genres = ['Fiction','Science','History','Mystery','Romance','Non-Fiction']
        # Generate unique books
        for _ in range(8):
            # Use ISBN values within signed 32-bit integer range to avoid overflow in INT columns
            isbn = random.randint(1000000000, 2147483646)
            if not exists("SELECT COUNT(*) FROM Books WHERE isbn=%s", (isbn,)):
                title = f"Book {uuid.uuid4().hex[:6]}"
                genre = random.choice(genres)
                pub_id = random.choice(publishers)
                year = random.randint(1990, 2024)
                try:
                    cursor.execute("INSERT INTO Books (title, isbn, genre, publisher_id, publication_year) VALUES (%s, %s, %s, %s, %s)",
                                   (title, isbn, genre, pub_id, year))
                    inserted['books'] += 1
                except mysql.connector.IntegrityError:
                    # skip any primary key conflicts or other integrity issues
                    continue

        # Create copies for random books at random branches
        cursor.execute("SELECT isbn FROM Books")
        book_isbns = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT branch_id FROM Library_Branches")
        branch_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(12):
            if not book_isbns or not branch_ids:
                break
            isbn = random.choice(book_isbns)
            branch_id = random.choice(branch_ids)
            # randomly include Reserved status sometimes
            status = random.choices(['Available', 'Reserved'], weights=[0.75, 0.25])[0]
            # Avoid duplicate identical copy records by checking same isbn+branch+status count
            if not exists("SELECT COUNT(*) FROM Book_Copies WHERE isbn=%s AND branch_id=%s AND status=%s", (isbn, branch_id, status)):
                cursor.execute("INSERT INTO Book_Copies (isbn, branch_id, status) VALUES (%s, %s, %s)", (isbn, branch_id, status))
                inserted['copies'] += 1

        # Create loans for some available copies
        cursor.execute("SELECT copy_id FROM Book_Copies WHERE status='Available'")
        available_copies = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT member_id FROM Members")
        member_ids = [r[0] for r in cursor.fetchall()]
        random.shuffle(available_copies)
        for copy_id in available_copies[:8]:
            if not member_ids:
                break
            member_id = random.choice(member_ids)
            # double-check copy still available
            if not exists("SELECT COUNT(*) FROM Book_Copies WHERE copy_id=%s AND status='Available'", (copy_id,)):
                continue
            # generate varied dates: issue_date in past 60 days
            days_back = random.randint(0, 60)
            issue_dt = _datetime.date.today() - _datetime.timedelta(days=days_back)
            loan_length = random.randint(7, 28)
            due_dt = issue_dt + _datetime.timedelta(days=loan_length)

            # decide if the loan was returned (some will be returned)
            returned = random.random() < 0.45
            return_dt = None
            fine_amount = None
            if returned:
                # return date could be between issue and issue+some days
                ret_offset = random.randint(1, max(1, loan_length + 12))
                return_dt = issue_dt + _datetime.timedelta(days=ret_offset)
                # compute fine if returned after due date
                if return_dt > due_dt:
                    days_late = (return_dt - due_dt).days
                    # fine between 0.5 and 2.0 per day
                    fine_amount = round(days_late * random.uniform(0.5, 2.0), 2)

            # prepare insert depending on return/fine
            if return_dt is not None and fine_amount is not None:
                cursor.execute("INSERT INTO Loans (copy_id, member_id, issue_date, due_date, return_date, fine_amount) VALUES (%s, %s, %s, %s, %s, %s)",
                               (copy_id, member_id, issue_dt.isoformat(), due_dt.isoformat(), return_dt.isoformat(), fine_amount))
            elif return_dt is not None:
                cursor.execute("INSERT INTO Loans (copy_id, member_id, issue_date, due_date, return_date) VALUES (%s, %s, %s, %s, %s)",
                               (copy_id, member_id, issue_dt.isoformat(), due_dt.isoformat(), return_dt.isoformat()))
            else:
                cursor.execute("INSERT INTO Loans (copy_id, member_id, issue_date, due_date) VALUES (%s, %s, %s, %s)",
                               (copy_id, member_id, issue_dt.isoformat(), due_dt.isoformat()))

            inserted['loans'] += 1

            # update copy status: if returned -> Available, else -> On Loan
            new_status = 'Available' if return_dt is not None else 'On Loan'
            cursor.execute("UPDATE Book_Copies SET status=%s WHERE copy_id=%s", (new_status, copy_id))

        conn.commit()

        # Dump CSVs for relevant tables
        try:
            dump_table_to_csv('Books', 'books.csv')
            dump_table_to_csv('Book_Copies', 'copies.csv')
            dump_table_to_csv('Loans', 'loans.csv')
            dump_table_to_csv('Members', 'members.csv')
        except Exception:
            pass

        cursor.close()
        conn.close()
        return jsonify({'message': 'Seed completed', 'inserted': inserted}), 201
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        return jsonify({'error': str(e)}), 500

# ==================== DASHBOARD / ANALYTICS ====================
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Basic counts
        cursor.execute("SELECT COUNT(*) AS total_books FROM Books")
        total_books = cursor.fetchone().get('total_books', 0)

        cursor.execute("SELECT COUNT(*) AS available_copies FROM Book_Copies WHERE status='Available'")
        available_copies = cursor.fetchone().get('available_copies', 0)

        cursor.execute("SELECT COUNT(*) AS books_on_loan FROM Book_Copies WHERE status='On Loan'")
        books_on_loan = cursor.fetchone().get('books_on_loan', 0)

        cursor.execute("SELECT COUNT(*) AS reserved_copies FROM Book_Copies WHERE status='Reserved'")
        reserved_copies = cursor.fetchone().get('reserved_copies', 0)

        cursor.execute("SELECT COUNT(*) AS active_members FROM Members")
        active_members = cursor.fetchone().get('active_members', 0)

        # Status distribution
        cursor.execute("SELECT status, COUNT(*) as cnt FROM Book_Copies GROUP BY status")
        status_rows = cursor.fetchall()
        status_dist = {row['status']: row['cnt'] for row in status_rows}

        # Loans trend - last 6 weeks (weekly buckets)
        weeks_back = 6
        today = _datetime.date.today()
        # Determine week start (Monday) for current week
        current_monday = today - _datetime.timedelta(days=today.weekday())
        week_labels = []
        week_starts = []
        for i in range(weeks_back, 0, -1):
            wk_start = current_monday - _datetime.timedelta(weeks=(i-1))
            week_starts.append(wk_start)
            week_labels.append(wk_start.strftime('%Y-%m-%d'))

        # initialize counts
        week_counts = [0] * weeks_back

        cursor.execute("SELECT issue_date FROM Loans WHERE issue_date >= %s", (week_starts[0],))
        loan_rows = cursor.fetchall()
        for r in loan_rows:
            d = r.get('issue_date')
            if not d:
                continue
            if isinstance(d, _datetime.datetime):
                d = d.date()
            for idx, wk_start in enumerate(week_starts):
                if wk_start <= d < (wk_start + _datetime.timedelta(weeks=1)):
                    week_counts[idx] += 1
                    break

        # Top genres
        cursor.execute("SELECT genre, COUNT(*) as cnt FROM Books GROUP BY genre ORDER BY cnt DESC LIMIT 6")
        genre_rows = cursor.fetchall()
        genres = [r['genre'] or 'Unknown' for r in genre_rows]
        genre_counts = [r['cnt'] for r in genre_rows]

        cursor.close()
        conn.close()

        return jsonify({
            'counts': {
                'total_books': total_books,
                'available_copies': available_copies,
                'books_on_loan': books_on_loan,
                'reserved_copies': reserved_copies,
                'active_members': active_members
            },
            'status_distribution': status_dist,
            'loans_trend': {
                'labels': week_labels,
                'counts': week_counts
            },
            'top_genres': {
                'labels': genres,
                'counts': genre_counts
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)