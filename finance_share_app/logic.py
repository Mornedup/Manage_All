from finance_share_app.models import *
import datetime


def get_default_date_range(months=0, month_start=26, today=datetime.datetime.now().date()):
    if today.day >= month_start:
        start_date = today.replace(day=month_start)
        if today.month == 12:
            end_date = today.replace(month=1, year=today.year + 1, day=month_start)
        else:
            end_date = today.replace(month=today.month + 1, day=month_start)
    else:
        if today.month == 1:
            start_date = today.replace(month=12, year=today.year - 1, day=month_start)
        else:
            start_date = today.replace(month=today.month - 1, day=month_start)
        end_date = today.replace(day=month_start)
    if ((start_date.month + months) % 12):
        start_date = start_date.replace(month=(start_date.month + months) % 12,
                                    year=start_date.year + int((start_date.month + months-1) / 12))
    else:
        start_date = start_date.replace(month=12,
                                        year=start_date.year + int((start_date.month + months-1) / 12))
    if ((end_date.month + months) % 12):
        end_date = end_date.replace(month=(end_date.month + months) % 12,
                                year=end_date.year + int((end_date.month + months-1) / 12))
    else:
        end_date = end_date.replace(month=12,
                                    year=end_date.year + int((end_date.month + months-1) / 12))
    return {'start_date': start_date, 'end_date': end_date}


def add_edit_claim_share(claim, shares):
    # clear current shares for the current claim
    UserClaimAllocate.objects.filter(claim=claim).delete()
    # write new share entries
    for user in shares:
        UserClaimAllocate.objects.create(user=user, claim=claim)
    count = UserClaimAllocate.objects.filter(claim=claim).count()
    UserClaimAllocate.objects.filter(claim=claim).update(share_amount=float(claim.amount) / count)


# def claims_to_text(claims):
#     # get list of claims as par and return a string with names for display
#     claimstr = ''
#     for claim in claims:
#         claimstr = claimstr + str(claim.description) + ', '
#     claimstr = claimstr[0:-2]
#     return claimstr


class ClaimUtils(object):
    def __init__(self):
        pass

    def get_shares(self, claim_id):
        claim = self.get_claim(claim_id)
        users = UserClaimAllocate.objects.filter(claim=claim)
        users_shares = {}
        print(users)
        for user in users:
            share = UserClaimAllocate.objects.get(user=user.user, claim=claim)
            users_shares[user.user.id] = {'share': share.share_amount, 'name': user.user.get_full_name()}
            print(users_shares)
        return users_shares

    def get_claim(self, claim_id):
        return Claim.objects.get(pk=claim_id)

    def get_claims(self, document):
        return Claim.objects.filter(docref=document)

    def get_document(self, document_id):
        return Document.objects.get(pk=document_id)

    def get_documents(self, user=None, daterange=None):
        if user and not daterange:
            return Document.objects.filter(owner=user)
        if user and daterange:
            return Document.objects.filter(owner=user,
                                           created_date__range=[daterange.get('start_date'), daterange.get('end_date')])

    def claims_to_text(self, claims):
        # get list of claims as par and return a string with names for display
        claimstr = ''
        for claim in claims:
            claimstr = claimstr + str(claim.description) + ', '
        claimstr = claimstr[0:-2]
        return claimstr

    def get_userclaimallocates(self, user, daterange):
        return UserClaimAllocate.objects.filter(user=user,
                                                claim__docref__created_date__range=[daterange.get('start_date'),
                                                                                    daterange.get('end_date')])


class ReportUtils(ClaimUtils):
    def __init__(self):
        pass

    def calculate_owed_to_user(self, user, daterange):
        docs = self.get_documents(user, daterange)
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
        return totals

    def calculate_owed_by_user(self, user, daterange):
        toshare = self.get_userclaimallocates(user, daterange)
        totals = {}
        for share in toshare:
            if user != share.claim.docref.owner:
                if share.claim.docref.owner in totals:
                    totals[share.claim.docref.owner] += share.share_amount
                else:
                    totals[share.claim.docref.owner] = share.share_amount
        return totals

    def calculate_final_out(self, owedbyuser, owedtouser):
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
        return finalout

    def compile_report(self, owedbyuser, owedtouser, finalout):
        return {'owedbyuser': owedbyuser, 'owedtouser': owedtouser, 'finalout': finalout}

    def generate_report_data(self, user, daterange):
        owed_to_user = self.calculate_owed_to_user(user, daterange)
        owed_by_user = self.calculate_owed_by_user(user, daterange)
        final = self.calculate_final_out(owed_by_user, owed_to_user)
        return self.compile_report(owed_by_user, owed_to_user, final)
