from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from chat.services import ChatService
from .services import UserService


class IsAdminGroupMember(permissions.BasePermission):
    """
    Allows access only to users who are members of the admin group.
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        return UserService.user_has_group(request.user, 'admin')


class IsUserChatParticipant(permissions.BasePermission):
    """
    Allows access only to chat participants.
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False

        chat_id = view.kwargs.get('chat_id')  # Get the chat_id from URL parameters
        print(ChatService.is_user_chat_participant(request.user, chat_id))
        return ChatService.is_user_chat_participant(request.user, chat_id)


# user permission codes
BAN_USER = "ban_user"
DELETE_USER = "delete_user"
BLOCK_USER = "block_user"
CHECK_PERMISSIONS = "check_permissions"
BAN_CHAT = "ban_chat"
BLOCK_CHAT = "block_chat"
DELETE_CHAT = "delete_chat"
VIEW_STATISTICS = "view_statistics"
CREATE_CHAT = "create_chat"
REMOVE_CHAT = "remove_chat"
GROUP_ADD_USER = "group_add_user"
GROUP_DELETE_USER = "group_delete_user"
GROUP_CHAT_HOST = "group_chat_host"
