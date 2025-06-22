from itertools import product, count
from dns.e164 import query
from flask import Flask, session, render_template, redirect, request
from flask_cors import CORS
import pymongo
import os
from datetime import datetime
from bson import ObjectId

App_root=os.path.dirname(os.path.abspath(__file__))
diet_plan_images_path=App_root+ "/" + "static/Diet_Plan_Images"

# MongoDB client setup...
my_client=pymongo.MongoClient("your-mongodb-connection-uri")
# ... rest of your Mongo setup ...

app=Flask(__name__)
app.secret_key="food_diet_nutrition"
CORS(app)  # <- Enable CORS for all routes

admin_username = "admin"
admin_password = "admin"

App_root=os.path.dirname(os.path.abspath(__file__))
diet_plan_images_path=App_root+ "/" + "static/Diet_Plan_Images"

from pymongo import MongoClient

import certifi
from pymongo import MongoClient

my_client = MongoClient(
    "mongodb+srv://nareshkurapati1399:XTM4YyAHvoI6pMt6@cluster0.kmhopuj.mongodb.net/?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile=certifi.where()
)

# Optional: test connection at startup
try:
    my_client.admin.command('ping')
    print("✅ MongoDB connection successful.")
except Exception as e:
    print("❌ MongoDB connection failed:", e)


my_database = my_client["Food_Diet_Nutrition"]

admin_collection=my_database["Admin"]
nutritionist_collection=my_database["Nutritionist"]
food_timings_collection=my_database["Food_Timings"]
food_in_diet_collection=my_database["Food_in_Diet"]
review_collection=my_database["Review"]
diet_plan_collection=my_database["Diet_Plan"]
user_food_collection=my_database["User_Food"]
users_collection=my_database["Users"]
payment_collection=my_database["Payments"]
exercise_timings_collection=my_database["Exercise_Timings"]
user_diet_collection=my_database["User_Diet"]
user_exercise_collection=my_database["User_Exercise"]
exercise_in_diet_collection=my_database["Exercise_in_Diet"]
exercise_type_collection = my_database["Exercise_Type"]
diet_for_collection = my_database["Diet_For"]

app=Flask(__name__)
app.secret_key="food_diet_nutrition"
admin_username = "admin"
admin_password = "admin"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/nutrition_home")
def nutrition_home():
    return render_template("nutrition_home.html")


@app.route("/user_home")
def user_home():
    return render_template("user_home.html")


@app.route("/admin_login_action", methods = ['post'])
def admin_login_action():
    username=request.form.get("username")
    password=request.form.get("password")
    if admin_username == username and admin_password == password :
        session['role'] = "Admin"
        return render_template("admin_home.html")
    else:
        return render_template("message.html", message = "Invalid Login Details")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/view_nutritionists")
def view_nutritionists():
    query={}
    nutritionists=nutritionist_collection.find(query)
    nutritionists=list(nutritionists)
    return render_template("view_nutritionists.html", nutritionists=nutritionists)


@app.route("/verify_nutritionist")
def verify_nutritionist():
    nutritionist_id = request.args.get("nutritionist_id")
    query={"$set": {"status":"verified"}}
    query1={"_id":ObjectId(nutritionist_id)}
    nutritionist_collection.update_one(query1, query)
    return redirect("/view_nutritionists")


@app.route("/unverify_nutritionist")
def unverify_nutritionist():
    nutritionist_id=request.args.get("nutritionist_id")
    query={"$set": {"status": "not verified"}}
    query1={"_id":ObjectId(nutritionist_id)}
    nutritionist_collection.update_one(query1, query)
    return redirect("/view_nutritionists")


