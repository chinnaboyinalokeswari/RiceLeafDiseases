from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import UserRegistrationModel

# Create your views here.
def AdminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/AdminHome.html')

        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'AdminLogin.html', {})


def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def RegisterUsersView(request):
    data = UserRegistrationModel.objects.all()
    return render(request,'admins/viewregisterusers.html',{'data':data})


def ActivaUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        UserRegistrationModel.objects.filter(id=id).update(status=status)
        data = UserRegistrationModel.objects.all()
        return render(request,'admins/viewregisterusers.html',{'data':data})


def AdminViewResults(request):
    import pandas as pd
    from users.utility import RiceLeaf_Classification
    rf_report = RiceLeaf_Classification.process_randomForest()
    dt_report = RiceLeaf_Classification.process_decesionTree()
    nb_report = RiceLeaf_Classification.process_naiveBayes()
    gb_report = RiceLeaf_Classification.process_gradientBoosting()
    rf_report = pd.DataFrame(rf_report).transpose()
    rf_report = pd.DataFrame(rf_report)
    dt_report = pd.DataFrame(dt_report).transpose()
    dt_report = pd.DataFrame(dt_report)
    nb_report = pd.DataFrame(nb_report).transpose()
    nb_report = pd.DataFrame(nb_report)
    gb_report = pd.DataFrame(gb_report).transpose()
    gb_report = pd.DataFrame(gb_report)
    # report_df.to_csv("rf_report.csv")
    return render(request,'admins/ml_reports.html',{'rf': rf_report.to_html,'dt': dt_report.to_html,'nb':nb_report.to_html,'gb': gb_report.to_html})



