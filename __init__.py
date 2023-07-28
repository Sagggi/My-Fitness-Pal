from flask import Flask, render_template, redirect, url_for, request
import random

app = Flask(__name__)

pushday=[['Bench Press','Dips','Incline Bench Press','Decline Bench Press'],['Flies','Dumbbell Shoulder Press','Arnold Press','Military Press','Side Raise','Front Raise'],['Skull Crushers','Cable Overhead Extension','Caple Rope Extension','Diamond Pushup']]
pullday=[['Dead Lift','T-Bar Rows','Bentover Rows','Cable Rows','Lat-pull Down','Pullups'],['Dumbbell Curls','Spider Curls','Wide Grip Curls','Hammer Curls','Narrow Grip Curls']]
legday=['Calves Raise',['Squats','Leg Extensions','Weighted Lunges','Leg Press','Sumo Dead Lifts','Leg Curls']]
home=[['Normal Pushups','Wide Grip Pushups','Diamond Pushups','Shoulder Tap'],['Pullups','V-Ups','Crunches'],['Jump Lunges','Squats','Calves Raise','Walking Lunges']]

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/introduction',methods=["POST"])
def intro_page():
    global name
    if request.form["Name"]=='':
        name='User'
    else:
        name=request.form["Name"]
    return render_template('intro_page.html',username=name)

@app.route('/inputinfo',methods=["POST"])
def input_info_page():
    return render_template('input_info_page.html')

@app.route('/final_page',methods=["POST"])
def final_page():
    weight=request.form["weight"]
    height=request.form["height"]
    age=request.form["age"]
    sex=request.form['sex']
    activeness=request.form['activeness']
    goal=request.form['goal']
    mode=request.form['mode']
    workout={}
    workout_push=[]
    workout_pull=[]
    workout_leg=[]
    workout_home=[]
    if mode=='gym':
        if goal=='fitness':
            workout['push1']=random.sample(pushday[1],3)
            workout['push2']=random.sample(pushday[2],2)
            workout['push3']=random.sample(pushday[2],2)
            workout['pull1']=random.sample(pullday[0],3)
            workout['pull2']=random.sample(pullday[1],2)
            workout['leg1']=[legday[0]]
            workout['leg2']=random.sample(legday[1],4)
            workout_push=workout['push1']+workout['push2']+workout['push3']
            workout_pull=workout['pull1']+workout['pull2']
            workout_leg=workout['leg1']+workout['leg2']
        elif goal=='weightloss':
            workout['cardio']=['Walking','Cycling']
            workout['push1']=random.sample(pushday[1],3)
            workout['push2']=random.sample(pushday[2],3)
            workout['push3']=random.sample(pushday[2],3)
            workout['pull1']=random.sample(pullday[0],3)
            workout['pull2']=random.sample(pullday[1],2)
            workout['leg1']=[legday[0]]
            workout['leg2']=random.sample(legday[1],4)
            workout_push=workout['cardio']+workout['push1']+workout['push2']+workout['push3']
            workout_pull=workout['cardio']+workout['pull1']+workout['pull2']
            workout_leg=workout['cardio']+workout['leg1']+workout['leg2']
        elif goal=='bulking':
            workout['push1']=random.sample(pushday[1],3)
            workout['push2']=random.sample(pushday[2],2)
            workout['push3']=random.sample(pushday[2],2)
            workout['pull1']=random.sample(pullday[0],3)
            workout['pull2']=random.sample(pullday[1],2)
            workout['leg1']=[legday[0]]
            workout['leg2']=random.sample(legday[1],4)
            workout_push=workout['push1']+workout['push2']+workout['push3']
            workout_pull=workout['pull1']+workout['pull2']
            workout_leg=workout['leg1']+workout['leg2']
        else:
            return redirect('/inputinfo')
    elif mode=='home':
        workout['cardio']=['Walking','Cycling']
        workout['home1']=random.sample(home[0],3)
        workout['home2']=random.sample(home[1],2)
        workout['home3']=random.sample(home[2],3)
        workout_home=workout['cardio']+workout['home1']+workout['home2']+workout['home3']
    else:
        return redirect('/inputinfo')
    if activeness=='sedentary':
        PA=1.0
    elif activeness=='lessactive':
        PA=1.12
    elif activeness=='active':
        PA=1.27
    else:
        return redirect('/inputinfo')
    if sex=='male':
        calorie=864-9.72*float(age)+PA*(14.2*float(weight)+503*float(height))
    elif sex=='female':
        calorie=387-7.31*float(age)+PA*(10.9*float(weight)+660.7*float(height))
    else:
        return redirect('/inputinfo')
    if goal=='weightloss':
        calorie-=300
    elif goal=='bulking':
        calorie+=300
    else:
        pass
    calorie=int(calorie)
    final_workout=workout_push+workout_pull+workout_leg+workout_home
    return render_template('final_page.html', workout=final_workout, calorie=calorie)

if __name__=="__main__":
    app.run(debug=True)