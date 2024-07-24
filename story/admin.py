from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Plan, UserPlan, Widget,Story, DiscountCode, Payment, Viewer
from .forms import UserCreationForm, UserChangeForm



# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'api_key')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
#کلا تاپل شوند 
class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'is_active', 'max_stories', 'max_widgets','stories_per_widget', 'created_at', 'updated_at')
    list_filter = ('price', 'is_active', 'max_stories', 'max_widgets', 'stories_per_widget')
    search_fields = ('title','description')

class UserPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'Plan','created_at', 'updated_at')
    list_filter = ('user', 'Plan')
    search_fields = ('user__email', 'plan__title')

class WidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'enable', 'shape', 'title_position', 'align', 'created_at', 'updated_at')
    list_filter = ('user', 'enable', 'shape', 'title_position', 'align')
    search_fields = ('title', 'user')

class StoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'content', 'user', 'widget', 'duration', 'next_story','previous_story','is_deleted', 'created_at', 'updated_at')
    list_filter = ('type', 'user', 'widget')
    search_fields = ('type', 'user')

class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'value', 'max_use', 'created_at', 'updated_at')
    list_filter = ('title','type', 'value', 'max_use')
    search_fields = ('title','type')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'discount_code', 'price', 'plan', 'status', 'gateway','tracking_code', 'created_at', 'updated_at')
    list_filter = ('user','discount_code', 'price', 'plan', 'status', 'gateway','tracking_code')
    search_fields = ('user','price','plan')

class ViewerAdmin(admin.ModelAdmin):
    list_display = ('viewer_session', 'story', 'os', 'client', 'created_at', 'updated_at')
    list_filter = ('viewer_session', 'story', 'os', 'client')
    search_fields = ('story','os','client')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(DiscountCode,DiscountCodeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Viewer, ViewerAdmin)

    #ordering = ('email',)
   # filter_horizontal = ('customuser_groups', 'customuser_user_permissions',)