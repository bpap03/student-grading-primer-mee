from flask import Flask, jsonify, request
from flask_cors import CORS


import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    #If it is empty it will return a blank json file
    try:
        allStudentDict = db.get_all_students()
        return jsonify(allStudentDict), 200
    except:
        #If there is an issue witht he data base/ autehnication or smth else it will show an error
        return jsonify({"error" : "Couldnt't fetch da students"}), 404

    


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json
    
    #Remove traniling/ leading white spaces and check not empty
    name = student_data.get("name" or "").strip()
    course = student_data.get("course" or "").strip()
    mark = student_data.get("mark")

    if name and course:
        try:
            newStudent = db.insert_student(name, course, mark)
            return newStudent, 200
        except:
            return jsonify({"error" : "data valid but unable to insert student"}), 404    
    
    return jsonify({"error" : "either name or course was blank"}),404



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    #assuming that any int will be valid, inc neg and 0

    student_data = request.json
    try:
        student = db.update_student(student_id, student_data.get("name"), student_data.get("course"), student_data.get("mark"))
    except:
        return jsonify({"error" : "database was unable to pefrom action"}), 404 
    
    if student is None:
        return jsonify({"error" : "unable to find student by id"}), 404  
    
    return student, 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    
    try:
        student = db.get_student_by_id(student_id)
    except:
        return ({"error" : "database was unable to pefrom a search action"}), 404

    #Assuming that if you can't search for the student via get get_student_by_id then it won't be able to delte either
    if student is None:
        return jsonify({"error" : "unable to find student by id"}), 404
    
    try:
       db.delete_student(student_id)
       return student,200
    except:
        return jsonify({"error" : "database was unable to pefrom action"}), 404



@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students_list = db.get_all_students()
    except:
        return jsonify({"error" : "database was unable to get all students"}), 404
    
    if len(students_list) == 0:
        return jsonify({"count": 0, "average": 0, "min": None, "max": None}), 200
    
   
    #edge case no marks entered yet
    marks = [s["mark"] for s in  students_list if s.get("mark") is not None]
    if len(marks) == 0:
        return jsonify({"count": len(students_list), "average": 0, "min": None, "max": None}), 200

    stats = {
        "count" : len(marks),
        "average" : sum(marks) / len(marks),
        "min" : min(marks),
        "max" : max(marks),
    }
    return jsonify(stats), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
