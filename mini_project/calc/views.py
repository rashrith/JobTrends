from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
import pyrebase 
import joblib
import pandas as pd

config={
    'apiKey': "AIzaSyBQt_VvM-THUsVu7MG9SY16NMblWwNiigg",
    'authDomain': "miniproject-720b3.firebaseapp.com",
    'databaseURL': "https://miniproject-720b3.firebaseio.com",
    'projectId': "miniproject-720b3",
    'storageBucket': "miniproject-720b3.appspot.com",
    'messagingSenderId': "71428181495",
    'appId': "1:71428181495:web:b9829f19a63b78333372f2"
}
# Initialize Firebase
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
reload=joblib.load('./models/RFModelforMPG.pkl')
onehotencoder_X=joblib.load('./models/RFModelforMPG1.pkl')
labelencoder_Y=joblib.load('./models/RFModelforMPG2.pkl')

# Create your views here.
def signIn(request):
    return render(request, "signIn.html")
def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"signIn.html",{"msg":message})
    print(user)
    # session_id=user['idToken']
    # request.session['uid']=str(session_id)
    return render(request, "home.html",{"e":email})
# def logout(request):
#     auth.logout(request)
#     return render(request,'signIn.html')
def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    print(email)
    try:
        user=authe.create_user_with_email_and_password(email,passw)
        print(user,name)
        # uid = user['localId']
        # data={"name":name,"status":"1"}
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
        

    
    return render(request,"signIn.html")
def home(request):
    return render(request,'home.html',{'name':'krishna'})
def add(request):
    # val1=int(request.GET['num1'])
    # val2=int(request.GET['num2'])
    # res=val1+val2
    if request.method=='POST':
        temp={}
        temp['location']=request.POST.get('Location')
        temp['sector']=request.POST.get('Category')
        temp['salary']=int(request.POST.get('Salary'))
        temp['expierence']=int(request.POST.get('Experience'))
        temp['qualification']=request.POST.get('Qualification')

    testDtaa=pd.DataFrame({'x':temp}).transpose()
    testDtaa=onehotencoder_X.transform(testDtaa).toarray()
    res=labelencoder_Y.inverse_transform([reload.predict(testDtaa)[0]])
    return render(request,"result.html",{'res':res[0]})