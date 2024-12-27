from authentication.models import User

def isSellerPermission(request):
    return request.user.is_authenticated and request.user.account_type == User.AccountTypes.SELLER

def hasStorePermission(request):
    return isSellerPermission(request) and request.user.stores.exists()