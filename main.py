from flask import Flask, abort
from flask_restful import Api, Resource
import datetime
import pymongo
from pymongo import MongoClient
from Email import *


Username = "Musa"  # Username for Online MongoDB
Password = "1234"  # Password for Online MongoDB
GateID = "2345"

Online_Data_Base_URL = (
    "mongodb+srv://"
    + Username
    + ":"
    + Password
    + "@cluster0-ifrbh.mongodb.net/MIM?retryWrites=true&w=majority"
)

app = Flask(__name__)

api = Api(app)  # Wrapping App


class GetUsers(Resource):
    def get(self, email):
        json = ""
        cluster = MongoClient(Online_Data_Base_URL)  # Online DataBase is Accesed
        db = cluster[
            "MIM"
        ]  # Online Cluster is Accessed Name Should be Changed Accordingly if Not Changed it will auto create new one with this name
        coll = db.UsersInfo  # Acessing this DataBase Collection
        x = coll.find({"Email": email})  # Email is found
        for i in x:  # For loop to Extract Load Data
            json = {
                "Name": i["Name"],
                "Credits": i["Credits"],
            }  # Json Is Made to Send Data that is Requested
        if json == "":  # If no User is Found Json is empty so 404 Abort is Called
            abort(404, description="Resource not found")
        return json  # Return the Json Form Data


class AddUsers(Resource):
    def get(self, email, name, contact, role):
        if role == "donor":  # Check What Role is it for
            num = 0  # Num to check that wheather user was already registered or not
            cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
            db = cluster["MIM"]  # DataBase Accessed
            coll = db.UsersInfo  # UserInfo is Accessed
            x = coll.find({"Email": email})  # Email Information is Checked
            for i in x:  # Check any User Present
                num += 1  # If Present num Incremented
            if (
                num == 0
            ):  # If num is 0 Then New Json will be Formed with Information Provided
                json = {
                    "Name": name,
                    "Email": email,
                    "Credits": 0,
                    "Contact_no": contact,
                    "Role": "donor",
                }
                coll.insert(json)  # Json is Posted to DB
                return {
                    "message": "Succesfull"
                }  # Message is Returned Showing Connection Succesfull
            else:
                return {
                    "Exception": "User is Present"
                }  # Exception is Returned User is Present
        else:
            return {
                "Exception": "Are you trying to break in?"
            }  # Warning is Returned Hacking is Being Done


class EditContact(Resource):
    def get(self, contact, email, role):
        myquery = {"Email": email}
        newvalues = {"$set": {"Contact_no": contact}}
        if role == "donor":  # Check What Role is it for
            cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
            db = cluster["MIM"]  # DataBase Accessed
            coll = db.UsersInfo  # UserInfo is Accessed
            coll.update_one(myquery, newvalues)
            return {"message": "Succesfull"}
        else:
            return {"Exception": "Error Updating"}


class EditName(Resource):
    def get(self, name, email, role):
        myquery = {"Email": email}
        newvalues = {"$set": {"Name": name}}
        if role == "donor":  # Check What Role is it for
            cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
            db = cluster["MIM"]  # DataBase Accessed
            coll = db.UsersInfo  # UserInfo is Accessed
            coll.update_one(myquery, newvalues)
            return {"message": "Succesfull"}
        else:
            return {"Exception": "Error Updating"}


class EditAddress(Resource):
    def get(self, address, email, role):
        myquery = {"Email": email}
        newvalues = {"$set": {"Address": address}}
        if role == "donor":  # Check What Role is it for
            cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
            db = cluster["MIM"]  # DataBase Accessed
            coll = db.UsersInfo  # UserInfo is Accessed
            coll.update_one(myquery, newvalues)
            return {"message": "Succesfull"}
        else:
            return {"Exception": "Error Updating"}


