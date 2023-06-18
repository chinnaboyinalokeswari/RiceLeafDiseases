# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def DatasetView(request):

    return render(request, 'users/viewdataset.html', {})


def UserClassification(request):
    import pandas as pd
    from .utility import RiceLeaf_Classification
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
    return render(request,'users/cl_reports.html',{'rf': rf_report.to_html,'dt': dt_report.to_html,'nb':nb_report.to_html,'gb': gb_report.to_html})


def UserPredictions(request):
    if request.method=='POST':
        image_file = request.FILES['file']
        # let's check if it is a csv file
        # if not image_file.name.endswith('.png'):
        #     messages.error(request, 'THIS IS NOT A PNG  FILE')
        fs = FileSystemStorage(location="media/rice_test/")
        filename = fs.save(image_file.name, image_file)
        # detect_filename = fs.save(image_file.name, image_file)
        uploaded_file_url = "/media/rice_test/" + filename  # fs.url(filename)
        print("Image path ", uploaded_file_url)
        from .utility.predections import predict_user_input
        result = predict_user_input(filename)
        print("Result=", result)
        return render(request, "users/UploadForm.html", {'path': uploaded_file_url,'result': result})
    else:
        return render(request, "users/UploadForm.html",{})
    return HttpResponse('working')