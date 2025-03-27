from django.contrib.auth.models import Group, User
from django.contrib import admin

from api.models import *


class ReadOnly(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister([Group, User])

admin.site.site_header = "Skillab Admin"
admin.site.site_title = "Skillab Admin"
admin.site.index_title = "Welcome to Skillab Admin"
admin.site.site_url = "/api/docs"


@admin.register(User)
class ChildClassAdmin(ReadOnly):
    list_display = ["username", "email", "is_staff", "is_active"]
    fields = ["username", "email", "is_staff", "is_active", "date_joined"]


class ProjectOrganizationInline(admin.TabularInline):
    model = ProjectOrganization
    extra = 0


class ProjectArticlesInline(admin.TabularInline):
    model = Article
    extra = 0
    fields = ["title", "authors", "doi"]


class OrganizationJobsInline(admin.TabularInline):
    model = Job
    extra = 0
    fields = ["title", "upload_date"]
    show_change_link = True


class OrganizationSkillInline(admin.TabularInline):
    model = OrganizationSkill
    extra = 0


class ArticleSkillInline(admin.TabularInline):
    model = ArticleSkill
    extra = 0


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 0


class LawPolicySkillInline(admin.TabularInline):
    model = LawPolicySkill
    extra = 0


class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 0


class JobOccupationInline(admin.TabularInline):
    model = JobOccupation
    extra = 0


class ProfileSkillInline(admin.TabularInline):
    model = ProfileSkill
    extra = 0


class CourseSkillInline(admin.TabularInline):
    model = CourseSkill
    extra = 0


class LawPublicationSkillInline(admin.TabularInline):
    model = LawPublicationSkill
    extra = 0


@admin.register(Project)
class ProjectAdmin(ReadOnly):
    search_fields = ["title"]
    list_display = ["title", "start_date", "source"]
    list_filter = ["source"]
    fields = [
        "title",
        "start_date",
        "end_date",
        "total_cost",
        "objective",
        "url",
        "source",
        "source_id",
    ]

    inlines = [ProjectOrganizationInline, ProjectArticlesInline, ProjectSkillInline]


@admin.register(Organization)
class OrganizationAdmin(ReadOnly):
    search_fields = ["name", "country", "city", "postcode", "street"]
    list_display = ["name", "country", "city", "postcode", "street"]
    list_filter = ["source", "country"]

    inlines = [
        ProjectOrganizationInline,
        OrganizationJobsInline,
        OrganizationSkillInline,
    ]


@admin.register(EscoSkill)
class EscoSkillAdmin(ReadOnly):
    search_fields = ["id", "label", "alternative_labels"]
    list_display = ["id", "label"]


@admin.register(IscoOccupation)
class IscoOccupationAdmin(ReadOnly):
    search_fields = ["id", "label", "alternative_labels"]
    list_display = ["id", "label"]


@admin.register(Article)
class ArticleAdmin(ReadOnly):
    search_fields = ["title", "summary"]
    list_display = ["title", "source", "source_id"]
    list_filter = ["source"]

    inlines = [ArticleSkillInline]


@admin.register(Course)
class CourseAdmin(ReadOnly):
    search_fields = ["title", "description"]
    list_display = ["title", "source", "source_id"]
    list_filter = ["source"]
    inlines = [CourseSkillInline]


@admin.register(Job)
class JobAdmin(ReadOnly):
    search_fields = ["title", "description"]
    list_display = ["title", "source", "source_id"]
    list_filter = ["source"]

    inlines = [JobSkillInline, JobOccupationInline]


@admin.register(Profile)
class ProfileAdmin(ReadOnly):
    search_fields = ["full_name"]
    list_display = ["full_name", "source", "source_id"]
    list_filter = ["source"]
    inlines = [ProfileSkillInline]


@admin.register(LawPublication)
class LawPublicationAdmin(ReadOnly):
    search_fields = ["title", "authors", "summary"]
    list_display = ["title", "source", "source_id"]
    list_filter = ["source"]
    inlines = [LawPublicationSkillInline]


@admin.register(LawPolicy)
class LawPolicyAdmin(ReadOnly):
    search_fields = ["title", "authors", "summary"]
    list_display = ["title", "source", "source_id"]
    list_filter = ["source"]
    inlines = [LawPolicySkillInline]


@admin.register(KeyValue)
class KeyValueAdmin(admin.ModelAdmin):
    search_fields = ["key", "value"]
    list_display = ["key", "value"]
