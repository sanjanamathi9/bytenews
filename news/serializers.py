from rest_framework import serializers
from .models import Article, Category, UserPreference

# ✅ Article Serializer: Used to display articles in JSON format
class ArticleSerializer(serializers.ModelSerializer):
    # You can choose StringRelatedField or PrimaryKeyRelatedField based on use case
    categories = serializers.StringRelatedField(many=True, read_only=True)
    # Optional improvement: include category IDs too (for flexibility)
    category_ids = serializers.PrimaryKeyRelatedField(
        source='categories', queryset=Category.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'summary',
            'link',
            'publication_date',
            'author',
            'source',
            'categories',      # readable names
            'category_ids',    # optional IDs if needed for updates
            'audio_file',
        ]
        read_only_fields = ['id', 'audio_file']  # audio_file will be filled later


# ✅ User Preference Serializer: For storing user's favorite categories
class UserPreferenceSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = UserPreference
        fields = ['id', 'user', 'categories']