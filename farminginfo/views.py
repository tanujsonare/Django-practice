from django.shortcuts import redirect, render 
from django.contrib import messages
# from  farminginfo.models import crops_info
from  farminginfo.models import crop_detail
from  farminginfo.models import account_info
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

    
def register(request):
    # print("Inside register")
    if request.method == 'POST':
        # print("Inside post")
        login_data = request.POST.dict()
        print(login_data)
        fullname = request.POST['fullname']
        # print(fullname) 
        email = request.POST['email'] 
        password = request.POST['password'] 
        retypepassword = request.POST['retypepassword']
        
        
        if (password == retypepassword and email == email):
            account_info.objects.create(fullname=fullname, email=email, password=password,date_of_creation = datetime.now(),date_of_modification = datetime.now())
            messages.success(request,'you are register successfully..') 
            return redirect('login')
        
        else:
            messages.warning(request,'both password are not matched or email already exist!!!!')
        
    return render(request,'webpages/register.html')
    #return redirect('register')

def login(request):
    print(request.session.has_key("logged_in"))
    if request.session.has_key('logged_in'):
        print("Login inside")
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        count = (account_info.objects.filter(email= email,password=password).count())
        if count>0:
            request.session['logged_in'] = True
            request.session['username'] = email
            messages.success(request,'you are logged in.')
            
            return redirect('home')
        # if (account_info.objects.filter(email = email,password = password).exists()):
        #     messages.success(request,'you are logged in..')
        #     return redirect('home')
        else:
            messages.warning(request, "Your password or email is not valid !!")
            return redirect('login')
            
    return render(request,'webpages/login.html')


def home(request):
    if request.session.has_key('logged_in'):
        # print("I am inside home")
        # print(request.session['logged_in'])
        # print(request.session.get('username'))
        username = request.session.get('username')
        # count = crop_detail.objects.values('Crop').distinct().count()
        # print(count)
        l = []        
        information = crop_detail.objects.values('Crop').distinct()
        
        for x in information:
            for i in x:
                l.append(x[i])
    
        list1 = [] 
        n = 0
        for x in l:
            information1 = crop_detail.objects.filter(Crop = l[n]).aggregate(Sum('Area'))
            list1.append(information1)
            n = n + 1

        
        list2 = [] 
        n = 0
        for x in l:
            information1 = crop_detail.objects.filter(Crop = l[n]).aggregate(Sum('Production'))
            list2.append(information1)
            n = n + 1

        list_area = []
        for y in list1:
            for z in y:
                list_area.append(y[z])
        
        list_production = []
        for y in list2:
            for z in y:
                list_production.append(y[z])
        
        list_id = []
        n = 0
        for x in l:
            id = crop_detail.objects.filter(Crop=l[n]).values('id')[0]['id']
            # print(id)
            list_id.append(id)
            n = n + 1
        
        mylist = zip(l,list_area,list_production,list_id)
        
        page = request.GET.get('page', 1)

        paginator = Paginator(list(mylist), 12)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        dict1 = {'username' :username,'mylist': mylist,'users' : users}
        return render(request,'webpages/home.html',dict1)
    return redirect('login')   

def product(request,id):
    list = []
    crop_name = crop_detail.objects.filter(id=id).values('Crop')
    for c in crop_name:
        for i in c:
            list.append(c[i])
    cropname_detail = crop_detail.objects.filter(Crop__in = list).values('Crop')
    state_detail = crop_detail.objects.filter(Crop__in = list).values('State_Name')
    district_detail = crop_detail.objects.filter(Crop__in = list).values('District_Name')
    season_detail = crop_detail.objects.filter(Crop__in = list).values('Season')
    cropyear_detail = crop_detail.objects.filter(Crop__in = list).values('Crop_Year')
    area_detail = crop_detail.objects.filter(Crop__in = list).values('Area')
    production_detail = crop_detail.objects.filter(Crop__in = list).values('Production')

    cropname = []
    for c in cropname_detail:
        for i in c:
            cropname.append(c[i])

    statename = []
    for c in state_detail:
        for i in c:
            statename.append(c[i])
    
    districtname = []
    for c in district_detail:
        for i in c:
            districtname.append(c[i])

    seasonname = []
    for c in season_detail:
        for i in c:
            seasonname.append(c[i])

    cropyear = []
    for c in cropyear_detail:
        for i in c:
            cropyear.append(c[i])

    area = []
    for c in area_detail:
        for i in c:
            area.append(c[i])

    production = []
    for c in production_detail:
        for i in c:
            production.append(c[i])

    total_area = []
    t_area = crop_detail.objects.filter(Crop__in = list).aggregate(Sum('Area')) 
    for x in t_area:
       total_area.append(t_area[x])
        
    total_production= [] 
    t_production = crop_detail.objects.filter(Crop__in = list).aggregate(Sum('Production'))
    for x in t_production:
        total_production.append(t_production[x])

   
    display_list = zip(cropname,statename,districtname,seasonname,cropyear,area,production)
    data = {'display_list' : display_list,'total_area':total_area[0],'total_production':total_production[0]}
    return render(request,'webpages/product.html',data)


         

        
def logout(request):
    # print("logout")
    # print(request.session['logged_in'])
    del request.session['logged_in']
    # print("completed")
    return redirect('login')    



        



    
