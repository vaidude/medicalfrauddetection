from django.contrib.auth import logout
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from  .models  import reg,adminreg,agent,Patient,PredictionResult
from django.contrib import messages
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

# Load the dataset
df = pd.read_csv('C:\\Users\\vaiva\\OneDrive\\Desktop\\office files\\Test_Beneficiarydata.csv')

# Display the first few rows to understand the structure of the data
print(df.head())
# Prepare features (X) and target variable (y)
X = df.drop(columns=['Class', 'BeneID'])  # Features
print(X.shape)
y = df['Class']  # Target variable
from sklearn.model_selection import train_test_split

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.ensemble import RandomForestClassifier

# Initialize the random forest classifier
rf_classifier = RandomForestClassifier()

# Train the classifier
rf_classifier.fit(X_train, y_train)
# Make predictions on the test data
y_pred = rf_classifier.predict(X_test)


# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')
def service(request):
    return render(request,'service.html')
def home(request):
    return render(request,'home.html')


# def register(request):
#     return render(request,'register.html')

# def login(request):
#     return render(request,'login.html')

def register(request):
    if request.method=='POST':
        a=request.POST.get('fname')
        c=request.POST.get('lname')
        d=request.POST.get('email')
        
        f=request.POST.get('pwd')
        g=request.POST.get('cpwd')
        h=request.POST.get('gender')
        reg(fname=a,lname=c,email=d,pwd=f,cpwd=g,gender=h).save()
        return render(request,'index.html')
    else:
        return render(request,'register.html')
    
def adminregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate the password using the adminreg model
        admin_instance = adminreg(name=name, email=email, password=password)

        try:
            admin_instance.full_clean()
            # If validation succeeds, save the adminreg object
            admin_instance.password = make_password(password)  # Hash the password before saving
            admin_instance.save()
            return render(request, 'index.html')
        except ValidationError as e:
            # If validation fails, capture the error messages and pass them to the template
            error_messages = e.messages
            return render(request, 'adminreg.html', {'error_messages': error_messages})

    else:
        return render(request, 'adminreg.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        try:
            user = reg.objects.get(email=email, pwd=pwd)
            if user.is_approved:
                # Agent is approved, proceed with login
                request.session['email'] = user.email
                return render(request, 'home.html')
            else:
                # Agent is not approved, display error message
                messages.error(request, "Your registration is pending approval.")
                return render(request, 'login.html')
        except reg.DoesNotExist:
            # Handle invalid login credentials
            messages.error(request, "Invalid Email or Password")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


    
# def admlog(request):
#     if request.method=="POST":
#         email=request.POST.get('email')
#         # print(name)
#         password = request.POST.get('password')
#         # print('joy')
#         cr = adminreg.objects.filter(email=email,password=password)
#         if cr:
#             ad =adminreg.objects.get(email=email,password=password)
#             id=ad.id
#             email=ad.email
#             password=ad.password
#             request.session['email']=email
#             return render(request,'adminhome.html')
#         else:
#             messages = "Invalid Email or Password"
#             print(messages)
#             return render(request,'adminlogin.html',{'messages':messages}) 
            
    # else:
       
    #     return render(request,'adminlogin.html')

def admhome(request):
    return render(request,'adminhome.html')
def logoutc(request):
    logout(request)
    return redirect(index) #
    
def profile(request):
        email=request.session['email']
        cr=reg.objects.get(email=email)
        fname=cr.fname
        lname=cr.lname
        email=cr.email
        pwd=cr.pwd
        cpwd=cr.cpwd
        gender=cr.gender
        return render(request,'profile.html',{'fname':fname,'lname':lname,'email':email,'pwd':pwd,'cpwd':cpwd,'gender':gender})
def proupdate(request):
    email=request.session['email']
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd=request.POST.get('pwd') 
        cpwd=request.POST.get('cpwd') 
        dt=reg.objects.get(email=email)
        dt.fname=fname
        dt.lname=lname
        dt.email=email
        dt.pwd=pwd
        dt.cpwd=cpwd
        dt.save()
        #message =  'Account created  successfully'
        #return render(request,"profile.html",{'message':message})
        messages.success(request, "Profile Updated Successfully")
        response=redirect('/profile/')
       
        return response
        
    else:
        return render(request,'profile.html',)
    
def userlist(request):
    users = reg.objects.all()
    return render(request, 'userlist.html', {'users': users})
    
def delete_user(request, user_id):
    user = reg.objects.get(pk=user_id)
    user.delete()
    return redirect('admhome')
def deletepatient(request, id):
    # Attempt to get the Patient object or return a 404 error if not found
    user = get_object_or_404(Patient, id=id)

    # Delete the patient object
    user.delete()

    # Redirect to the admin home page
    return render(request, 'adminhome.html')


def agentreg(request):
    if request.method == 'POST':
        agname = request.POST.get('agname')
        agemail = request.POST.get('agemail')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        # Validate the password using the adminreg model
        agent(agname=agname, agemail=agemail, password=password, phone=phone).save()
        return render(request, 'agentlogin.html')
    else:
        return render(request, 'agentregister.html')


def approve_reject_agent(request):
    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        print(agent_id)
        action = request.POST.get('action')
        try:
            agen = agent.objects.get(id=agent_id)
            if action == 'approve':
                agen.is_approved = True
                agen.save()
                messages.success(request, f"Agent {agen.agname} has been approved successfully.")
            elif action == 'reject':
                agen.is_approved = False
                agen.save()
                messages.success(request, f"Agent {agen.agname} has been rejected.")
            else:
                messages.error(request, "Invalid action.")
        except agent.DoesNotExist:
            messages.error(request, "Agent not found.")
    return HttpResponseRedirect('/agentlist')


    #     try:
    #         agentdata.full_clean()
    #         # If validation succeeds, save the adminreg object
    #         agentdata.password = make_password(password)  # Hash the password before saving
    #         agentdata.save()
    #         return render(request, 'agentlogin.html')
    #     except ValidationError as e:
    #         # If validation fails, capture the error messages and pass them to the template
    #         error_messages = e.messages
    #         return render(request, 'agentregister.html', {'error_messages': error_messages})

    # else:
    #     return render(request, 'agentregister.html')
def agenthome(request):
    return render(request,"agenthome.html")


def agentlog(request):
    if request.method == "POST":
        agemail = request.POST.get('agemail')
        password = request.POST.get('password')
        try:
            # Check if the agent is approved and login
            ad = agent.objects.get(agemail=agemail, password=password)
            if ad.is_approved:
                request.session['agent_id']= ad.id
                request.session['agemail'] = agemail
                return redirect('agenthome')  # Redirect to agent home page
            else:
                # Agent exists but is not approved
                messages.error(request, "Your account is not approved yet. Please wait for approval.")
                return render(request, 'agentlogin.html')
        except agent.DoesNotExist:
            # Handle invalid login (agent does not exist)
            messages.error(request, "Invalid Email or Password")
            return render(request, 'agentlogin.html')
    else:
        return render(request, 'agentlogin.html')

from .models import Patient

from django.shortcuts import render, redirect
from .models import Patient
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

from .models import Patient
from django.shortcuts import render
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Initialize the model outside the view function
model = RandomForestClassifier()

# def uploadform(request):
#     if request.method == 'POST':
#         # Retrieve data from the POST request
#         agemail = request.POST.get("agemail")
#         BeneficiaryId = request.POST.get("BeneficiaryId")
#         if Patient.objects.filter(BeneficiaryId=BeneficiaryId).exists():
#             # Patient with the same BeneficiaryId already exists, so display an error message
#             error_message = "A patient with the same BeneficiaryId already exists."
#             return render(request, 'error.html')
#         provider = request.POST.get('provider')
#         InscClaimAmtReimbursed = float(request.POST.get('InscClaimAmtReimbursed'))
#         DeductibleAmtPaid = float(request.POST.get('DeductibleAmtPaid'))
#         PotentialFraud = float(request.POST.get('PotentialFraud'))
#         gender = float(request.POST.get('gender'))
#         race = float(request.POST.get('race'))
#         RenalDiseaseIndicator = float(request.POST.get('RenalDiseaseIndicator'))
#         NoOfMonths_PartACov = float(request.POST.get('NoOfMonths_PartACov'))
#         NoOfMonths_PartBCov = float(request.POST.get('NoOfMonths_PartBCov'))
#         ChronicCond_Alzheimer = float(request.POST.get('ChronicCond_Alzheimer', 0))  # Default value provided
#         ChronicCond_Heartfailure = float(request.POST.get('ChronicCond_Heartfailure', 0))  # Default value provided
#         ChronicCond_KidneyDisease = float(request.POST.get('ChronicCond_KidneyDisease', 0))  # Default value provided
#         ChronicCond_Cancer = float(request.POST.get('ChronicCond_Cancer', 0))  # Default value provided
#         ChronicCond_ObstrPulmonary = float(request.POST.get('ChronicCond_ObstrPulmonary', 0))  # Default value provided
#         ChronicCond_Depression = float(request.POST.get('ChronicCond_Depression', 0))  # Default value provided
#         ChronicCond_Diabetes = float(request.POST.get('ChronicCond_Diabetes', 0))  # Default value provided
#         ChronicCond_IschemicHeart = float(request.POST.get('ChronicCond_IschemicHeart', 0))  # Default value provided
#         ChronicCond_Osteoporasis = float(request.POST.get('ChronicCond_Osteoporasis', 0))  # Default value provided
#         ChronicCond_rheumatoidarthritis = float(request.POST.get('ChronicCond_rheumatoidarthritis', 0))  # Default value provided
#         ChronicCond_stroke = float(request.POST.get('ChronicCond_stroke', 0))  # Default value provided
#         Numberofdaysadmitted= float(request.POST.get('Numberofdaysadmitted',0))
#         IPAnnualReimbursementAmt = float(request.POST.get('IPAnnualReimbursementAmt'))
#         IPAnnualDeductibleAmt = float(request.POST.get('IPAnnualDeductibleAmt'))
#         OPAnnualReimbursementAmt = float(request.POST.get('OPAnnualReimbursementAmt'))
#         OPAnnualDeductibleAmt = float(request.POST.get('OPAnnualDeductibleAmt'))


        
#         providers = Providers.objects.get(provideno=provider)
#         results = providers.result
#         print(results)

#         # Create a new Patient object
#         patient = Patient.objects.create(
#             agemail=agemail,
#             BeneficiaryId=BeneficiaryId,
#             provider=provider,
#             InscClaimAmtReimbursed=InscClaimAmtReimbursed,
#             DeductibleAmtPaid=DeductibleAmtPaid,
#             PotentialFraud=PotentialFraud,
#             gender=gender,
#             race=race,
#             RenalDiseaseIndicator=RenalDiseaseIndicator,
#             NoOfMonths_PartACov=NoOfMonths_PartACov,
#             NoOfMonths_PartBCov=NoOfMonths_PartBCov,
#             ChronicCond_Alzheimer=ChronicCond_Alzheimer,
#             ChronicCond_Heartfailure=ChronicCond_Heartfailure,
#             ChronicCond_KidneyDisease=ChronicCond_KidneyDisease,
#             ChronicCond_Cancer=ChronicCond_Cancer,
#             ChronicCond_ObstrPulmonary=ChronicCond_ObstrPulmonary,
#             ChronicCond_Depression=ChronicCond_Depression,
#             ChronicCond_Diabetes=ChronicCond_Diabetes,
#             ChronicCond_IschemicHeart=ChronicCond_IschemicHeart,
#             ChronicCond_Osteoporasis=ChronicCond_Osteoporasis,
#             ChronicCond_rheumatoidarthritis=ChronicCond_rheumatoidarthritis,
#             ChronicCond_stroke=ChronicCond_stroke,

#             IPAnnualReimbursementAmt=IPAnnualReimbursementAmt,
#             IPAnnualDeductibleAmt=IPAnnualDeductibleAmt,
#             OPAnnualReimbursementAmt=OPAnnualReimbursementAmt,
#             OPAnnualDeductibleAmt=OPAnnualDeductibleAmt,
#         )

#         # Prepare data for fitting the model
#         X_train = np.array([[ InscClaimAmtReimbursed, DeductibleAmtPaid, PotentialFraud, gender, race,
#                              RenalDiseaseIndicator, NoOfMonths_PartACov, NoOfMonths_PartBCov, ChronicCond_Alzheimer,
#                              ChronicCond_Heartfailure, ChronicCond_KidneyDisease, ChronicCond_Cancer,
#                              ChronicCond_ObstrPulmonary, ChronicCond_Depression, ChronicCond_Diabetes,
#                              ChronicCond_IschemicHeart, ChronicCond_Osteoporasis, ChronicCond_rheumatoidarthritis,
#                              ChronicCond_stroke, IPAnnualReimbursementAmt, IPAnnualDeductibleAmt,
#                              OPAnnualReimbursementAmt, OPAnnualDeductibleAmt]])

#         # Fit the model
#         y_train = [1]  # Assuming you have a target value for this sample
#         model.fit(X_train, y_train)

#         # Make predictions
#         result = model.predict_proba(X_train)
#         print(result.shape)  # This should print the shape of the result array

# # Extract the probability of the first class (index 0)
#         fraud_probability = result[0][0]   
#         print('prob', fraud_probability)
#         fraud_probability = np.random.rand()  
#         print(fraud_probability)
        
#         if fraud_probability >= 0.4:
#             predicted_label = 'Yes'
#         else:
#             predicted_label = 'No'









#         # Save the predicted label to the patient object
#         patient.prediction_result = predicted_label
#         patient.save()

        

#         return render(request, 'result.html', {'patient': patient,'results':predicted_label,"fraud_probability":fraud_probability})
#     else:
#         return render(request, 'uploadform.html')

        # Render the form template if the request method is not POST
    
def patientviewbyid2(request):
    res11 = request.session.get('res')

    if res11 == "0":
        res11 = "Genuine"
    elif res11 == "1":
        res11 = "Fraud"

    # Assuming you have the BeneficiaryId of the patient in session
    # beneficiary_id = request.session.get('beneficiary_id')
    BeneficiaryId = request.session.get('BeneficiaryId')
    print(BeneficiaryId)
    print(res11)
    if BeneficiaryId:
        try:
            patient = Patient.objects.get(BeneficiaryId=BeneficiaryId)
            patient.prediction_result = res11
            patient.save()
        except Patient.DoesNotExist:
            # Handle case where patient with BeneficiaryId doesn't exist
            pass

    return render(request, 'patientviewbyid2.html', {'resuu': res11})
#     res11=request.session['res']

#     if res11=="0":
#         res11="Genuine"
#     if res11=="1":
#         res11="Fraud"
#     PredictionResult.objects.create(prediction=res11)
    
#     return render(request,'patientviewbyid2.html',{'resuu':res11})
def save_prediction_result(request):
    if request.method == 'POST':
        prediction = request.POST.get('prediction')
        PredictionResult.objects.create(prediction=prediction)
        return render(request, 'patientviewbyid2', {'resuu': prediction})
    else:
        return render(request, 'patientviewbyid2.html')  # Handle error gracefully



def listpatient(request):
    data=Patient.objects.all()
    return render(request,"listpatient.html",{"data":data})

def patientlistviewforagent(request):
    agemail = request.session.get('agemail')
    
    if agemail:
        # Assuming your cart model has a field named 'username' to store the username of the user who added the item to the cart
        cr = Patient.objects.filter(agemail=agemail)
        # prediction_results = {}
        # for patient in cr:
        #     prediction_result = PredictionResult.objects.filter(patient=patient).order_by('-created_at').first()
        #     prediction_results[patient.id] = prediction_result.prediction if prediction_result else None
        
        return render(request, 'patientlistviewforagent.html', {'data': cr,})
    else:
        # Handle the case when the user is not logged in
        # You might want to redirect the user to the login page or show an error message
        return HttpResponse("You need to be logged in to view list.")


from django.http import HttpResponse

def search(request):
    if request.method == 'POST':
        cat = request.POST.get('BeneficiaryId')
        data = Patient.objects.filter(BeneficiaryId=cat)
        return render(request,'search.html',{ "data" : data })
    else:
        return render(request, 'search.html')
    

        
    #     if data:
    #         return render(request, 'search.html', {'data': data})
    #     else:
    #         message = "No data found for the provided search criteria."
    #         return render(request, 'search.html', {'message': message})
    # else:
    #     return render(request, 'search.html')
def adpatient(request):
    data=Patient.objects.all()
    return render(request,'adpatient.html',{'data':data})
def deletes(request,id):
    data=agent.objects.get(id=id)
    data.delete()
    return render(request,'adminhome.html')

# views.py
import csv
from .models import Providers

def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        decoded_file = myfile.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(decoded_file)
        for row in csv_reader:
            obj = Providers(
                provideno=row[0],
                result=row[1],
                # Add more fields as needed
            )
            obj.save()
        return HttpResponse('CSV file has been imported successfully!')
    else:
        return render(request, 'import_csv.html')
    
def agentlist(request):
    data=agent.objects.all()
    return render(request,"agentlist.html",{"data":data})    


def patientview(request, agemail):
    if agemail:
        # Retrieve patients associated with the given agent's email address
        patients = Patient.objects.filter(agemail=agemail)
        
        # Pass the retrieved patients data to the template for rendering
        return render(request, 'patientview.html', {'patients': patients})
    else:
        # Handle the case when the user is not logged in
        # You might want to redirect the user to the login page or show an error message
        return HttpResponse("You need to be logged in to view the patient list.")

    
def admlog(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        u='admin@gmail.com'
        p='admin'
        if email==u:
            if password==p:
                return render(request,'adminhome.html')
    return render(request,'adminlogin.html')


def viewbyid(request):
    if request.method == "POST":
        BeneficiaryId = request.POST.get('BeneficiaryId')  # Use .get() method instead of ()
        cr = Patient.objects.filter(BeneficiaryId=BeneficiaryId)
        if cr:
            userd = Patient.objects.get(BeneficiaryId=BeneficiaryId)
            id = userd.id
            BeneficiaryId = userd.BeneficiaryId
            request.session['id'] = id
            request.session['BeneficiaryId'] = BeneficiaryId
            print('id at line 453',id)
            id=request.session['id']
            print('id is',id)
            cr = Patient.objects.get(id=id)
            agemail= cr.agemail
            # Provider= cr.provider
            BeneficiaryId= cr.BeneficiaryId
            InscClaimAmtReimbursed=cr.InscClaimAmtReimbursed
            DeductibleAmtPaid =cr.DeductibleAmtPaid
            PotentialFraud=cr.PotentialFraud
            gender=cr.gender
            race=cr.race
            RenalDiseaseIndicator=cr.RenalDiseaseIndicator
            NoOfMonths_PartACov=cr.NoOfMonths_PartACov
            NoOfMonths_PartBCov=cr.NoOfMonths_PartBCov
            ChronicCond_Alzheimer=cr.ChronicCond_Alzheimer
            print('alchemers',ChronicCond_Alzheimer)
            if ChronicCond_Alzheimer==True:
                ChronicCond_Alzheimer=1
            else:
                ChronicCond_Alzheimer=0

            ChronicCond_Heartfailure=cr.ChronicCond_Heartfailure
            if ChronicCond_Heartfailure==True:
                ChronicCond_Heartfailure=1
            else:
                ChronicCond_Heartfailure=0
            ChronicCond_KidneyDisease=cr.ChronicCond_KidneyDisease
            if ChronicCond_KidneyDisease==True:
                ChronicCond_KidneyDisease=1
            else:
                ChronicCond_KidneyDisease=0
            ChronicCond_Cancer=cr.ChronicCond_Cancer
            if ChronicCond_Cancer==True:
                ChronicCond_Cancer=1
            else:
                ChronicCond_Cancer=0

            ChronicCond_ObstrPulmonary=cr.ChronicCond_ObstrPulmonary
            if ChronicCond_ObstrPulmonary==True:
                ChronicCond_ObstrPulmonary=1
            else:
                ChronicCond_ObstrPulmonary=0
            ChronicCond_Depression=cr.ChronicCond_Depression
            if ChronicCond_Depression==True:
                ChronicCond_Depression=1
            else:
                ChronicCond_Depression=0
            ChronicCond_Diabetes=cr.ChronicCond_Diabetes
            if ChronicCond_Diabetes==True:
                ChronicCond_Diabetes=1
            else:
                ChronicCond_Diabetes=0
            ChronicCond_IschemicHeart=cr.ChronicCond_IschemicHeart
            if ChronicCond_IschemicHeart==True:
                ChronicCond_IschemicHeart=1
            else:
                ChronicCond_IschemicHeart=0
            ChronicCond_Osteoporasis=cr.ChronicCond_Osteoporasis
            if ChronicCond_Osteoporasis==True:
                ChronicCond_Osteoporasis=1
            else:
                ChronicCond_Osteoporasis=0
            ChronicCond_rheumatoidarthritis=cr.ChronicCond_rheumatoidarthritis
            if ChronicCond_rheumatoidarthritis==True:
                ChronicCond_rheumatoidarthritis=1
            else:
                ChronicCond_rheumatoidarthritis=0
            ChronicCond_stroke=cr.ChronicCond_stroke
            if ChronicCond_stroke==True:
                ChronicCond_stroke=1
            else:
                ChronicCond_stroke=0
            IPAnnualReimbursementAmt=cr.IPAnnualReimbursementAmt
            IPAnnualDeductibleAmt=cr.IPAnnualDeductibleAmt
            OPAnnualReimbursementAmt=cr.OPAnnualReimbursementAmt
            OPAnnualDeductibleAmt=cr.OPAnnualDeductibleAmt
            #         # Prepare data for fitting the model



# Create input data
            input_data = {
    'Gender': [gender],  # Rename 'gender' to 'Gender'
    'Race': [race],      # Rename 'race' to 'Race'
    'InscClaimAmtReimbursed': [InscClaimAmtReimbursed],
    'DeductibleAmtPaid': [DeductibleAmtPaid],
    'NoOfMonths_PartACov': [NoOfMonths_PartACov],
    'NoOfMonths_PartBCov': [NoOfMonths_PartBCov],
    'ChronicCond_Alzheimer': [ChronicCond_Alzheimer],
    'ChronicCond_Heartfailure': [ChronicCond_Heartfailure],
    'ChronicCond_KidneyDisease': [ChronicCond_KidneyDisease],
    'ChronicCond_Cancer': [ChronicCond_Cancer],
    'ChronicCond_ObstrPulmonary': [ChronicCond_ObstrPulmonary],
    'ChronicCond_Depression': [ChronicCond_Depression],
    'ChronicCond_Diabetes': [ChronicCond_Diabetes],
    'ChronicCond_IschemicHeart': [ChronicCond_IschemicHeart],
    'ChronicCond_Osteoporasis': [ChronicCond_Osteoporasis],
    'ChronicCond_rheumatoidarthritis': [ChronicCond_rheumatoidarthritis],
    'ChronicCond_stroke': [ChronicCond_stroke],
    'IPAnnualReimbursementAmt': [IPAnnualReimbursementAmt],
    'IPAnnualDeductibleAmt': [IPAnnualDeductibleAmt],
    'OPAnnualReimbursementAmt': [OPAnnualReimbursementAmt],
    'OPAnnualDeductibleAmt': [OPAnnualDeductibleAmt]
                        }

# Create input DataFrame
            input_df = pd.DataFrame(input_data)

# Print the shape of the input DataFrame
            print("Shape of input DataFrame:", input_df.shape)



#         # Make predictions
            prediction = rf_classifier.predict(input_df)

# # Extract the probability of the first class (index 0)
            fraud_probability = prediction[0]   
            print('prob', fraud_probability)

        
            if fraud_probability >= 0.4:
                predicted_label = 'Fraud'
            else:
                predicted_label = 'Genuine'
            request.session['res']=predicted_label
            return render(request, 'patientviewbyid.html',{'agemail':agemail,
                                                #    'Provider': Provider,
                                                   'BeneficiaryId': BeneficiaryId,
                                                   'InscClaimAmtReimbursed':InscClaimAmtReimbursed,
                                                   'DeductibleAmtPaid':DeductibleAmtPaid,
                                                   'PotentialFraud':PotentialFraud,
                                                    'gender':gender,
                                                    'race':race,
                                                    'RenalDiseaseIndicator':RenalDiseaseIndicator,
                                                    'NoOfMonths_PartACov':NoOfMonths_PartACov,
                                                    'NoOfMonths_PartBCov':NoOfMonths_PartBCov,
                                                    'ChronicCond_Alzheimer':ChronicCond_Alzheimer,
                                                    'ChronicCond_Heartfailure':ChronicCond_Heartfailure,
                                                    'ChronicCond_KidneyDisease':ChronicCond_KidneyDisease,
                                                    'ChronicCond_Cancer':ChronicCond_Cancer,
                                                    'ChronicCond_ObstrPulmonary':ChronicCond_ObstrPulmonary,
                                                    'ChronicCond_Depression':ChronicCond_Depression,
                                                    'ChronicCond_Diabetes':ChronicCond_Diabetes,
                                                    'ChronicCond_IschemicHeart':ChronicCond_IschemicHeart,
                                                    'ChronicCond_Osteoporasis':ChronicCond_Osteoporasis,
                                                    'ChronicCond_rheumatoidarthritis':ChronicCond_rheumatoidarthritis,
                                                    'ChronicCond_stroke':ChronicCond_stroke,
                                                    'IPAnnualReimbursementAmt':IPAnnualReimbursementAmt,
                                                    'IPAnnualDeductibleAmt':IPAnnualDeductibleAmt,
                                                    'OPAnnualReimbursementAmt':OPAnnualReimbursementAmt,
                                                    'OPAnnualDeductibleAmt':OPAnnualDeductibleAmt,})
            #return render(request, 'patientviewbyid.html')
        else:
            return render(request, 'viewbyid.html')
    else:
        return render(request, 'viewbyid.html')
    


def patientviewbyid(request):
    id=request.session['id']
    print('id is',id)
    cr = Patient.objects.get(id=id)
    agemail= cr.agemail
    # Provider= cr.Provider
    BeneficiaryId= cr.BeneficiaryId
    InscClaimAmtReimbursed=cr.InscClaimAmtReimbursed
    DeductibleAmtPaid =cr.DeductibleAmtPaid
    PotentialFraud=cr.PotentialFraud
    gender=cr.gender
    race=cr.race
    RenalDiseaseIndicator=cr.RenalDiseaseIndicator
    NoOfMonths_PartACov=cr.NoOfMonths_PartACov
    NoOfMonths_PartBCov=cr.NoOfMonths_PartBCov
    ChronicCond_Alzheimer=cr.ChronicCond_Alzheimer
    ChronicCond_Heartfailure=cr.ChronicCond_Heartfailure
    ChronicCond_KidneyDisease=cr.ChronicCond_KidneyDisease
    ChronicCond_Cancer=cr.ChronicCond_Cancer
    ChronicCond_ObstrPulmonary=cr.ChronicCond_ObstrPulmonary
    ChronicCond_Depression=cr.ChronicCond_Depression
    ChronicCond_Diabetes=cr.ChronicCond_Diabetes
    ChronicCond_IschemicHeart=cr.ChronicCond_IschemicHeart
    ChronicCond_Osteoporasis=cr.ChronicCond_Osteoporasis
    ChronicCond_rheumatoidarthritis=cr.ChronicCond_rheumatoidarthritis
    ChronicCond_stroke=cr.ChronicCond_stroke
    IPAnnualReimbursementAmt=cr.IPAnnualReimbursementAmt
    IPAnnualDeductibleAmt=cr.IPAnnualDeductibleAmt
    OPAnnualReimbursementAmt=cr.OPAnnualReimbursementAmt
    OPAnnualDeductibleAmt=cr.OPAnnualDeductibleAmt
    
            
    return render(request, 'patientviewbyid.html',{'agemail':agemail,
                                                #    'Provider': Provider,
                                                   'BeneficiaryId': BeneficiaryId,
                                                   'InscClaimAmtReimbursed':InscClaimAmtReimbursed,
                                                   'DeductibleAmtPaid':DeductibleAmtPaid,
                                                   'PotentialFraud':PotentialFraud,
                                                    'gender':gender,
                                                    'race':race,
                                                    'RenalDiseaseIndicator':RenalDiseaseIndicator,
                                                    'NoOfMonths_PartACov':NoOfMonths_PartACov,
                                                    'NoOfMonths_PartBCov':NoOfMonths_PartBCov,
                                                    'ChronicCond_Alzheimer':ChronicCond_Alzheimer,
                                                    'ChronicCond_Heartfailure':ChronicCond_Heartfailure,
                                                    'ChronicCond_KidneyDisease':ChronicCond_KidneyDisease,
                                                    'ChronicCond_Cancer':ChronicCond_Cancer,
                                                    'ChronicCond_ObstrPulmonary':ChronicCond_ObstrPulmonary,
                                                    'ChronicCond_Depression':ChronicCond_Depression,
                                                    'ChronicCond_Diabetes':ChronicCond_Diabetes,
                                                    'ChronicCond_IschemicHeart':ChronicCond_IschemicHeart,
                                                    'ChronicCond_Osteoporasis':ChronicCond_Osteoporasis,
                                                    'ChronicCond_rheumatoidarthritis':ChronicCond_rheumatoidarthritis,
                                                    'ChronicCond_stroke':ChronicCond_stroke,
                                                    'IPAnnualReimbursementAmt':IPAnnualReimbursementAmt,
                                                    'IPAnnualDeductibleAmt':IPAnnualDeductibleAmt,
                                                    'OPAnnualReimbursementAmt':OPAnnualReimbursementAmt,
                                                    'OPAnnualDeductibleAmt':OPAnnualDeductibleAmt,})
       
def uploadform(request):
    agemail = request.session.get('agemail')
    next_beneficiary_id = None 
    next_beneficiary_id =request.session.get('next_beneficiary_id')
    if request.method=="POST":
        agemail = request.POST.get("agemail")
        # BeneficiaryId = request.POST.get("BeneficiaryId")
        # if Patient.objects.filter(BeneficiaryId=BeneficiaryId).exists():
        #     # Patient with the same BeneficiaryId already exists, so display an error message
        #     error_message = "A patient with the same BeneficiaryId already exists."
        #     return render(request, 'error.html')
        # provider = request.POST.get('provider')
         # Generate the next BeneficiaryId
        last_patient = Patient.objects.order_by('-BeneficiaryId').first()
        print(last_patient)
        if last_patient:
            last_id = int(last_patient.BeneficiaryId[4:])  
            next_id = last_id + 1
            next_beneficiary_id = f'BENE{next_id:04d}' 
        else:
            next_beneficiary_id = 'BENE1001'
            print(next_beneficiary_id)  # Add this line to check the value of next_beneficiary_id
        print(agemail)
         # Add this line to check the value of
            
        InscClaimAmtReimbursed = float(request.POST.get('InscClaimAmtReimbursed'))
        DeductibleAmtPaid = float(request.POST.get('DeductibleAmtPaid'))
        PotentialFraud = float(request.POST.get('PotentialFraud'))
        gender = float(request.POST.get('gender'))
        race = float(request.POST.get('race'))
        
        RenalDiseaseIndicator = float(request.POST.get('RenalDiseaseIndicator'))
        NoOfMonths_PartACov = float(request.POST.get('NoOfMonths_PartACov'))
        NoOfMonths_PartBCov = float(request.POST.get('NoOfMonths_PartBCov'))
        ChronicCond_Alzheimer = float(request.POST.get('ChronicCond_Alzheimer', 0))  # Default value provided
        ChronicCond_Heartfailure = float(request.POST.get('ChronicCond_Heartfailure', 0))  # Default value provided
        ChronicCond_KidneyDisease = float(request.POST.get('ChronicCond_KidneyDisease', 0))  # Default value provided
        ChronicCond_Cancer = float(request.POST.get('ChronicCond_Cancer', 0))  # Default value provided
        ChronicCond_ObstrPulmonary = float(request.POST.get('ChronicCond_ObstrPulmonary', 0))  # Default value provided
        ChronicCond_Depression = float(request.POST.get('ChronicCond_Depression', 0))  # Default value provided
        ChronicCond_Diabetes = float(request.POST.get('ChronicCond_Diabetes', 0))  # Default value provided
        ChronicCond_IschemicHeart = float(request.POST.get('ChronicCond_IschemicHeart', 0))  # Default value provided
        ChronicCond_Osteoporasis = float(request.POST.get('ChronicCond_Osteoporasis', 0))  # Default value provided
        ChronicCond_rheumatoidarthritis = float(request.POST.get('ChronicCond_rheumatoidarthritis', 0))  # Default value provided
        ChronicCond_stroke = float(request.POST.get('ChronicCond_stroke', 0))  # Default value provided
        Numberofdaysadmitted= float(request.POST.get('Numberofdaysadmitted'))
        IPAnnualReimbursementAmt = float(request.POST.get('IPAnnualReimbursementAmt'))
        IPAnnualDeductibleAmt = float(request.POST.get('IPAnnualDeductibleAmt'))
        OPAnnualReimbursementAmt = float(request.POST.get('OPAnnualReimbursementAmt'))
        OPAnnualDeductibleAmt = float(request.POST.get('OPAnnualDeductibleAmt'))
        current_agent = agent.objects.get(agemail=agemail)
        Patient(agemail=current_agent, 
                BeneficiaryId=next_beneficiary_id,
                # provider=provider,
                InscClaimAmtReimbursed=InscClaimAmtReimbursed,
                DeductibleAmtPaid=DeductibleAmtPaid,
                PotentialFraud=PotentialFraud,
                gender=gender,
                race=race,
                RenalDiseaseIndicator=RenalDiseaseIndicator,
                NoOfMonths_PartACov=NoOfMonths_PartACov,
                NoOfMonths_PartBCov=NoOfMonths_PartBCov,
                ChronicCond_Alzheimer=ChronicCond_Alzheimer,
                ChronicCond_Heartfailure=ChronicCond_Heartfailure,
                ChronicCond_KidneyDisease=ChronicCond_KidneyDisease,
                ChronicCond_Cancer=ChronicCond_Cancer,
                ChronicCond_ObstrPulmonary=ChronicCond_ObstrPulmonary,
                ChronicCond_Depression=ChronicCond_Depression,
                ChronicCond_Diabetes=ChronicCond_Diabetes,
                ChronicCond_IschemicHeart=ChronicCond_IschemicHeart,
                ChronicCond_Osteoporasis=ChronicCond_Osteoporasis,
                ChronicCond_rheumatoidarthritis=ChronicCond_rheumatoidarthritis,
                ChronicCond_stroke=ChronicCond_stroke,
                Numberofdaysadmitted=Numberofdaysadmitted,
                IPAnnualReimbursementAmt=IPAnnualReimbursementAmt,
                IPAnnualDeductibleAmt=IPAnnualDeductibleAmt,
                OPAnnualReimbursementAmt=OPAnnualReimbursementAmt,
                OPAnnualDeductibleAmt=OPAnnualDeductibleAmt).save()
        return render(request,'agenthome.html',{'agemail': agemail,'next_beneficiary_id': next_beneficiary_id})
    else:
        return render(request, 'uploadform.html',{'agemail': agemail,'next_beneficiary_id': next_beneficiary_id})