@app.route("/view_diet_plans")
def view_diet_plans():
    if session['role']=="Admin":
        query = {}
        diet_plans = diet_plan_collection.find(query)
        diet_plans = list(diet_plans)
        query = {}
        food_timings = food_timings_collection.find(query)
        food_timings = list(food_timings)
        query = {}
        exercise_timings = exercise_timings_collection.find(query)
        exercise_timings = list(exercise_timings)
    elif session['role']=="Nutritionist":
        nutritionist_id=session['nutritionist_id']
        query={"nutritionist_id":ObjectId(nutritionist_id)}
        diet_plans = diet_plan_collection.find(query)
        diet_plans = list(diet_plans)
        query={}
        food_timings=food_timings_collection.find(query)
        food_timings=list(food_timings)
        query={}
        exercise_timings=exercise_timings_collection.find(query)
        exercise_timings=list(exercise_timings)
    elif session['role']=="user":
        query = {}
        diet_plans = diet_plan_collection.find(query)
        diet_plans = list(diet_plans)
        query = {}
        food_timings = food_timings_collection.find(query)
        food_timings = list(food_timings)
        query = {}
        exercise_timings = exercise_timings_collection.find(query)
        exercise_timings = list(exercise_timings)
    else:
        query = {}
        diet_plans = diet_plan_collection.find(query)
        diet_plans = list(diet_plans)
        query = {}
        food_timings = food_timings_collection.find(query)
        food_timings = list(food_timings)
        query = {}
        exercise_timings = exercise_timings_collection.find(query)
        exercise_timings = list(exercise_timings)
    return render_template("view_diet_plans.html", food_timings=food_timings, exercise_timings=exercise_timings, diet_plans=diet_plans, get_nutritionist_name_by_nutritionist_id=get_nutritionist_name_by_nutritionist_id, str=str)


@app.route("/verify_diet_plan")
def verify_diet_plan():
    diet_plan_id=request.args.get("diet_plan_id")
    query={"_id":ObjectId(diet_plan_id)}
    query1={"$set":{"status":"verified"}}
    diet_plan_collection.update_one(query, query1)
    return redirect("/view_diet_plans")


@app.route("/unverify_diet_plan")
def unverify_diet_plan():
    diet_plan_id=request.args.get("diet_plan_id")
    query = {"_id": ObjectId(diet_plan_id)}
    query1 = {"$set": {"status": "not verified"}}
    diet_plan_collection.update_one(query, query1)
    return redirect("/view_diet_plans")


@app.route("/nutrition_login")
def nutrition_login():
    return render_template("nutrition_login.html")


@app.route("/nutrition_login_action", methods=['post'])
def nutrition_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    query={"email":email, "password":password}
    count = nutritionist_collection.count_documents(query)
    if count>0:
        nutritionists = nutritionist_collection.find_one(query)
        if str(nutritionists['status']) == "verified":
            session['role']="Nutritionist"
            session['nutritionist_id'] = str(nutritionists['_id'])
            session['nutritionist_first_name'] = nutritionists['first_name']
            return render_template("nutrition_home.html")
        else:
            return render_template("message.html", message1="Nutritionist Not Verified")
    else:
        return render_template("message.html", message1="Invalid Login Details")


@app.route("/nutrition_registration")
def nutrition_registration():
    return render_template("nutrition_registration.html")


@app.route("/nutrition_registration_action", methods=['post'])
def nutrition_registration_action():
    first_name=request.form.get("first_name")
    last_name=request.form.get("last_name")
    email=request.form.get("email")
    phone=request.form.get("phone")
    password=request.form.get("password")
    confirm_password=request.form.get("confirm_password")
    address=request.form.get("address")
    state=request.form.get("state")
    city=request.form.get("city")
    zipcode=request.form.get("zipcode")
    if password!=confirm_password:
        return render_template("message.html", message1="Password Not Matched")
    query={"email":email}
    count=nutritionist_collection.count_documents(query)
    if count>0:
        return render_template("message.html", message1="Email already registered")
    query={"phone":phone}
    count=nutritionist_collection.count_documents(query)
    if count>0:
        return render_template("message.html", message1="Phone Number already registered")
    query = {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "password": confirm_password, "address": address, "state": state, "city": city, "zipcode": zipcode, "status": "not verified"}
    nutritionist_collection.insert_one(query)
    return render_template("message.html", message="Nutritionist Registered")


@app.route("/create_diet_plan")
def create_diet_plan():
    return render_template("create_diet_plan.html")


@app.route("/create_diet_plan_action", methods=['post'])
def create_diet_plan_action():
    diet_title=request.form.get("diet_title")
    diet_price=request.form.get("diet_price")
    age_from=request.form.get("age_from")
    age_out=request.form.get("age_out")
    instructions=request.form.get("instructions")
    about_diet=request.form.get("about_diet")
    calories_to_be_burn=request.form.get("calories_to_be_burn")
    calories_to_be_consume=request.form.get("calories_to_be_consume")
    diet_for=request.form.get("diet_for")
    nutritionist_id = session['nutritionist_id']

    product_images = request.files.get("image")
    path = diet_plan_images_path + "/" + product_images.filename
    product_images.save(path)

    query={"diet_title":diet_title, "diet_price":diet_price, "age_from":age_from, "age_out":age_out, "instructions":instructions, "about_diet":about_diet, "calories_to_be_burn":calories_to_be_burn, "calories_to_be_consume":calories_to_be_consume, "diet_for":diet_for, "nutritionist_id":ObjectId(nutritionist_id), "image":product_images.filename, "status":"not verified"}
    diet_plan_collection.insert_one(query)
    return render_template("message.html", message="Diet Plan Added")


