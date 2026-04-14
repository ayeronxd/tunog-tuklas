import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tunog_tuklas.settings')
django.setup()

from core.models import Level, UserLevelProgress
from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.order_by('-date_joined').first()
    if user:
        account = user.account
        
        # Complete M, I, O
        levels_to_complete = ["m", "i", "o"]
        for lname in levels_to_complete:
            lvl = Level.objects.filter(name__icontains=lname).first()
            if lvl:
                prog, _ = UserLevelProgress.objects.get_or_create(account=account, level=lvl)
                prog.is_completed = True
                prog.is_unlocked = True
                prog.stars_earned = 3
                prog.save()
                print(f"Completed {lvl.name}")
        
        # Unlock B
        lvl_b = Level.objects.filter(name__icontains="b").first()
        if lvl_b:
            prog_b, _ = UserLevelProgress.objects.get_or_create(account=account, level=lvl_b)
            prog_b.is_unlocked = True
            prog_b.save()
            print(f"Unlocked {lvl_b.name}")
            
        print(f"Successfully restored progress for {user.email}")
    else:
        print("No user found.")
except Exception as e:
    print(f"Error: {e}")
