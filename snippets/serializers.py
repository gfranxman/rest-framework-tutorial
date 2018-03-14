from rest_framework import serializers
from .models import Snippet, MULTI_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    linenos = serializers.CharField(label='Line Numbers')
    multiselect = serializers.MultipleChoiceField(choices=MULTI_CHOICES)
    mselect = serializers.MultipleChoiceField(choices=MULTI_CHOICES)


    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style',
                  'multiselect', 'mselect')

                  
class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,
                                                   view_name='snippet-detail',
                                                   read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
