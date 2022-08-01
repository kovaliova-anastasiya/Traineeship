from rest_framework import serializers


class BlockActionSerializer(serializers.Serializer):
    ACTIONS = (
        ('BLOCK', 'block'),
        ('UNBLOCK', 'unblock')
    )

    action = serializers.ChoiceField(choices=ACTIONS,
                                     error_messages={'invalid_choice': 'The request action is not valid'})
    content = serializers.CharField(max_length=300, required=False,
                                    error_messages={'max_length': "Tweet content is too Long"})
    unblock_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S.%f',
                                             error_messages={'invalid_choice': 'Date format %Y-%m-%d %H:%M:%S.%f'})
