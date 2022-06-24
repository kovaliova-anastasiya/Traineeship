from rest_framework import serializers


class RoleActionSerializer(serializers.Serializer):
    roles = (
        ('USER', 'user'),
        ('MODERATOR', 'moderator'),
        ('ADMIN', 'admin')
    )

    roles = serializers.ChoiceField(choices=roles,
                                    error_messages={'invalid_choice': 'The request action is not valid'})
