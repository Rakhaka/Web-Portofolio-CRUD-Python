from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

# Konfigurasi database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)


@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mahasiswa")
    data_mahasiswa = cursor.fetchall()
    return render_template('index.html', data_mahasiswa=data_mahasiswa)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']

        cursor = db.cursor()
        cursor.execute("INSERT INTO mahasiswa (nama, nim, jurusan) VALUES (%s, %s, %s)", (nama, nim, jurusan))
        db.commit()

        return redirect(url_for('index'))
    
    return render_template('tambah.html')

@app.route('/ubah/<int:id>', methods=['GET', 'POST'])
def ubah(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mahasiswa WHERE id=%s", (id,))
    mahasiswa = cursor.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']
        nim = request.form['nim']
        jurusan = request.form['jurusan']

        cursor.execute("UPDATE mahasiswa SET nama=%s, nim=%s, jurusan=%s WHERE id=%s", (nama, nim, jurusan, id)) 
        db.commit()

        return redirect(url_for('index'))
    
    return render_template('ubah.html', mahasiswa=mahasiswa)

@app.route('/hapus/<int:id>')
def hapus(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM mahasiswa WHERE id=%s", (id,))
    db.commit()

    return redirect(url_for('index'))


if __name__ == '_name_':
    app.run(debug=True)