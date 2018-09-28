class AllocationForm(UserCreationForm):

    class Meta:
        model=Allocation
        fields = (
        'owner',
        'description',
        'total_ammount',
        'created_date',
        'start_date'
        'end_date',
        'claim_list',
        )
