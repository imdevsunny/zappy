from django.db import models
from django.conf import settings
# Create your models here.


class ChatBot(models.Model):
    MODEL_TYPES = [
        ('GPT-3(Legacy)', 'GPT-3(Legacy)'),
        ('GPT-4', 'GPT-4'),
        ('GPT-4 Turbo', 'GPT-4 Turbo'),
        ('GPT-4o', 'GPT-4o'),
        ('GPT-4o-mini', 'GPT-4o-mini'),
    ]
    ROLE_TYPES = [
        ('Business Analyst', 'Business Analyst'),
        ('Customer Service Representative', 'Customer Service Representative'),
        ('Fitness Instructor', 'Fitness Instructor') ,
        ('Educational Tutor', 'Educational Tutor') ,
        ('Entertainment Host', 'Entertainment Host') ,
        ('Healthcare Assistant', 'Healthcare Assistant') ,
        ('Technical Helpdesk', 'Technical Helpdesk') ,
        ('Artistic Consultant', 'Artistic Consultant') ,
    ]
    PERSONALITY_TYPES = [
        ('Professional & Efficient', 'Professional & Efficient'),
        ('Friendly & Responsive', 'Friendly & Responsive'),
        ('Analytical & Trustworthy', 'Analytical & Trustworthy'),
        ('Motivational & Energetic', 'Motivational & Energetic'),
        ('Witty & Sarcastic', 'Witty & Sarcastic'),
        ('Compassionate & Knowledgeable', 'Compassionate & Knowledgeable'),
        ('Technical & Patient', 'Technical & Patient'),
        ('Innovative & Creative', 'Innovative & Creative'),
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255,choices=MODEL_TYPES, null=True, blank=True)
    role = models.CharField(max_length=255,choices=ROLE_TYPES, null=True, blank=True)
    personality = models.CharField(max_length=255, choices=PERSONALITY_TYPES, null=True, blank=True)
    image = models.ImageField(upload_to='bot_pics', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}, {self.user.email}"