@app.route("/user_login")
def user_login():
    return render_template("user_login.html")


@app.route("/user_login_action", methods=['post'])
def user_login_action():
    email=request.form.get("email")
    password=request.form.get("password")
    query={"email":email, "password":password}
    count = users_collection.count_documents(query)
    if count>0:
        user = users_collection.find_one(query)
        session['role']="user"
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        return render_template("user_home.html")
    else:
        return render_template("message.html", message1="Invalid Login Details")


@app.route("/user_registration")
def user_registration():
    return render_template("user_registration.html")


@app.route("/user_registration_action", methods=['post'])
def user_registration_action():
    name=request.form.get("name")
    email=request.form.get("email")
    phone=request.form.get("phone")
    password=request.form.get("password")
    confirm_password=request.form.get("confirm_password")
    address=request.form.get("address")
    age=request.form.get("age")
    gender=request.form.get("gender")
    if password!=confirm_password:
        return render_template("message.html", message1="Password Not Matched")
    query={"email":email}
    count=users_collection.count_documents(query)
    if count>0:
        return render_template("message.html", message1="Duplicate Email Id")
    query = {"phone": phone}
    count = users_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message1="Duplicate Phone Number")
    query = {"name":name, "email": email, "password":confirm_password, "address":address, "age":age, "gender":gender}
    users_collection.insert_one(query)
    return render_template("message.html", message="User Successfully Registered")


@app.route("/buy_diet_plan")
def buy_diet_plan():
    diet_plan_id=request.args.get("diet_plan_id")
    user_id=session['user_id']
    amount=request.args.get("amount")
    current_month = datetime.now().strftime("%Y-%m")
    return render_template("buy_diet_plan.html", user_id=user_id, diet_plan_id=diet_plan_id, amount=amount, current_month=current_month)


@app.route("/payment_action", methods=['post'])
def payment_action():
    user_id=request.form.get("user_id")
    diet_plan_id=request.form.get("diet_plan_id")
    amount=request.form.get("amount")
    holder_name=request.form.get("holder_name")
    card_number=request.form.get("card_number")
    cvv=request.form.get("cvv")
    card_type=request.form.get("card_type")
    expire_date=request.form.get("expire_date")
    date=datetime.now().date()
    date_str = date.isoformat()
    query={"amount":amount, "date":date_str, "holder_name":holder_name, "card_number":card_number, "cvv":cvv, "card_type":card_type, "expire_date":expire_date, "status":"payment successful", "diet_plan_id":ObjectId(diet_plan_id), "user_id":ObjectId(user_id)}
    payment_collection.insert_one(query)
    query={"user_id":ObjectId(user_id), "diet_plan_id":ObjectId(diet_plan_id), "status":"enrolled"}
    user_diet_collection.insert_one(query)
    return render_template("message.html", message="Diet Plan Successfully Purchased")


@app.route("/food_timings")
def food_timings():
    diet_plan_id=request.args.get("diet_plan_id")
    return render_template("food_timings.html", diet_plan_id=diet_plan_id)


@app.route("/food_timings_action", methods=['post'])
def food_timings_action():
    diet_plan_id=request.form.get("diet_plan_id")
    timing_title=request.form.get("timing_title")
    food_time=request.form.get("food_time")
    calories_can_take=request.form.get("calories_can_take")
    carbs_can_take = request.form.get("carbs_can_take")
    proteins_can_take = request.form.get("proteins_can_take")
    fats_can_take = request.form.get("fats_can_take")
    facts = {
        "calories_can_take": calories_can_take,
        "carbs_can_take": carbs_can_take,
        "fats_can_take": fats_can_take,
        "proteins_can_take": proteins_can_take
    }
    query={"diet_plan_id":ObjectId(diet_plan_id), "food_timing_title":timing_title, "food_time":food_time, "facts":facts}
    food_timings_collection.insert_one(query)
    return redirect("/view_diet_plans")


