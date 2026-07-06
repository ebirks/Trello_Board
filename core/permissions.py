from rest_framework import permissions


class IsBoardMemberOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Add this line!
        print("--- IsBoardMemberOrReadOnly has_permission triggered! ---")
        return True  # Let it pass to the next check

    def has_object_permission(self, request, view, obj):
        print(f"--- Checking permissions for user: {request.user.username} ---")
        print(f"Board owner is: {obj.owner}")
        print(f"Request method is: {request.method}")

        # If it's a GET, HEAD, or OPTIONS request
        if request.method in permissions.SAFE_METHODS:
            is_member = obj.memberships.filter(user=request.user).exists()
            print(f"Is member? {is_member}")
            return obj.owner == request.user or is_member

        # For POST, PUT, DELETE:
        if obj.owner == request.user:
            print("User is the owner. Allowing.")
            return True

        print("User is not the owner. Checking role...")
        try:
            membership = obj.memberships.get(user=request.user)
            print(f"Found membership. Role is: {membership.role}")
            if membership.role in ['admin', 'editor']:
                return True
            else:
                return False
        except Exception as e:
            print(f"No membership found: {e}")
            return False