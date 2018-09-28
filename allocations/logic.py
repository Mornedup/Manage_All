from django.utils import timezone
from .models import Allocation
from .forms import AllocationForm

def GetDefaultStartDate():
    sd = timezone.now
    if sd.month=1:
        sd.replace(year=sd.year-1, month=12, day=26)
    else:
        sd.replace(month=sd.month-1, day=26)

def share_calc(sharepartners, total):
    return total/(count sharepartners)

def allocate(user, description, startdate, enddate):
    claimlist = get all from claims database that contains "user"
    claimlist = []
    total=0
    for claim in claimlist
        if claim.owner == claim.docref_id.owner
        total += share_calc(claim.alocate_to, claim.ammount)
        claim_list.append(claim.identifier)

    form = AllocationForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()



    return render(request, 'blog/post_edit.html', {'form': form, 'BaseTemplate': BlogConfig.BaseTemplate})
    created entry in allocation database
        set the user =owner
        set description
        set start and end dates
        set total_ammount
        set list of claims in claim_list