@app.route("/exercise_timings")
def exercise_timings():
    diet_plan_id=request.args.get("diet_plan_id")
    return render_template("exercise_timings.html", diet_plan_id=diet_plan_id)


@app.route("/exercise_timings_action", methods=['post'])
def exercise_timings_action():
    diet_plan_id=request.form.get("diet_plan_id")
    timing_title=request.form.get("timing_title")
    exercise_time=request.form.get("exercise_time")
    calories_should_be_burn = request.form.get("calories_should_be_burn")
    query={"diet_plan_id":ObjectId(diet_plan_id), "exercise_title":timing_title, "exercise_time":exercise_time, "calories_should_be_burn":calories_should_be_burn}
    exercise_timings_collection.insert_one(query)
    return redirect("/view_diet_plans")


@app.route("/view_enrolled_diet_plans")
def view_enrolled_diet_plans():
    query = {}
    if session['role']=='user':
        user_id=session['user_id']
        query={"user_id":ObjectId(user_id), "status":"enrolled"}
    elif session['role']=='Nutritionist':
        nutritionist_id = session['nutritionist_id']
        diet_plans = diet_plan_collection.find({"nutritionist_id":ObjectId(nutritionist_id)})
        diet_plan_ids = []
        for diet_plan in diet_plans:
            diet_plan_ids.append({"diet_plan_id":ObjectId(diet_plan['_id'])})
        query = {"$or":diet_plan_ids}
    user_diets=user_diet_collection.find(query)
    user_diets=list(user_diets)
    return render_template("view_enrolled_diet_plans.html", get_diet_plan_by_diet_plan_id=get_diet_plan_by_diet_plan_id, get_exercise_by_diet_plan_id=get_exercise_by_diet_plan_id, get_food_items_by_diet_plan_id=get_food_items_by_diet_plan_id, str=str, user_diets=user_diets)


@app.route("/add_food_details")
def add_food_details():
    food_timing_id=request.args.get("food_timing_id")
    query={"food_timing_id":ObjectId(food_timing_id)}
    food_details=food_in_diet_collection.find(query)
    food_details=list(food_details)
    return render_template("add_food_details.html", food_timing_id=food_timing_id, food_details=food_details)


@app.route("/add_food_details_action", methods=['post'])
def add_food_details_action():
    food_timing_id=request.form.get("food_timing_id")
    food_name=request.form.get("food_name")
    quantity=request.form.get("quantity")
    units=request.form.get("units")
    preparation_process=request.form.get("preparation_process")
    calories=request.form.get("calories")
    carbohydrates=request.form.get("carbohydrates")
    fats=request.form.get("fats")
    proteins=request.form.get("proteins")
    facts = {
        "calories":calories,
        "carbohydrates":carbohydrates,
        "fats":fats,
        "proteins":proteins
    }
    query={"food_timing_id":ObjectId(food_timing_id), "food_name":food_name, "quantity":quantity, "units":units, "preparation_process":preparation_process,"facts":facts}
    food_in_diet_collection.insert_one(query)
    return redirect("/add_food_details?food_timing_id="+str(food_timing_id))


@app.route("/add_exercises")
def add_exercises():
    exercise_timing_id = request.args.get("exercise_timing_id")
    query={"exercise_timing_id":exercise_timing_id}
    exercises=exercise_in_diet_collection.find(query)
    exercises=list(exercises)
    query = {}
    exercise_types = exercise_type_collection.find(query)
    exercise_types = list(exercise_types)
    return render_template("add_exercises.html", exercise_timing_id=exercise_timing_id, exercises=exercises, exercise_types=exercise_types, get_exercise_type_by_exercise_type_id=get_exercise_type_by_exercise_type_id)


@app.route("/add_exercises_action", methods=['post'])
def add_exercises_action():
    exercise_timing_id=request.form.get("exercise_timing_id")
    exercise_name=request.form.get("exercise_name")
    exercise_type=request.form.get("exercise_type")
    duration=request.form.get("duration")
    calories_burn=request.form.get("calories_burn")
    query={"exercise_timing_id":exercise_timing_id, "exercise_name":exercise_name, "exercise_type":ObjectId(exercise_type), "duration":duration, "calories-burn":calories_burn}
    exercise_in_diet_collection.insert_one(query)
    return redirect("/add_exercises?exercise_timing_id="+str(exercise_timing_id))


