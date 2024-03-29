import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormMixin

from account.models import Notification
from account.models import User
from .forms import CommentForm
from .forms import SocialGroupEventForm
from .forms import SocialGroupForm
from .forms import SocialGroupPostForm
from .models import Comment
from .models import SocialGroup
from .models import SocialGroupEvent, SocialGroupEventMember
from .models import SocialGroupMember
from .models import SocialGroupPost


class SocialGroupsView(View):
    template_name = 'social_groups.html'

    def get(self, request, *args, **kwargs):
        search_my_groups = request.GET.get('search_my_groups', '')
        search_all_groups = request.GET.get('search_all_groups', '')

        # Get the complete list of group IDs for groups the user is a member of
        all_user_group_ids = SocialGroupMember.objects.filter(
            user=request.user
        ).values_list('social_group__id', flat=True)

        # User Groups with search functionality
        user_groups_query = Q(user=request.user)
        if search_my_groups:
            user_groups_query &= Q(social_group__name__icontains=search_my_groups)
        user_groups = SocialGroupMember.objects.filter(user_groups_query).select_related('social_group')

        # All Public Groups excluding user's groups with search functionality
        all_groups_query = Q(privacy='public')
        if search_all_groups:
            all_groups_query &= Q(name__icontains=search_all_groups)
        all_groups = SocialGroup.objects.filter(all_groups_query).exclude(id__in=all_user_group_ids)

        context = {
            'user_groups': [member.social_group for member in user_groups],
            'all_groups': all_groups
        }

        return render(request, self.template_name, context)


class CreateSocialGroupView(LoginRequiredMixin, CreateView):
    model = SocialGroup
    form_class = SocialGroupForm
    template_name = 'create_social_group.html'
    success_url = reverse_lazy('social_groups')  # Zaktualizuj, jeśli potrzebujesz innego URL

    def form_valid(self, form):
        form.instance.creator = self.request.user  # Zakładam, że masz pole 'creator' w modelu SocialGroup
        response = super().form_valid(form)  # Zapisz grupę
        # Dodaj użytkownika jako członka grupy z rolą 'admin'
        SocialGroupMember.objects.create(user=self.request.user, social_group=self.object, role='admin')
        return response


class JoinGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        group = get_object_or_404(SocialGroup, pk=group_id)
        # Sprawdź, czy użytkownik już nie jest członkiem grupy
        if not SocialGroupMember.objects.filter(user=request.user, social_group=group).exists():
            SocialGroupMember.objects.create(user=request.user, social_group=group, role='member')
        return redirect('social_groups')  # Zakładam, że 'social_groups' to nazwa URL do Twojej listy grup


class SocialGroupDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = SocialGroup
    template_name = 'social_group_detail.html'
    context_object_name = 'social_group'
    form_class = SocialGroupPostForm  # Assuming you want to create a post from the detail view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_group = self.get_object()

        # Get search query from the request
        search_query = self.request.GET.get('search_posts', '')

        # Filter posts based on the search query
        posts_query = Q(social_group=social_group)
        if search_query:
            posts_query &= (Q(user__first_name__icontains=search_query) |
                            Q(user__last_name__icontains=search_query) |
                            Q(content__icontains=search_query))
        posts = SocialGroupPost.objects.filter(posts_query).order_by('-created_at')

        context['posts'] = posts
        context['search_posts'] = search_query
        context['comment_form'] = CommentForm()  # For adding comments
        context['current_group_id'] = social_group.id
        self.request.session["current_group_id"] = social_group.id

        # Find the admin member of the social group
        user_membership = SocialGroupMember.objects.filter(
            user=self.request.user,
            social_group=social_group
        ).first()
        context['user_is_admin_or_moderator'] = user_membership.role in ['admin',
                                                                         'moderator'] if user_membership else False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the social group
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.social_group = self.get_object()
        post.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('social_group_detail', kwargs={'pk': self.object.pk})


class AddPostView(CreateView):
    model = SocialGroupPost
    form_class = SocialGroupPostForm
    template_name = 'create_post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_group_id'] = self.kwargs['social_group_id']  # Ensure this key matches your URL conf
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.social_group_id = self.kwargs['social_group_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('social_group_detail', kwargs={'pk': self.kwargs['social_group_id']})


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = get_object_or_404(SocialGroupPost, pk=post_id)
            comment.save()
            can_edit = request.user == comment.user or request.user.is_staff
            return JsonResponse({'status': 'success', 'comment_id': comment.id, 'comment': comment.content,
                                 'user': comment.user.get_full_name(), 'can_edit': can_edit})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})


