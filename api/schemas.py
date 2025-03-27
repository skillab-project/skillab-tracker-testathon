from enum import Enum
from typing import List, Any
from datetime import date

from ninja import ModelSchema, FilterSchema, Schema
from ninja.schema import Field
from django.db.models import Q

from api.models import *


class LogicEnum(str, Enum):
    and_ = "and"
    or_ = "or"


def logic_list(
    fields: List[str],
    values: List[str] | None,
    logic: LogicEnum,
) -> Q:
    q = Q()
    for value in values or []:
        word_q = Q()
        for field in fields:
            word_q |= Q(**{f"{field}__icontains": value})

        q = (q & word_q) if logic == LogicEnum.and_ else (q | word_q)

    return q


def logic_list_foreign_key(field: str, values: List[str] | None, logic: LogicEnum) -> Q:
    # Awesome and hacky solution by: https://stackoverflow.com/a/39595260/11718554
    if logic == LogicEnum.or_:
        return Q(**{f"{field}__in": values})

    q = Q()
    for value in values or []:
        q |= ~Q(**{f"{field}": value})
    return ~q


# ---------------------- Skills ----------------------


class EscoSkillSchema(ModelSchema):
    class Meta:
        model = EscoSkill
        fields = "__all__"


class EscoSkillFilter(FilterSchema):
    ids: List[str] = Field(
        None,
        q="id__in",
        description="The skill IDs that will be returned.",
        example=[
            "http://data.europa.eu/esco/skill/ccd0a1d9-afda-43d9-b901-96344886e14d",
            "http://data.europa.eu/esco/skill/19a8293b-8e95-4de3-983f-77484079c389",
        ],
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in skill's label, alternative labels or description",
        example=["programming"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_, description="The logic to use when filtering by keywords"
    )

    ancestors: List[str] = Field(
        None,
        description="A list of ancestor IDs that must be included in skill's knowledge, language, skill or traversal ancestors",
        example=[
            "http://data.europa.eu/esco/skill/335228d2-297d-4e0e-a6ee-bc6a8dc110d9"
        ],
    )

    ancestors_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by ancestors",
        example=LogicEnum.or_,
    )

    children: List[str] = Field(
        None,
        description="A list of children IDs that must be included in skill's children",
        example=[],
    )

    children_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by children",
    )

    min_knowledge_level: int = Field(
        None,
        q="knowledge_levels__0__gte",
        description="All knowledge path levels must be greater than or equal to this value",
        example="",
    )
    max_knowledge_level: int = Field(
        None,
        q="knowledge_levels__-1__lte",
        description="All knowledge path levels must be less than or equal to this value",
        example="",
    )

    min_language_level: int = Field(
        None,
        q="language_levels__0__gte",
        description="All language path levels must be greater than or equal to this value",
        example="",
    )
    max_language_level: int = Field(
        None,
        q="language_levels__-1__lte",
        description="All language path levels must be less than or equal to this value",
        example="",
    )

    min_skill_level: int = Field(
        None,
        q="skill_levels__0__gte",
        description="All skill path levels must be greater than or equal to this value",
        example=3,
    )
    max_skill_level: int = Field(
        None,
        q="skill_levels__-1__lte",
        description="All skill path levels must be less than or equal to this value",
        example="",
    )

    min_traversal_level: int = Field(
        None,
        q="traversal_levels__0__gte",
        description="All traversal path levels must be greater than or equal to this value",
        example="",
    )
    max_traversal_level: int = Field(
        None,
        q="traversal_levels__-1__lte",
        description="All traversal path levels must be less than or equal to this value",
        example="",
    )

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str] | None) -> Q:
        return logic_list(
            ["label", "alternative_labels", "description"], values, self.keywords_logic
        )

    def filter_ancestors_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_ancestors(self, values: List[str]) -> Q:
        return logic_list(
            [
                "knowledge_ancestors",
                "language_ancestors",
                "skill_ancestors",
                "traversal_ancestors",
            ],
            values,
            self.ancestors_logic,
        )

    def filter_children_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_children(self, values: List[str]) -> Q:
        return logic_list(
            ["children"],
            values,
            self.children_logic,
        )