@app.route("/view_food")
def view_food():
    food_timing_id=request.args.get("food_timing_id")
    user_diet_id=request.args.get("user_diet_id")
    query={"food_timing_id":ObjectId(food_timing_id)}
    food_timings=food_in_diet_collection.find(query)
    food_in_diets=list(food_timings)
    return render_template("view_food.html", get_user_food_by_food_in_diet_id=get_user_food_by_food_in_diet_id, food_in_diets=food_in_diets, food_timing_id=food_timing_id, user_diet_id=user_diet_id, int=int)


@app.route("/view_exercises")
def view_exercises():
    user_diet_id=request.args.get("user_diet_id")
    exercise_timing_id=request.args.get("exercise_timing_id")
    print(exercise_timing_id)
    query={"exercise_timing_id":ObjectId(exercise_timing_id)}
    print(query)
    exercises=exercise_in_diet_collection.find(query)
    print(exercises)
    exercises=list(exercises)
    print(exercises)
    return render_template("view_exercises.html", get_user_exercise_by_exercise_in_diet_id=get_user_exercise_by_exercise_in_diet_id, exercises=exercises, user_diet_id=user_diet_id, exercise_timing_id=exercise_timing_id, int=int, str=str)


@app.route("/user_diet_action", methods=['post'])
def user_diet_action():
    user_diet_id=request.form.get("user_diet_id")
    food_in_diet_id=request.form.get("food_in_diet_id")
    food_timing_id=request.form.get("food_timing_id")
    quantity=request.form.get("quantity")
    date=request.form.get("date")
    query={"user_diet_id":ObjectId(user_diet_id), "food_in_diet_id":ObjectId(food_in_diet_id), "quantity":quantity, "date":date}
    user_food_collection.insert_one(query)
    return redirect("/view_food?user_diet_id="+str(user_diet_id)+"&food_in_diet_id="+str(food_in_diet_id)+"&food_timing_id="+str(food_timing_id))


@app.route("/user_exercise_action", methods=['post'])
def user_exercise_action():
    user_diet_id=request.form.get("user_diet_id")
    exercise_timing_id=request.form.get("exercise_timing_id")
    exercise_in_diet_id=request.form.get("exercise_in_diet_id")
    number_of_sets=request.form.get("number_of_sets")
    date=request.form.get("date")
    query={"user_diet_id":ObjectId(user_diet_id), "exercise_in_diet_id":ObjectId(exercise_in_diet_id), "number_of_sets":number_of_sets, "date":date}
    user_exercise_collection.insert_one(query)
    return redirect("/view_exercises?user_diet_id="+str(user_diet_id)+"&exercise_in_diet_id="+str(exercise_in_diet_id)+"&exercise_timing_id="+str(exercise_timing_id))


@app.route("/view_review")
def view_review():
    query={}
    reviews=review_collection.find(query)
    reviews=list(reviews)
    return render_template("review.html", reviews=reviews)


@app.route("/review")
def review():
    user_id=session['user_id']
    user_diet_id=request.args.get("user_diet_id")
    return render_template("review.html", user_diet_id=user_diet_id, user_id=user_id)


@app.route("/review_action", methods=['post'])
def review_action():
    user_id=request.form.get("user_id")
    user_diet_id=request.form.get("user_diet_id")
    rating=request.form.get("rating")
    review=request.form.get("review")
    date=datetime.now()
    query={"user_id":user_id, "user_diet_id":user_diet_id, "rating":rating, "review":review, "date":date}
    review_collection.insert_one(query)
    return redirect("/view_enrolled_diet_plans")


@app.route("/discussion")
def discussion():
    user_diet_id = request.args.get("user_diet_id")
    diet_details=user_diet_collection.find({'_id':ObjectId(user_diet_id)})
    diet_details=list(diet_details)
    return render_template("discussion.html", user_diet_id=user_diet_id, diet_details=diet_details, get_nutritionist_name_by_nutritionist_id=get_nutritionist_name_by_nutritionist_id, get_user_name_by_user_id=get_user_name_by_user_id)


