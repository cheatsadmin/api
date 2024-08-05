from django.contrib import admin

from cheatgame.issue.models import Issue, IssueCategory, IssueReport, Tag, IssueTag


@admin.register(Issue)
class ImageAdmin(admin.ModelAdmin):
    fields = ("title", "picture", "description", "min_price", "max_price",)
    search_fields = ("title",)
    list_display = (
        "title",
        "picture"
    )


@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    fields = ("issue", "category")
    list_display = ("issue", "category")


@admin.register(IssueReport)
class IssueReportAdmin(admin.ModelAdmin):
    fields = ("user", "delivery_data", "is_paid")
    list_display = ("user", "delivery_data", "is_paid")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ("title", "issue_type")
    list_display = ("title", "issue_type")


@admin.register(IssueTag)
class IssueTagAdmin(admin.ModelAdmin):
    fields = ("issue", "tag")
