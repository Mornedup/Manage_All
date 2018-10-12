from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ClaimUploadForm
from django.utils import timezone
from .models import Claim
from authapp.models import CUser
from allocations.models import *

# Create your views here.
@login_required
def makeclaim(request):
    if request.method == 'POST':
        claimForm = ClaimUploadForm(request.POST)
        if (claimForm.is_valid()):
            claim = claimForm.save(commit=False)
            claim.owner = request.user
            claim.created_date = timezone.now()
            claim.save()
            for user in CUser.objects.filter(pk__in=request.POST.getlist('checkbox')):
                userclaim = UserClaimAllocate.objects.create(user=user, claim=claim)
            count=UserClaimAllocate.objects.filter(claim=claim).count()
            UserClaimAllocate.objects.filter(claim=claim).update(share_ammount=claim.ammount/(count))
            return redirect('claims_list')
    else:
        claimform = ClaimUploadForm()
        return render(request, 'claimsmanage/makeclaim.html', {'claimform': claimform, 'users':CUser.objects.all()})

@login_required
def view_claimslist(request):
    return render(request, 'claimsmanage/list_claims.html', {'claims': Claim.objects.filter(owner=request.user)})

@login_required
def view_claim(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    users = UserClaimAllocate.objects.filter(claim=claim)
    return render(request, 'claimsmanage/view_claim.html', {'claim': claim, 'users':users})