@app.route("/discussion_action", methods=['post'])
def discussion_action():
    user_diet_id = request.form.get("user_diet_id")
    comment=request.form.get("comment")
    date=datetime.now()
    commented_by = None
    messaged_by = None
    if session['role']=="user":
        commented_by = session['user_id']
        messaged_by = "User"
    elif session['role']=="Nutritionist":
        commented_by = session['nutritionist_id']
        messaged_by="Nutritionist"
    discussion_on_diet={
        "comment":comment,
        "date":date,
        "commented_by":ObjectId(commented_by),
        "messaged_by":messaged_by
    }
    user_diet_collection.update_one(
        {"_id":ObjectId(user_diet_id)},
        {"$push": {"discussion_on_diet": discussion_on_diet}}
    )
    return redirect("/discussion?user_diet_id="+str(user_diet_id))


def get_nutritionist_name_by_nutritionist_id(nutritionist_id):
    query={'_id':nutritionist_id}
    nutritionists=nutritionist_collection.find_one(query)
    return nutritionists


def get_diet_plan_by_diet_plan_id(diet_plan_id):
    query={'_id':diet_plan_id}
    diet_plan=diet_plan_collection.find_one(query)
    return diet_plan


def get_exercise_by_diet_plan_id(diet_plan_id):
    query = {"diet_plan_id": diet_plan_id}
    print(query)
    exercises = exercise_timings_collection.find_one(query)
    print(exercises)
    return exercises


def get_food_items_by_diet_plan_id(diet_plan_id):
    query = {"diet_plan_id": diet_plan_id}
    food_timing = food_timings_collection.find_one(query)
    return food_timing


def get_user_food_by_food_in_diet_id(food_in_diet_id,user_diet_id):
    user_foods = user_food_collection.find({"food_in_diet_id":ObjectId(food_in_diet_id), "user_diet_id":ObjectId(user_diet_id)})
    return user_foods


def get_user_exercise_by_exercise_in_diet_id(exercise_in_diet_id,user_diet_id):
    user_exercises = user_exercise_collection.find({"exercise_in_diet_id":ObjectId(exercise_in_diet_id),"user_diet_id":ObjectId(user_diet_id)})
    return user_exercises


def get_user_name_by_user_id(user_id):
    query={"_id":ObjectId(user_id)}
    users=users_collection.find_one(query)
    return users


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add_exercise_type")
def add_exercise_type():
    query = {}
    exercises = exercise_type_collection.find(query)
    exercises = list(exercises)
    return render_template("add_exercise_type.html", exercises=exercises)


@app.route("/add_exercise_type_action", methods=['post'])
def add_exercise_type_action():
    exercise_name = request.form.get("exercise_name")
    query = {"exercise_name":exercise_name}
    exercise_type_collection.insert_one(query)
    return redirect("/add_exercise_type")


@app.route("/diet_for")
def diet_for():
    query = {}
    diets = diet_for_collection.find(query)
    diets = list(diets)
    return render_template("diet_for.html", diets = diets)


@app.route("/diet_type_action", methods=['post'])
def diet_type_action():
    diet_name = request.form.get("diet_name")
    query = {"diet_name": diet_name}
    diet_for_collection.insert_one(query)
    return redirect("/diet_for")


@app.route("/update_food_details")
def update_food_details():
    food_timing_id = request.args.get("food_timing_id")
    query = {'_id':ObjectId(food_timing_id)}
    food_timings = food_timings_collection.find_one(query)
    return render_template("update_food_details.html", food_timings=food_timings)


@app.route("/update_food_details_action", methods=['post'])
def update_food_details_action():
    food_timing_id = request.form.get("food_timing_id")
    timing_title = request.form.get("timing_title")
    food_time = request.form.get("food_time")
    calories_can_take = request.form.get("calories_can_take")
    carbs_can_take = request.form.get("carbs_can_take")
    proteins_can_take = request.form.get("proteins_can_take")
    fats_can_take = request.form.get("fats_can_take")
    facts = {
        "calories_can_take": calories_can_take,
        "carbs_can_take": carbs_can_take,
        "fats_can_take": fats_can_take,
        "proteins_can_take": proteins_can_take
    }
    query = {'_id':ObjectId(food_timing_id)}
    query1 = {"$set":{"timing_title":timing_title, "food_time":food_time, "facts":facts}}
    food_timings_collection.update_one(query, query1)
    return redirect("/view_diet_plans")


def get_exercise_type_by_exercise_type_id(exercise_type_id):
    query = {'_id':ObjectId(exercise_type_id)}
    exercise_type = exercise_type_collection.find_one(query)
    return exercise_type


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port for Render
    app.run(host="0.0.0.0", port=port)