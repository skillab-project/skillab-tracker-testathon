from typing import List, Dict, Set

from ninja import Router, Form
from ninja.pagination import paginate

from api.schemas import *
from api.models import *
from api.helpers import get_descendants


router = Router()


# ---------------------- Skills ----------------------
@router.post("skills", tags=["Skill"], response=List[EscoSkillSchema])
@paginate
def get_skills(request, filters: EscoSkillFilter = Form(...)):
    return filters.filter(EscoSkill.objects.all())


# ---------------------- Occupations ----------------------
@router.post("occupations", tags=["Occupation"], response=List[IscoOccupationSchema])
@paginate
def get_occupations(request, filters: IscoOccupationFilter = Form(...)):
    return filters.filter(IscoOccupation.objects.all())


# ---------------------- Utility ----------------------
@router.post("utility/skill-back-propagation", tags=["Utility"], response=List[str])
def skill_back_propagation(request, filters: BackPropagationFilter = Form(...)):
    skills = filters.filter(EscoSkill.objects.all())
    backpropagation_set = set()

    for skill in skills:
        backpropagation_set.update(s for p in skill.knowledge_ancestors for s in p)
        backpropagation_set.update(s for p in skill.language_ancestors for s in p)
        backpropagation_set.update(s for p in skill.skill_ancestors for s in p)
        backpropagation_set.update(s for p in skill.traversal_ancestors for s in p)

    return list(backpropagation_set)


@router.post(
    "utility/occupations-back-propagation", tags=["Utility"], response=List[str]
)
def occupation_back_propagation(request, filters: BackPropagationFilter = Form(...)):
    occupations = filters.filter(IscoOccupation.objects.all())
    backpropagation_set = set()

    for occupation in occupations:
        backpropagation_set.update(o for p in occupation.ancestors for o in p)

    return list(backpropagation_set)


@router.post("utility/skills-propagation", tags=["Utility"], response=List[str])
def skills_propagation(request, propagation_in: PropagationIn = Form(...)):
    skills = EscoSkill.objects.all().values("id", "children")
    skill_map: Dict[str, List[str]] = {
        skill["id"]: skill["children"] for skill in skills
    }
    descendant_set: Set[str] = set()

    for skill_id in propagation_in.ids:
        get_descendants(skill_id, skill_map, descendant_set)

    return list(descendant_set)


@router.post("utility/occupations-propagation", tags=["Utility"], response=List[str])
def occupations_propagation(request, propagation_in: PropagationIn = Form(...)):
    occupations = IscoOccupation.objects.all().values("id", "children")
    occupation_map: Dict[str, List[str]] = {
        occupation["id"]: occupation["children"] for occupation in occupations
    }
    descendant_set: Set[str] = set()

    for occupation_id in propagation_in.ids:
        get_descendants(occupation_id, occupation_map, descendant_set)

    return list(descendant_set)


# ---------------------- Projects ----------------------
@router.post("projects", tags=["Project"], response=List[ProjectSchema])
@paginate
def get_projects(request, filters: ProjectFilter = Form(...)):
    return (
        filters.filter(Project.objects.all())
        .prefetch_related("skills", "organizations")
        .distinct()
    )


@router.get("projects/sources", tags=["Project"], response=List[str])
def get_project_sources(request):
    return Project.objects.values_list("source", flat=True).distinct()


# ---------------------- Organizations ----------------------
@router.post("organizations", tags=["Organization"], response=List[OrganizationSchema])
@paginate
def get_organizations(request, filters: OrganizationFilter = Form(...)):
    return (
        filters.filter(Organization.objects.all())
        .prefetch_related("skills", "projects")
        .distinct()
    )


@router.get("organizations/sources", tags=["Organization"], response=List[str])
def get_organization_sources(request):
    return Organization.objects.values_list("source", flat=True).distinct()


# ---------------------- Articles ----------------------
@router.post("articles", tags=["Article"], response=List[ArticleSchema])
@paginate
def get_articles(request, filters: ArticleFilter = Form(...)):
    return filters.filter(Article.objects.all()).prefetch_related("skills").distinct()


@router.get("articles/sources", tags=["Article"], response=List[str])
def get_article_sources(request):
    return Article.objects.values_list("source", flat=True).distinct()


# ---------------------- Courses ----------------------
@router.post("courses", tags=["Course"], response=List[CourseSchema])
@paginate
def get_courses(request, filters: CourseFilter = Form(...)):
    return filters.filter(Course.objects.all()).prefetch_related("skills").distinct()


@router.get("courses/sources", tags=["Course"], response=List[str])
def get_course_sources(request):
    return Course.objects.values_list("source", flat=True).distinct()


# ---------------------- Jobs ----------------------
@router.post("jobs", tags=["Job"], response=List[JobSchema])
@paginate
def get_jobs(request, filters: JobFilter = Form(...)):
    return (
        filters.filter(Job.objects.all())
        .prefetch_related("skills", "occupations")
        .distinct()
    )


@router.get("jobs/sources", tags=["Job"], response=List[str])
def get_job_sources(request):
    return Job.objects.values_list("source", flat=True).distinct()


# ---------------------- Profiles ----------------------
@router.post("profiles", tags=["Profile"], response=List[ProfileSchema])
@paginate
def get_profiles(request, filters: ProfileFilter = Form(...)):
    return filters.filter(Profile.objects.all()).prefetch_related("skills").distinct()


@router.get("profiles/sources", tags=["Profile"], response=List[str])
def get_profile_sources(request):
    return Profile.objects.values_list("source", flat=True).distinct()


# ---------------------- Law Policies ----------------------
@router.post("law-policies", tags=["LawPolicy"], response=List[LawPolicySchema])
@paginate
def get_law_policies(request, filters: LawPolicyFilter = Form(...)):
    return filters.filter(LawPolicy.objects.all()).prefetch_related("skills").distinct()


@router.get("law-policies/sources", tags=["LawPolicy"], response=List[str])
def get_law_policy_sources(request):
    return LawPolicy.objects.values_list("source", flat=True).distinct()


# ---------------------- Law Publications ----------------------
@router.post(
    "law-publications", tags=["LawPublication"], response=List[LawPublicationSchema]
)
@paginate
def get_law_publications(request, filters: LawPublicationFilter = Form(...)):
    return (
        filters.filter(LawPublication.objects.all())
        .prefetch_related("skills")
        .distinct()
    )


@router.get("law-publications/sources", tags=["LawPublication"], response=List[str])
def get_law_publication_sources(request):
    return LawPublication.objects.values_list("source", flat=True).distinct()
