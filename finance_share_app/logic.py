from finance_share_app.models import *
import datetime


def get_default_date_range(offset=0):
    # produces the month daterange that you are in
    # offset will be the amount of months back you want to move your range

    today = datetime.datetime.now()

    if today.day >= 25:
        if today.month == 12:
            enddate = today.replace(month=1, year=today.year+1, day=25)
        else:
            enddate = today.replace(month=today.month+1, day=25)
        startdate = today.replace(day=26)
    else:
        enddate = today.replace(day=25)
        if today.month == 1:
            startdate = today.replace(month=12, year=today.year-1, day=26)
        else:
            startdate = today.replace(month=today.month-1, day=26)

    daterange = {'start_date': startdate.date(), 'end_date': enddate.date()}
    return (daterange)


def calculate_owed_to_user(user, daterange):
    docs = Document.objects.filter(owner=user,
                                   created_date__range=[daterange.get('start_date'), daterange.get('end_date')])
    totals = {}
    for doc in docs:
        claims = Claim.objects.filter(docref=doc)
        for claim in claims:
            for share in UserClaimAllocate.objects.filter(claim=claim):
                if share.user != user:
                    if share.user in totals:
                        totals[share.user] += share.share_amount
                    else:
                        totals[share.user] = share.share_amount
    return (totals)


def calculate_owed_by_user(user, daterange):
    toshare = UserClaimAllocate.objects.filter(user=user,
                                               claim__docref__created_date__range=[daterange.get('start_date'),
                                                                                   daterange.get('end_date')])
    totals = {}
    for share in toshare:
        if user != share.claim.docref.owner:
            if share.claim.docref.owner in totals:
                totals[share.claim.docref.owner] += share.share_amount
            else:
                totals[share.claim.docref.owner] = share.share_amount
    return (totals)


def calculate_final_out(owedbyuser, owedtouser):
    finalout = {}
    for user in owedbyuser:
        if user in owedtouser:
            result = owedtouser[user] - owedbyuser[user]
        else:
            result = owedbyuser[user] * (-1)
        finalout[user] = result

    for user in owedtouser:
        if user not in finalout:
            finalout[user] = owedtouser[user]

    return (finalout)


def compile_report(owedbyuser, owedtouser, finalout):
    return ({'owedbyuser': owedbyuser, 'owedtouser': owedtouser, 'finalout': finalout})


def add_edit_claim_share(claim, shares):
    #clear current shares for the current claim
    UserClaimAllocate.objects.filter(claim=claim).delete()


    #write new sahre entries
    for user in shares:
        UserClaimAllocate.objects.create(user=user, claim=claim)
    count = UserClaimAllocate.objects.filter(claim=claim).count()
    UserClaimAllocate.objects.filter(claim=claim).update(share_amount=int(claim.amount) / count)
