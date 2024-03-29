from django.urls import path
from .views import *

urlpatterns = [
    path('social-groups/', SocialGroupsView.as_view(), name='social_groups'),
    path('social-groups/<int:pk>/', SocialGroupDetailView.as_view(), name='social_group_detail'),
    path('social-groups/<int:social_group_id>/users', SocialGroupUsersView.as_view(), name='social_group_memebers'),
    path('social-groups/create/', CreateSocialGroupView.as_view(), name='create_social_group'),
    path('join-group/<int:group_id>/', JoinGroupView.as_view(), name='join_group'),
    path('social-groups/<int:social_group_id>/add-post/', AddPostView.as_view(), name='social_group_add_post'),
    path('social-groups/<int:post_id>/add-comment/', AddCommentView.as_view(), name='social_group_add_comment'),
    path('edit-comment/', EditCommentView.as_view(), name='social_group_edit_comment'),
    path('social-groups/post/<int:post_id>/delete/', DeletePostView.as_view(), name='social_group_delete_post'),
    path('edit-post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add_comment'),
    path('social-groups/<int:social_group_id>/<int:user_id>/invite-user/', InviteUserView.as_view(),
         name='invite_user'),
    path('social-groups/<int:social_group_id>/events/', SocialGroupEventsView.as_view(), name='social_group_events'),
    path('social-groups/<int:social_group_id>/create-event/', CreateSocialGroupEventView.as_view(),
         name='create_social_group_event'),
    path('social-groups/<int:social_group_id>/events/<int:event_id>/join/', JoinEventView.as_view(), name='join_event'),
    path('social-groups/<int:social_group_id>/events/<int:event_id>/delete/', DeleteEventView.as_view(),
         name='delete_event'),
    path('social-groups/<int:social_group_id>/leave/', LeaveGroupView.as_view(), name='leave_group'),
    path('delete-group/<int:group_id>/', DeleteGroupView.as_view(), name='delete_group'),

    path('social-groups/<int:social_group_id>/posts/<int:post_id>/report', SocialGroupPostReportView.as_view(),
         name='report-post'),
    path('post/<int:post_id>/comment/<int:comment_id>', PostCommentReport.as_view(), name='report_comment'),
    path('delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),

]
