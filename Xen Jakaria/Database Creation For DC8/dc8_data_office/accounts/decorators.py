from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def sp_admin_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url='login'):
    '''
        Decorator for views that checks that the logged in user is a SP_ADMIN
        redirects to the log-in page if necessary.
        '''
    actual_decorators=user_passes_test(

        lambda u:u.profile.role.role_name=='SP_ADMIN',login_url=login_url,redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorators(function)

    return actual_decorators