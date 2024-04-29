from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class reg(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    pwd = models.CharField(max_length=15)
    cpwd = models.CharField(max_length=15)
    gender = models.CharField(max_length=6)
      # Add field for approval status


class adminreg(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    password = models.CharField(max_length=10)
        # validators=[
        #     RegexValidator(
        #         regex=r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,}',
        #         message='Password must contain at least 8 characters, including at least one lowercase letter, one uppercase letter, one digit, and one special character.',
        #     ),
        # ]
    

class agent(models.Model):
    agname=models.CharField(max_length=40)
    agemail=models.EmailField(max_length=40)
    password=models.CharField(max_length=10)
    phone=models.IntegerField()
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.agemail




class Patient(models.Model):
    agemail=models.EmailField(max_length=40)
    BeneficiaryId = models.CharField(max_length=40, unique=True)
    provider = models.CharField(max_length=100)
    InscClaimAmtReimbursed = models.DecimalField(max_digits=10, decimal_places=2)
    DeductibleAmtPaid = models.DecimalField(max_digits=10, decimal_places=2)
    PotentialFraud = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    race = models.CharField(max_length=50)
    RenalDiseaseIndicator = models.CharField(max_length=10)
    NoOfMonths_PartACov = models.IntegerField()
    NoOfMonths_PartBCov = models.IntegerField()
    ChronicCond_Alzheimer = models.BooleanField(default=False)
    ChronicCond_Heartfailure = models.BooleanField(default=False)
    ChronicCond_KidneyDisease = models.BooleanField(default=False)
    ChronicCond_Cancer = models.BooleanField(default=False)
    ChronicCond_ObstrPulmonary = models.BooleanField(default=False)
    ChronicCond_Depression = models.BooleanField(default=False)
    ChronicCond_Diabetes = models.BooleanField(default=False)
    ChronicCond_IschemicHeart = models.BooleanField(default=False)
    ChronicCond_Osteoporasis = models.BooleanField(default=False)
    ChronicCond_rheumatoidarthritis = models.BooleanField(default=False)
    ChronicCond_stroke = models.BooleanField(default=False)
    IPAnnualReimbursementAmt = models.DecimalField(max_digits=10, decimal_places=2)
    IPAnnualDeductibleAmt = models.DecimalField(max_digits=10, decimal_places=2)
    OPAnnualReimbursementAmt = models.DecimalField(max_digits=10, decimal_places=2)
    OPAnnualDeductibleAmt = models.DecimalField(max_digits=10, decimal_places=2)
    prediction_result=models.CharField(max_length=100)
    Numberofdaysadmitted=models.IntegerField()
    def save(self, *args, **kwargs):
        if not self.BeneficiaryId:
            last_beneficiary = Patient.objects.order_by('-BeneficiaryId').first()
            if last_beneficiary:
                last_id = int(last_beneficiary.BeneficiaryId[4:])  # Extract the numeric part
                new_id = last_id + 1
            else:
                new_id = 1001  # If no patients exist yet, start from 1001
            self.BeneficiaryId = f"BENE{new_id:04d}"  # Format the new id
        super(Patient, self).save(*args, **kwargs)
    def __str__(self):
        return self.BeneficiaryId  # Return the provider name when the object is printed



class Providers(models.Model):
    provideno=models.CharField(max_length=100)
    result=models.CharField(max_length=30)

class PredictionResult(models.Model):
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)