class BackPropagationFilter(FilterSchema):
    ids: List[str] = Field(None, q="id__in")


class PropagationIn(Schema):
    ids: List[str] = Field()


# ---------------------- Occupations ----------------------
class IscoOccupationSchema(ModelSchema):
    class Meta:
        model = IscoOccupation
        fields = "__all__"


class IscoOccupationFilter(FilterSchema):
    ids: List[str] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned occupations",
        example=[],
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in occupations's label, alternative labels or description",
        example=["programming"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_, description="The logic to use when filtering by keywords"
    )

    ancestors: List[str] = Field(
        None,
        description="A list of ancestor IDs that must be included in skill's knowledge, language, skill or traversal ancestors",
        example=[],
    )

    ancestors_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by ancestors",
    )

    children: List[str] = Field(
        None,
        description="A list of children IDs that must be included in skill's children",
        example=[],
    )

    children_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by children",
    )

    min_level: int = Field(
        None,
        q="levels__0__gte",
        description="All levels must be greater than or equal to this value",
        example="",
    )
    max_level: int = Field(
        None,
        q="levels__-1__lte",
        description="All levels must be less than or equal to this value",
        example="",
    )

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(
            ["label", "alternative_labels", "description"], values, self.keywords_logic
        )

    def filter_ancestors_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_ancestors(self, values: List[str]) -> Q:
        return logic_list(
            ["ancestors"],
            values,
            self.ancestors_logic,
        )

    def filter_children_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_children(self, values: List[str]) -> Q:
        return logic_list(
            ["children"],
            values,
            self.children_logic,
        )


# ---------------------- Projects ----------------------
class ProjectSchema(ModelSchema):
    class Meta:
        model = Project
        fields = "__all__"

    skills: List[str]
    organizations: List[int]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)

    @staticmethod
    def resolve_organizations(obj):
        return obj.organizations.values_list("organization_id", flat=True)


class ProjectFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned projects",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only projects that have these skills will be returned",
        example=[
            "http://data.europa.eu/esco/skill/103f7814-d262-4df6-a1b6-759bc51f76cb"
        ],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    keywords: List[str] = Field(
        None,
        description="A keyword that must be included in project's title or objective",
        example=["software"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    start_date: date = Field(
        None,
        q="start_date__gte",
        description="The start date must be greater than or equal to this value",
        example="2015-01-01",
    )
    end_date: date = Field(
        None,
        q="end_date__lte",
        description="The end date must be less than or equal to this value",
        example="2018-12-31",
    )
    min_total_cost: float = Field(
        None,
        q="total_cost__gte",
        description="The total cost must be greater than or equal to this value",
        example="",
    )
    max_total_cost: float = Field(
        None,
        q="total_cost__lte",
        description="The total cost must be less than or equal to this value",
        example="",
    )
    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only projects from these sources will be returned",
        example=["cordis-fp7"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["title", "objective"], values, self.keywords_logic)


# ---------------------- Organizations ----------------------
class OrganizationSchema(ModelSchema):
    class Meta:
        model = Organization
        fields = "__all__"

    skills: List[str]
    projects: List[int]

    @staticmethod
    def resolve_projects(obj):
        return obj.projects.values_list("project_id", flat=True)

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class OrganizationFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned organizations",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only organizations that have these skills will be returned",
        example=None,
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in organization's name or description",
        example=["software"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    projects: List[int] = Field(
        None,
        description="Only organizations that are related to these projects will be returned",
        example=[],
    )

    projects_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by projects",
    )

    countries: List[str] = Field(
        None,
        q="country__in",
        description="Only organizations from these countries will be returned",
        example=["IT"],
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only organizations from these sources will be returned",
        example=["cordis-fp7"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_projects_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_projects(self, values: List[int]) -> Q:
        return logic_list_foreign_key(
            "projects__project_id", values, self.projects_logic
        )

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["name", "description"], values, self.keywords_logic)


# ---------------------- Articles ----------------------
class ArticleSchema(ModelSchema):
    class Meta:
        model = Article
        fields = "__all__"

    skills: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class ArticleFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned articles",
        example=[],
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in article's title, abstract or journal",
        example=["python"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    skill_ids: List[str] = Field(
        None,
        description="Only articles that have these skills will be returned",
        example=[
            "http://data.europa.eu/esco/skill/21d2f96d-35f7-4e3f-9745-c533d2dd6e97"
        ],
    )
    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    projects: List[int] = Field(
        None,
        q="project_id__in",
        description="Articles that are related to these projects will be returned",
        example=[],
    )

    publication_date_min: date = Field(
        None,
        q="publication_date__gte",
        description="The publication date must be greater than or equal to this value",
        example="",
    )

    publication_date_max: date = Field(
        None,
        q="publication_date__lte",
        description="The publication date must be less than or equal to this value",
        example="",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only articles from these sources will be returned",
        example=[],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["title", "summary"], values, self.keywords_logic)


# ---------------------- Courses ----------------------
class CourseSchema(ModelSchema):
    class Meta:
        model = Course
        fields = "__all__"

    skills: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class CourseFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned courses",
        example=[],
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in course's title, or description",
        example=["python"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    skill_ids: List[str] = Field(
        None,
        q="skills__skill_id__in",
        description="Only courses that have these skills will be returned",
        example=[
            "http://data.europa.eu/esco/skill/ccd0a1d9-afda-43d9-b901-96344886e14d"
        ],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    min_creation_date: date = Field(
        None,
        q="creation_date__gte",
        description="The creation date must be greater than or equal to this value",
        example="",
    )
    max_creation_date: date = Field(
        None,
        q="creation_date__lte",
        description="The creation date must be less than or equal to this value",
        example="",
    )

    min_rating: float = Field(
        None,
        q="rating__gte",
        description="The rating must be greater than or equal to this value",
        ge=0,
        le=10,
        example="",
    )
    max_rating: float = Field(
        None,
        q="rating__lte",
        description="The rating must be less than or equal to this value",
        ge=0,
        le=10,
        example="",
    )

    min_price: float = Field(
        None,
        q="price__gte",
        description="The price must be greater than or equal to this value",
        ge=0,
        example="",
    )
    max_price: float = Field(
        None,
        q="price__lte",
        description="The price must be less than or equal to this value",
        ge=0,
        example="",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only courses from these sources will be returned",
        example=["udemy"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["title", "description"], values, self.keywords_logic)


# ---------------------- Jobs ----------------------
class JobSchema(ModelSchema):
    class Meta:
        model = Job
        fields = "__all__"

    skills: List[str]
    occupations: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)

    @staticmethod
    def resolve_occupations(obj):
        return obj.occupations.values_list("occupation_id", flat=True)


class JobFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned jobs",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only jobs that have these skills will be returned",
        example=[
            "http://data.europa.eu/esco/skill/ccd0a1d9-afda-43d9-b901-96344886e14d"
        ],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    occupation_ids: List[str] = Field(
        None,
        description="Only jobs that have these occupations will be returned",
        example=[],
    )
    occupation_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by occupations",
    )

    organization_ids: List[int] = Field(
        None,
        q="organization_id__in",
        description="Jobs that are related to these organizations will be returned",
        example=[],
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in job's title, description or location",
        example=["python"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    min_upload_date: date = Field(
        None,
        q="upload_date__gte",
        description="The upload date must be greater than or equal to this value",
        example="",
    )
    max_upload_date: date = Field(
        None,
        q="upload_date__lte",
        description="The upload date must be less than or equal to this value",
        example="",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only jobs from these sources will be returned",
        example=["linkedin"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(
            ["title", "description", "location", "type", "experience_level"],
            values,
            self.keywords_logic,
        )

    def filter_occupation_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_occupation_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key(
            "occupations__occupation_id", values, self.occupation_ids_logic
        )


# ---------------------- Profiles ----------------------
class ProfileSchema(ModelSchema):
    class Meta:
        model = Profile
        fields = "__all__"

    skills: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class ProfileFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned profiles",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only profiles that have these skills will be returned",
        example=[
            "http://data.europa.eu/esco/skill/ccd0a1d9-afda-43d9-b901-96344886e14d"
        ],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in profile's name, content, occupation or location",
        example=["python"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only profiles from these sources will be returned",
        example=["stack-math"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(
            ["full_name", "location", "content", "occupation"],
            values,
            self.keywords_logic,
        )


# ---------------------- Law Policies ----------------------
class LawPolicySchema(ModelSchema):
    class Meta:
        model = LawPolicy
        fields = "__all__"

    skills: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class LawPolicyFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned law policies",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only law policies that have these skills will be returned",
        example=[],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in law policy's title, summary, or authors",
        example=["software"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    min_publication_date: date = Field(
        None,
        q="publication_date__gte",
        description="The publication date must be greater than or equal to this value",
        example="",
    )

    max_publication_date: date = Field(
        None,
        q="publication_date__lte",
        description="The publication date must be less than or equal to this value",
        example="",
    )

    min_page_count: int = Field(
        None,
        q="page_count__gte",
        description="The page count must be greater than or equal to this value",
        example="",
    )

    max_page_count: int = Field(
        None,
        q="page_count__lte",
        description="The page count must be less than or equal to this value",
        example="",
    )

    type: str = Field(
        None,
        description="Only law policies with this type will be returned",
        example="",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only law policies from these sources will be returned",
        example=["eur_lex"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["title", "summary", "authors"], values, self.keywords_logic)


# ---------------------- Law Publications ----------------------
class LawPublicationSchema(ModelSchema):
    class Meta:
        model = LawPublication
        fields = "__all__"

    skills: List[str]

    @staticmethod
    def resolve_skills(obj):
        return obj.skills.values_list("skill_id", flat=True)


class LawPublicationFilter(FilterSchema):
    ids: List[int] = Field(
        None,
        q="id__in",
        description="A list of IDs that must included in the returned law publications",
        example=[],
    )

    skill_ids: List[str] = Field(
        None,
        description="Only law publications that have these skills will be returned",
        example=[],
    )

    skill_ids_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by skill IDs",
    )

    keywords: List[str] = Field(
        None,
        description="Keywords that must be included in law publication's title, authors, summary",
        example=["Greece"],
    )

    keywords_logic: LogicEnum = Field(
        LogicEnum.or_,
        description="The logic to use when filtering by keywords",
    )

    isbns: List[str] = Field(
        None,
        q="isbn__in",
        description="Only law publications with these ISBNs will be returned",
        example=[],
    )

    publication_date_min: date = Field(
        None,
        q="publication_date__gte",
        description="The publication date must be greater than or equal to this value",
        example="",
    )

    publication_date_max: date = Field(
        None,
        q="publication_date__lte",
        description="The publication date must be less than or equal to this value",
        example="",
    )

    sources: List[str] = Field(
        None,
        q="source__in",
        description="Only law publications from these sources will be returned",
        example=["ILO"],
    )

    def filter_skill_ids_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_skill_ids(self, values: List[str]) -> Q:
        return logic_list_foreign_key("skills__skill_id", values, self.skill_ids_logic)

    def filter_keywords_logic(self, _: LogicEnum) -> Q:
        return Q()

    def filter_keywords(self, values: List[str]) -> Q:
        return logic_list(["title", "authors", "summary"], values, self.keywords_logic)
