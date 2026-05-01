from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# 🔌 CONNECT TO YOUR DATABASE
conn = psycopg2.connect(
    database="trinity_db",   # change if needed
    user="postgres",
    password="Zen2928@",
    host="localhost",
    port="5432"
)

# 🏠 DASHBOARD
@app.route('/')
def dashboard():
    return render_template("index.html")


# 👥 RESIDENTS PAGE
@app.route('/residents')
def residents():
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        h.house_no,
        h.wing,
        COUNT(r.resident_id),
        MAX(CASE 
            WHEN r.role IN ('owner','secretary','cashier','member') 
            THEN r.name 
        END)
    FROM House h
    LEFT JOIN Resident r 
    ON h.house_no = r.house_no
    GROUP BY h.house_no, h.wing
    ORDER BY h.wing, h.house_no;
    """)

    flats = cur.fetchall()

    return render_template("residents.html", flats=flats)


# 📄 DETAILS PAGE
@app.route('/details/<house>')
def details(house):
    cur = conn.cursor()

    cur.execute("""
    SELECT name, role 
    FROM Resident 
    WHERE house_no=%s
    """, (house,))

    members = cur.fetchall()

    return render_template("details.html",
                           house=house,
                           members=members)


# 👨‍👩‍👧 MEMBERS PAGE
@app.route('/members/<house>')
def members(house):
    cur = conn.cursor()

    cur.execute("""
    SELECT name, role 
    FROM Resident 
    WHERE house_no=%s
    """, (house,))

    members = cur.fetchall()

    return render_template("members.html",
                           house=house,
                           members=members)


app.run(debug=True)
