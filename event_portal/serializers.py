from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'help_text', 'options', 'is_faq','is_recommended']
        
class EventQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()  # Include the full question data

    class Meta:
        model = EventQuestion
        fields = ['question']
        
class EventSerializer(serializers.ModelSerializer):
    event_wallpaper = serializers.ImageField(required=False)
    event_question = EventQuestionSerializer(many=True, read_only=True)  

    class Meta:
        model = Event
        fields = ['id','title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
                  'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
                  'posted_by', 'event_question']
        
    # def get_event_wallpaper(self, obj):
    #     request = self.context.get('request')
    #     if obj.event_wallpaper:
    #         return request.build_absolute_uri(obj.event_wallpaper.url)
    #     return None  

class EventRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    category_id = serializers.CharField(source='category.id', read_only=True)
    posted_by = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    event_wallpaper = serializers.SerializerMethodField()
    event_question = serializers.SerializerMethodField()  # Custom method for serializing questions

    class Meta:
        model = Event
        fields = [
            'id','title','category_id', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
            'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
            'posted_by', 'event_question','is_active'
        ]

    def get_event_wallpaper(self, obj):
        request = self.context.get('request')
        if obj.event_wallpaper:
            return request.build_absolute_uri(obj.event_wallpaper.url)
        return None

    def get_event_question(self, obj):
        """
        Custom method to serialize related EventQuestion and Question data.
        """
        event_questions = EventQuestion.objects.filter(event=obj)  # Get related EventQuestions for this event
        event_question_data = []

        for event_question in event_questions:
            
            question = event_question.question  # Get the related Question
            question_data = {
                
                'id': question.id,
                'question': question.question,
                'options': question.options,
                'help_text': question.help_text,
                'is_faq': question.is_faq
            }
            event_question_data.append(question_data)

        return event_question_data

class EventActiveRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)
    posted_by = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    event_wallpaper = serializers.SerializerMethodField()
    event_question = serializers.SerializerMethodField()  # Custom method for serializing questions

    class Meta:
        model = Event
        fields = [
            'id','title', 'category', 'start_date', 'start_time', 'venue', 'address', 'link', 'is_public',
            'need_registration', 'registration_close_date', 'description', 'event_wallpaper', 'instructions',
            'posted_by', 'event_question'
        ]

    def get_event_wallpaper(self, obj):
        request = self.context.get('request')
        if obj.event_wallpaper:
            return request.build_absolute_uri(obj.event_wallpaper.url)
        return None

    def get_event_question(self, obj):
        """
        Custom method to serialize related EventQuestion and Question data.
        """
        event_questions = EventQuestion.objects.filter(event=obj)  # Get related EventQuestions for this event
        event_question_data = []

        for event_question in event_questions:
            question = event_question.question  # Get the related Question
            options_list = question.options.split(',') if question.options else []  # Split options by comma
            # Creating a list of dictionaries from options
            options_data = [{"option": option.strip()} for option in options_list]  # Create list of dictionaries

            question_data = {
                'id': question.id,
                'question': question.question,
                'options': options_data,  # Use the formatted options
                'help_text': question.help_text,
                'is_faq': question.is_faq
            }
            event_question_data.append(question_data)

        return event_question_data
