from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """Custom authentication backend that allows login with email."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            
            user = User.objects.filter(email=username).first()
            
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            
            return user
        return None
