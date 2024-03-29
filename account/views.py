from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from social_group.models import SocialGroupPost, SocialGroupMember
from .models import Notification
from .serializers import NotificationSerializer
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, CustomPasswordChangeForm
from django.shortcuts import get_object_or_404
from social_group.models import SocialGroup


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            # print(email, password)
            if user is not None:
                login(request, user)
                print('logged in')
                return redirect('dashboard')  # Redirect to the 'dashboard' named URL
            else:
                print('not logged in')
        return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')  # Redirect to login page after logout


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        # Get all social groups where the user is a member
        social_groups = SocialGroupMember.objects.filter(user=request.user).values_list('social_group', flat=True)
        # Get all posts related to these social groups
        posts = SocialGroupPost.objects.filter(social_group__in=social_groups).select_related('user',
                                                                                              'social_group').order_by(
            '-created_at')

        # Get notifications for the user, both the queryset for template rendering and the serialized data for potential JS use
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        notifications_serialized = NotificationSerializer(notifications, many=True).data

        context = {
            'posts': posts,
            'notifications': notifications,  # Raw queryset for template
            'notifications_serialized': notifications_serialized,  # Serialized data
            'user': request.user
        }
        return render(request, self.template_name, context)


class UserSettingsView(LoginRequiredMixin, View):
    template_name = 'user_settings.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'delete_account.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()  # Usunięcie konta
        logout(request)  # Wylogowanie użytkownika po usunięciu konta
        return redirect('home')  # Przekierowanie na stronę główną


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'change_password.html'

    def get(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomPasswordChangeForm(request.user, request.POST)
        print(form.errors)  # Dodaj to, aby sprawdzić błędy formularza w konsoli
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password was successfully updated.')
            return redirect('user_settings')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})


class DeleteNotificationView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        notification_id = self.kwargs.get('notification_id')
        # Ensure that the notification belongs to the user
        notification = Notification.objects.filter(id=notification_id, user=request.user)
        if notification.exists():
            notification.delete()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            # If the notification does not exist or does not belong to the user
            return JsonResponse({'status': 'failed', 'message': 'Notification not found or access denied.'}, status=404)


class AcceptInvitationView(LoginRequiredMixin, View):
    def post(self, request, social_group_id, notification_id):
        # Find the invitation notification
        invitation = get_object_or_404(Notification, id=notification_id, user=request.user, sg_id=social_group_id,
                                       is_invitation=True)
        # Find the social group
        group = get_object_or_404(SocialGroup, id=social_group_id)

        # Add user to the social group
        SocialGroupMember.objects.create(user=request.user, social_group=group, role='member')

        # Optionally, you can delete the invitation notification after accepting
        invitation.delete()

        messages.success(request, "You have joined the group successfully.")
        return JsonResponse({'status': 'success'}, status=200)
