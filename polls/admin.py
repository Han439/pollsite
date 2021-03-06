from django.contrib import admin
from .models import PollQuestion, PollOption, VoteEntry

# Register your models here.
#admin.site.register(PollQuestion)

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
	list_display = ('question', 'option', 'vote',)
	list_filter = ('question',)

#admin.site.register(PollOption, PollOptionAdmin)

class PollOptionInline(admin.TabularInline):
	model = PollOption


@admin.register(PollQuestion)
class PollQuestion(admin.ModelAdmin):
	inlines = [PollOptionInline]

admin.site.register(VoteEntry)