@method_decorator(csrf_exempt, name='dispatch')
class EditCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        comment_id = data.get('id')
        content = data.get('content')

        try:
            comment = Comment.objects.get(pk=comment_id, user=request.user)  # Tylko autor może edytować komentarz
            comment.content = content
            comment.save()
            return JsonResponse({'status': 'success', 'content': content})
        except Comment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment not found or permission denied'}, status=404)


class DeletePostView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(SocialGroupPost, pk=kwargs['post_id'])
        if request.user == post.user or request.user.is_staff:
            post.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this post.'},
                                status=403)


@method_decorator(csrf_exempt, name='dispatch')
class EditPostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(SocialGroupPost, pk=post_id)
        if request.user == post.user or request.user.is_staff:
            data = json.loads(request.body)
            post.content = data['content']
            post.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Not authorized to edit this post'}, status=403)


class SocialGroupUsersView(LoginRequiredMixin, View):
    template_name = 'social_group_users.html'

    def get(self, request, social_group_id):
        search_members = request.GET.get('search_members', '')
        search_non_members = request.GET.get('search_non_members', '')

        social_group = get_object_or_404(SocialGroup, pk=social_group_id)

        # Get the complete list of members in the group without search filter
        all_member_ids = SocialGroupMember.objects.filter(
            social_group=social_group
        ).values_list('user__id', flat=True)

        # Members of the group with search functionality
        members_query = Q(social_group=social_group)
        if search_members:
            members_query &= (
                    Q(user__first_name__icontains=search_members) |
                    Q(user__last_name__icontains=search_members)
            )
        members = SocialGroupMember.objects.filter(members_query).select_related('user')

        # Users not in the group with search functionality
        non_members_query = Q()
        if search_non_members:
            non_members_query &= (
                    Q(first_name__icontains=search_non_members) |
                    Q(last_name__icontains=search_non_members)
            )
        non_members = User.objects.exclude(id__in=all_member_ids).filter(non_members_query)

        context = {
            'group': social_group,
            'members': members,
            'non_members': non_members,
            'search_members': search_members,
            'search_non_members': search_non_members,
            'current_group_id': social_group.id,
            'request_user_member_is_admin': SocialGroupMember.objects.get(social_group=social_group,
                                                                          user=request.user).role == 'admin'
        }
        return render(request, self.template_name, context)

    def post(self, request, social_group_id):
        # Assuming 'member_id' and 'new_role' are sent in POST request
        member_id = request.POST.get('member_id')
        new_role = request.POST.get('new_role')
        try:
            member = SocialGroupMember.objects.get(pk=member_id, social_group_id=social_group_id)
            member.role = new_role
            member.save()

            return JsonResponse({'success': True, 'message': 'Role updated successfully.'})
        except SocialGroupMember.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Member not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class InviteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        group_id = kwargs.get('social_group_id')
        added_user = get_object_or_404(User, pk=user_id)
        social_group = get_object_or_404(SocialGroup, pk=group_id)

        # Create an invitation
        if not Notification.objects.filter(user=added_user, sg_id=social_group).exists():
            # Create a notification for the invited user
            Notification.objects.create(
                user=added_user,
                sg_id=social_group,
                message=f"You have been invited to join the group {social_group.name}.",
                is_invitation=True
            )

            return JsonResponse({'status': 'success', 'message': 'User invited successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'User is already a member or has been invited'},
                                status=400)


class SocialGroupEventsView(View):
    template_name = 'social_group_events.html'

    def get(self, request, *args, **kwargs):
        social_group_id = kwargs.get('social_group_id')  # Zakładamy, że ID grupy jest przekazywane jako parametr URL

        # Wydarzenia użytkownika w tej grupie
        user_events = SocialGroupEventMember.objects.filter(
            user=request.user,
            event__social_group_id=social_group_id
        ).select_related('event')

        # Dostępne wydarzenia w tej grupie, do których użytkownik nie należy
        user_events_ids = user_events.values_list('event__id', flat=True)
        available_events = SocialGroupEvent.objects.filter(
            social_group_id=social_group_id
        ).exclude(id__in=user_events_ids)

        for membership in user_events:
            membership.event.is_organizer = membership.role == 'organizer'

        context = {
            'social_group_id': social_group_id,
            'user_events': [membership.event for membership in user_events],
            'available_events': available_events,
        }

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CreateSocialGroupEventView(View):
    form_class = SocialGroupEventForm
    template_name = 'create_social_group_event.html'

    def get(self, request, social_group_id, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'social_group_id': social_group_id})

    def post(self, request, social_group_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.social_group = SocialGroup.objects.get(pk=social_group_id)
            event.save()

            # Ustaw bieżącego użytkownika jako organizatora
            SocialGroupEventMember.objects.create(
                event=event,
                user=request.user,
                role='organizer'
            )

            return redirect('social_group_events', social_group_id=social_group_id)
        return render(request, self.template_name, {'form': form, 'social_group_id': social_group_id})


@method_decorator(login_required, name='dispatch')
class JoinEventView(View):
    def post(self, request, social_group_id, event_id):
        event = get_object_or_404(SocialGroupEvent, id=event_id, social_group_id=social_group_id)
        SocialGroupEventMember.objects.get_or_create(
            event=event,
            user=request.user,
            defaults={'role': 'participant'}
        )
        return redirect('social_group_events', social_group_id=social_group_id)


class DeleteEventView(LoginRequiredMixin, View):
    def post(self, request, social_group_id, event_id):
        event = get_object_or_404(SocialGroupEvent, id=event_id, social_group_id=social_group_id)

        # Sprawdź, czy użytkownik jest organizatorem wydarzenia
        is_organizer = SocialGroupEventMember.objects.filter(event=event, user=request.user,
                                                             role='organizer').exists()

        if is_organizer:
            event.delete()
            messages.success(request, 'Event has been deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this event.')

        return redirect(reverse('social_group_events', kwargs={'social_group_id': social_group_id}))


class LeaveGroupView(LoginRequiredMixin, View):
    def post(self, request, social_group_id):
        group = get_object_or_404(SocialGroup, pk=social_group_id)
        membership = SocialGroupMember.objects.filter(user=request.user, social_group=group).first()

        if membership:
            if membership.role == 'admin':  # Check if the user is an admin
                group.delete()  # Delete the whole group if the user is admin
                messages.success(request, "You were the admin. The group has been deleted successfully.")
            else:
                membership.delete()  # Delete the membership if the user is not an admin
                messages.success(request, "You have left the group successfully.")
        else:
            messages.error(request, "You are not a member of this group.")

        return redirect(reverse('social_groups'))  # Redirect to the list of groups or an appropriate view


@method_decorator(login_required, name='dispatch')
class DeleteGroupView(View):
    def post(self, request, group_id):  # Add 'group_id' argument
        social_group = get_object_or_404(SocialGroup, id=group_id)

        # Find the admin member of the social group
        admin_member = SocialGroupMember.objects.filter(social_group=social_group, role='admin',
                                                        user=request.user).first()

        if admin_member:
            social_group.delete()
            # Additional logic, such as sending notifications to group members, can be added here
        return redirect('social_groups')  # Redirect to the list of groups or an appropriate view


@method_decorator(login_required, name='dispatch')
class SocialGroupPostReportView(View):
    def post(self, request, social_group_id, post_id):
        post = get_object_or_404(SocialGroupPost, id=post_id, social_group_id=social_group_id)
        # Fetch moderators and admins
        responsible_members = SocialGroupMember.objects.filter(
            Q(social_group_id=social_group_id) &
            (Q(role='moderator') | Q(role='admin'))
        )

        message = f"The post created by {post.user.get_full_name()} has been reported by {request.user.get_full_name()}. The post contains such content: \"{post.content}\""

        # Create a notification for each moderator or admin
        for member in responsible_members:
            Notification.objects.get_or_create(
                user=member.user,
                sg_id=post.social_group,
                message=message,
                is_invitation=False
            )

        return JsonResponse(
            {"success": True, "message": "Report has been successfully submitted and moderators and admins notified."})


class PostCommentReport(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
        social_group = comment.post.social_group
        # Fetch moderators and admins
        responsible_members = SocialGroupMember.objects.filter(
            Q(social_group=social_group) &
            (Q(role='moderator') | Q(role='admin'))
        )

        message_template = "The comment created by {user} has been reported by {reporter}. The comment contains such content: \"{content}\""

        # Create a notification for each moderator or admin
        for member in responsible_members:
            Notification.objects.get_or_create(
                user=member.user,
                sg_id=social_group,
                message=message_template.format(user=comment.user.get_full_name(),
                                                reporter=request.user.get_full_name(), content=comment.content)
            )

        return JsonResponse(
            {"success": True, "message": "Comment has been successfully reported and moderators and admins notified."})

class DeleteCommentView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, user=request.user)  # Ensure only the owner can delete

        if comment.user == request.user or request.user.is_staff:
            comment.delete()
            return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this comment'}, status=403)
