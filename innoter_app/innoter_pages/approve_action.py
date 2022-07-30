from rest_framework import serializers


class ApproveActionSerializer(serializers.Serializer):
    ACTIONS = (
        ('APPROVE', 'approve'),
        ('REJECT', 'reject'),
    )

    action = serializers.ChoiceField(choices=ACTIONS,
                                     error_messages={'invalid_choice': 'The request action is not valid'})
    content = serializers.CharField(max_length=300, required=False,
                                    error_messages={'max_length': 'Tweet content is too Long'})
    request_pk = serializers.IntegerField(required=True,
                                          error_messages={'type': 'Invalid input'})
