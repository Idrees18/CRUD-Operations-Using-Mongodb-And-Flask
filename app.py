from datetime import datetime
from bson import ObjectId
from flask import Flask, redirect, render_template
from pymongo import MongoClient
from flask import request

app = Flask(__name__)

client = MongoClient("mongodb+srv://Idrees:idrees@mongodb-crud.irnsp.mongodb.net/test")
db = client["Prescriptiondatabase"]  # or db = client.test_database
collection = db["prescriptions"]  # or collection = db.test_collection$

#routing the home page 
@app.route("/")
def hello_world():
    return render_template("index.html")

#create function and route to add data
@app.route("/create", methods=["POST"])
def create():
    data = {}
    data["Patientkey"] = request.form["Patient_key"]
    data["Prescriptionnumber"] = request.form["Prescription_Number"]
    data["Date"] = request.form["Date"]
    data["Doctorname"] = request.form["Doctorname"]
    data["Prescription"] = request.form["Prescription"]
    collection.insert_one(data)
    return render_template("index1.html", text="Prescription Added Successfully")

#read the data
@app.route("/read", methods=["GET", "POST"])
def read():
    display = collection.find()
    display1 = collection.find()
    emp = list(display1)
    return render_template("read.html", collection=display, t=emp)

#delete the data
@app.route("/delete")
def delete():
    key = request.values.get("_id")
    collection.delete_one({"_id": ObjectId(key)})
    return redirect("/read")

#update the data
@app.route("/update", methods=["GET", "POST"])
def update():
    global id
    id = request.values.get("_id")
    task = collection.find({"_id": ObjectId(id)})
    return render_template("update.html", tasks=task)

#update form 
@app.route("/updating", methods=["GET", "POST"])
def updating():
    updateDoctorname = request.form["updateDoctorname"]
    Prescription = request.form["Prescription"]
    Updatedate = datetime.today()
    collection.update_one({"_id": ObjectId(id)}, {'$set': {"updateDoctorname": updateDoctorname, "Prescription": Prescription, "Updateddate": Updatedate}})
    return render_template("updatesucessfull.html", text1="Updated Sucessfully")

#search the data using the patient key
@app.route("/prescriptionslist", methods=["GET", "POST"])
def prescriptionslist():
    searchquery = request.form["search"]
    result = collection.find({"Patientkey": searchquery})
    emp1 = list(result)
    return render_template("search.html", collection=emp1, a=emp1)


if __name__ == "__main__":
    app.run(debug=True)
