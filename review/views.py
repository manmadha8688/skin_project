from django.shortcuts import render,redirect
from .models import reviews

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def add_review(request):
    if request.method == 'POST':
        ratting = int(request.POST['rating'])
        dis = request.POST['feedback']
        
        review = reviews(ratting=ratting,discription=dis,by=request.user.name)
        review.save()
        return redirect('/')
    
    return render(request,'/')
