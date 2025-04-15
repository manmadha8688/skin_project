from django.shortcuts import render,redirect
from .models import reviews

# Create your views here.
def add_review(request):
    if request.method == 'POST':
        ratting = int(request.POST['rating'])
        dis = request.POST['feedback']
        
        review = reviews(ratting=ratting,discription=dis,by=request.user.name)
        review.save()
        return redirect('/')
    
    return render(request,'/')
