from flask import Flask,jsonify,render_template,request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

CORS(app) 

connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL server host
        user='root',  # Replace with your MySQL username
        password='Siva&guru17',  # Replace with your MySQL password
        database='World'  # Replace with your database name
)
cursor = connection.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/countryPage')
def HomePage():
    return render_template('country.html')

@app.route('/country')
def getAllPlayers():
    cursor.execute("select * from country join city on country.Code = city.Countrycode limit 100")
    rows = cursor.fetchall()
    return rows
@app.route('/country/<string:code>')
def getCountry(code):
    cursor.execute("SELECT * FROM country WHERE Code = %s", (code,)) 
    rows = cursor.fetchall()
    return rows


@app.route('/addMovie',methods=['POST'])
def addMovie():
    data=request.get_json(force=True)
    sql = "INSERT INTO TamilMovies (movie_id,movie_name) VALUES (%s, %s)"
    values = (data["id"],data["name"])
    cursor.execute(sql, values)
    connection.commit()
    return jsonify({"message": "Movie added successfully!"})

@app.route('/addedMovie/<string:movie_id>/<string:movie_name>')
def addedMovies(movie_id,movie_name):
    sql = "INSERT INTO TamilMovies (movie_id,movie_name) VALUES (%s,%s)"
    values = (movie_id,movie_name)
    cursor.execute(sql,values)
    connection.commit()
    return jsonify({"message": "Movie added successfully!"})
    

@app.route('/updateMovie/<int:movie_id>')
def updateMovie(movie_id):
    # sql = "Update TamilMovies set movie_name = %s where movie_id = %s"
    # values = ("Varisu",3)
    # cursor.execute(sql,values)
    # connection.commit()
    # return "Movie updated successfully"



    
    try:
        cursor.execute("select * from TamilMovies where movie_id=%s",(movie_id,))
        movie = cursor.fetchone()
        
        if not movie:
            return jsonify({"error": "Movie not found"})
        
        else:
                sql = "UPDATE TamilMovies SET movie_name = %s WHERE movie_id = %s"
                cursor.execute(sql, ('Sarkar',movie_id))
                connection.commit()
                return jsonify({"message": f"Movie with ID {movie_id} updated successfully"})
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Movie updated successfully", "movie_id": 3, "new_name": "Varisu"})


@app.route('/deleteMovie/<int:movie_id>')
def delete_movie(movie_id):
    try:
        # Check if the movie exists before deleting
        cursor.execute("SELECT * FROM TamilMovies WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            return jsonify({"error": "Movie not found"}), 404  # If movie ID doesn't exist

        else:
            
            sql = "DELETE FROM TamilMovies WHERE movie_id = %s"
            cursor.execute(sql, (movie_id,))
            connection.commit()

            return jsonify({"message": f"Movie with ID {movie_id} deleted successfully"})
        

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/updatedMovie')
def updatedMovie():
    try:
        cursor.execute("SELECT * FROM TamilMovies WHERE movie_id=%s",(movie_id,))
        movie = cursor.fetchone()
        
        if not movie:
            return jsonify({"error": "Movie not found"})
        
        else:
                sql = "UPDATE TamilMovies SET movie_name = %s WHERE movie_id = %s"
                cursor.execute(sql, (movie_name,movie_id))
                connection.commit()
                return jsonify({"message": f"Movie with ID {movie_id} updated successfully"})
        
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/delMovie/<int:movie_id>')
def delMovie(movie_id):
    try:
        # Check if the movie exists before deleting
        cursor.execute("SELECT * FROM TamilMovies WHERE movie_id = %s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            return jsonify({"message    ": "Movie not found"})  # If movie ID doesn't exist

        else:
            
            sql = "DELETE FROM TamilMovies WHERE movie_id = %s"
            cursor.execute(sql, (movie_id,))
            connection.commit()

            return jsonify({"message": f"Movie with ID {movie_id} deleted successfully"})
        

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

