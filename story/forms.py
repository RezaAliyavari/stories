from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from .models import User, Plan, UserPlan, Widget, DiscountCode, Payment, Viewer

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email',)

class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ('email',)


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'description', 'price', 'is_active', 'max_stories', 'max_widgets', 'stories_per_widget']

class UserPlanForm(forms.ModelForm):
    class Meta:
        model = UserPlan
        fields = ['user', 'Plan']

class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ['id', 'title', 'user', 'enable', 'shape', 'title_position', 'align']

class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = ['id', 'title', 'type', 'value', 'max_use']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'discount_code', 'price', 'plan', 'status', 'gateway','tracking_code']

class ViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = ['id', 'story', 'os', 'client']