class Payment(Resource):
    def get(self, payment, email, role, inarea, via):
        myquery = {"Email": email}
        if role == "donor":  # Check What Role is it for
            cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
            db = cluster["MIM"]  # DataBase Accessed
            coll = db.UsersInfo  # UserInfo is Accessed
            x = coll.find({"Email": email})
            previous = 0
            name = ""
            for i in x:
                previous = i["Credits"]
                name = i["Name"]
            previous += payment
            newvalues = {"$set": {"Credits": previous}}
            coll.update_one(myquery, newvalues)
            time = datetime.datetime.now()
            time = str(time)
            json = {
                "Donation in": inarea,
                "Amount": payment,
                "Time": time,
                "Checksum": "x_ABgaji182XUqi9_qi8",
                "Method": via,
                "User": name,
            }
            cluster = MongoClient(Online_Data_Base_URL)
            db = cluster["MIM_USERS_DONATION"]
            coll = db[name]
            coll.insert_one(json)
            SuccessfulDonation(email, name, payment, inarea)
            return {"message": "Succesfull"}
        else:
            return {"Exception": "Error Updating"}


class DataCharts(Resource):
    def get(self, email):
        cluster = MongoClient(Online_Data_Base_URL)  # Connection to DB
        db = cluster["MIM"]  # DataBase Accessed
        coll = db.UsersInfo  # UserInfo is Accessed
        x = coll.find({"Email": email})
        name = ""
        for i in x:
            name = i["Name"]
        db = cluster["MIM_USERS_DONATION"]
        coll = db[name]
        x = coll.find({"User": name})
        # -----------------------------------------------------
        School = 0
        Hospital = 0
        Food = 0
        Poverty = 0
        Water = 0
        Energy = 0
        Employment = 0
        Environment = 0
        Peace = 0
        Disability = 0
        Absue = 0
        Emergency = 0
        Sum = 0
        Total = 0
        # -----------------------------------------------------
        for i in x:
            if i["Donation in"] == "Education":
                School += 1
            if i["Donation in"] == "Hospital":
                Hospital += 1
            if i["Donation in"] == "Food":
                Food += 1
            if i["Donation in"] == "Poverty":
                Poverty += 1
            if i["Donation in"] == "Water":
                Water += 1
            if i["Donation in"] == "Energy":
                Energy += 1
            if i["Donation in"] == "Employment":
                Employment += 1
            if i["Donation in"] == "Environment":
                Environment += 1
            if i["Donation in"] == "Peace":
                Peace += 1
            if i["Donation in"] == "Disability":
                Disability += 1
            if i["Donation in"] == "Abuse":
                Abuse += 1
            if i["Donation in"] == "Emergency":
                Emergency += 1
            Total += 1
            Sum += i["Amount"]
        json = {
            "Education": School,
            "Hospital": Hospital,
            "Food": Food,
            "Poverty": Poverty,
            "Water": Water,
            "Energy": Energy,
            "Employment": Employment,
            "Environment": Environment,
            "Peace": Peace,
            "Disability": Disability,
            "Abuse": Absue,
            "Emergency": Emergency,
            "Sum": Sum,
            "Total": Total,
        }
        return json


api.add_resource(GetUsers, "/" + GateID + "/<string:email>")
api.add_resource(
    AddUsers,
    "/" + GateID + "/<string:email>/<string:name>/<string:contact>/<string:role>",
)
api.add_resource(
    EditContact,
    "/" + GateID + "/<string:email>/<string:contact>/<string:role>/contact",
)
api.add_resource(
    EditName, "/" + GateID + "/<string:email>/<string:name>/<string:role>/name",
)
api.add_resource(
    EditAddress,
    "/" + GateID + "/<string:email>/<string:address>/<string:role>/address",
)
api.add_resource(
    Payment,
    "/"
    + GateID
    + "/<string:email>/<int:payment>/<string:inarea>/<string:via>/<string:role>/payment",
)
api.add_resource(
    DataCharts, "/" + GateID + "/<string:email>/charts",
)

if __name__ == "__main__":
    app.run(debug=True)

