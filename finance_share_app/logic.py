from django.utils import timezone
from finance_share_app.models import *

def get_default_date_range(offset=0):
    # offset will be the ammount of months back you want to move your range
    startdate = timezone.now()
    startdate.replace(month=startdate.month+offset)
    if startdate.month==1:
        startdate.replace(year=startdate.year-1, month=12, day=26)
    else:
        startdate.replace(month=startdate.month-1, day=26)

    enddate= timezone.now()
    if enddate.month==1:
        enddate.replace(year=enddate.year-1, month=12, day=26)
    else:
        enddate.replace(day=25)

    return ({'start_date':startdate.date(), 'end_date':enddate.date()})

def calculate_owed_to_user(user, daterange):
    docs = Document.objects.filter(owner=user, created_date__range=[daterange.get('start_date'), daterange.get('end_date')])
    totals={}
    for doc in docs:
        claims = Claim.objects.filter(docref=doc)
        for claim in claims:
            for share in UserClaimAllocate.objects.filter(claim=claim):
                if share.user != user:
                    if share.user in totals:
                        totals[share.user]+=share.share_ammount
                    else:
                        totals[share.user]=share.share_ammount
    print(totals)
    return (totals)

def calculate_owed_by_user(user, daterange):
    toshare=UserClaimAllocate.objects.filter(user=user, claim__docref__created_date__range=[daterange.get('start_date'), daterange.get('end_date')])
    totals={}
    for share in toshare:
        if user != share.claim.docref.owner:
            if share.claim.docref.owner in totals:
                totals[share.claim.docref.owner]+=share.share_ammount
            else:
                totals[share.claim.docref.owner]=share.share_ammount
    return (totals)

def calculate_final_out(owedbyuser, owedtouser):
    finalout = {}
    for user in owedbyuser:
        if user in owedtouser:
            result = owedtouser[user]-owedbyuser[user]
        else:
            result = owedbyuser[user]*(-1)
        finalout[user] = result

    for user in owedtouser:
        if user not in finalout:
            finalout[user] = owedtouser[user]

    return(finalout)

def compile_report(user, owedbyuser, owedtouser, finalout):
    return ({'owedbyuser':owedbyuser, 'owedtouser':owedtouser, 'finalout':finalout})
