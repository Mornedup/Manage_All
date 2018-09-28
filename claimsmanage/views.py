from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClaimUploadForm
from django.utils import timezone
from .models import Claim

# Create your views here.
@login_required
def makeclaim(request):
    if request.method == 'POST':
        ClaimForm = ClaimUploadForm(request.POST)
        if (ClaimForm.is_valid()):
            claim = ClaimForm.save(commit=False)
            claim.owner = request.user
            claim.created_date = timezone.now()
            claim.save()
            return redirect('claims_list')
    else:
        form = ClaimUploadForm()
        print(form)
        return render(request, 'claimsmanage/makeclaim.html', {'form': form})

@login_required
def view_claim(request):
    return render(request, 'claimsmanage/list_claims.html', {'claims': Claim.objects.all()})

"""@login_required


        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'BaseTemplate': BlogConfig.BaseTemplate})"""
