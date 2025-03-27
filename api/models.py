from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


class EscoSkill(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(
        max_length=2048, null=True, blank=True, help_text="The label of the skill"
    )
    alternative_labels = ArrayField(
        models.CharField(max_length=2048),
        default=list,
        help_text="Alternative labels of the skill",
    )
    description = models.TextField(
        null=True, blank=True, help_text="Description of the skill"
    )
    # Using JSON field because sub-arrays must have the same length in postgres array field
    knowledge_ancestors = models.JSONField(
        help_text="The knowledge pillar ancestors of the skill (list of lists of strings)",
    )
    language_ancestors = models.JSONField(
        help_text="The language pillar ancestors of the skill (list of lists of strings)",
    )
    skill_ancestors = models.JSONField(
        help_text="The skill pillar ancestors of the skill (list of lists of strings)",
    )
    traversal_ancestors = models.JSONField(
        help_text="The traversal pillar ancestors of the skill (list of lists of strings)",
    )
    knowledge_levels = models.JSONField(
        help_text="The levels of the skill in knowledge paths"
    )
    language_levels = models.JSONField(
        help_text="The levels of the skill in language paths"
    )
    skill_levels = models.JSONField(help_text="The levels of the skill in skill paths")
    traversal_levels = models.JSONField(
        help_text="The levels of the skill in traversal paths"
    )
    children = models.JSONField(
        help_text="The children (direct descendants) of the skill"
    )

    def __str__(self):
        return self.label


class IscoOccupation(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(
        max_length=2048, null=True, blank=True, help_text="The label of the occupation"
    )
    alternative_labels = ArrayField(
        models.CharField(max_length=2048),
        default=list,
        help_text="Alternative labels of the occupation",
    )
    description = models.TextField(
        null=True, blank=True, help_text="Description of the occupation"
    )
    ancestors = models.JSONField(
        help_text="The ancestors of the occupation (list of lists of strings)",
    )
    levels = models.JSONField(help_text="The levels of the occupation")
    children = models.JSONField(
        help_text="The children (direct descendants) of the occupation"
    )

    def __str__(self):
        return self.label


class Project(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_project"
            )
        ]
        indexes = [
            GinIndex(
                fields=["title", "objective"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops"],
                name="project_search",
            )
        ]

    title = models.CharField(max_length=16384, help_text="Title of the project")
    start_date = models.DateField(
        help_text="Start date of the project", null=True, blank=True
    )
    end_date = models.DateField(
        help_text="End date of the project", null=True, blank=True
    )
    total_cost = models.FloatField(
        help_text="Total cost of the project", null=True, blank=True
    )
    objective = models.TextField(
        help_text="Objective of the project", null=True, blank=True
    )
    url = models.URLField(
        max_length=2048,
        help_text="URL of the project (e.g project's website)",
        null=True,
        blank=True,
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the project, from where information was retrieved (e.g H2020, FP7, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the project in the source database",
    )

    def __str__(self):
        return self.title


class ProjectSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "skill"], name="unique_project_skill"
            )
        ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The project that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="projects",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a project.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.project.title}"


class Organization(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_organization"
            )
        ]

        indexes = [
            GinIndex(
                fields=["name", "description"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops"],
                name="organization_search",
            )
        ]

    name = models.CharField(max_length=16384, help_text="Name of the organization")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the organization",
    )
    url = models.URLField(
        max_length=2048,
        null=True,
        blank=True,
        help_text="URL of organization's website",
    )
    country = models.CharField(
        max_length=255, null=True, blank=True, help_text="Country of the organization"
    )
    city = models.CharField(
        max_length=255, null=True, blank=True, help_text="City of the organization"
    )
    postcode = models.CharField(
        max_length=255, null=True, blank=True, help_text="Postcode of the organization"
    )
    street = models.CharField(
        max_length=255, null=True, blank=True, help_text="Street of the organization"
    )
    source = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Source of the organization, from where information was retrieved (e.g H2020, FP7, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the organization in the source database",
    )

    def __str__(self):
        return self.name


class ProjectOrganization(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="organizations",
        help_text="The project that the organization is part of.",
    )
    organization = models.ForeignKey(
        Organization,
        related_name="projects",
        on_delete=models.CASCADE,
        help_text="Organization that is part of the project.",
    )
    role = models.CharField(
        max_length=16384,
        help_text="Role of the organization in the project",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.organization.name} - {self.project.title}"


class OrganizationSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "skill"], name="unique_organization_skill"
            )
        ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The organization that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="organizations",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with an organization.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.organization.name}"


class Article(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_article"
            )
        ]

        indexes = [
            GinIndex(
                fields=["title", "summary"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops"],
                name="article_search",
            )
        ]

    title = models.CharField(max_length=16384, help_text="Title of the article")
    summary = models.TextField(
        null=True,
        blank=True,
        default=None,
        help_text="Description / Abstract / Summary of the article",
    )
    publication_date = models.DateField(
        null=True,
        blank=True,
        default=None,
        help_text="Publication date of the article",
    )
    authors = models.TextField(
        default=None, null=True, blank=True, help_text="Authors of the article"
    )
    journal = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=2048,
        help_text="Journal where the article was published",
    )
    url = models.URLField(
        null=True,
        blank=True,
        default=None,
        max_length=2048,
        help_text="URL of the article",
    )
    doi = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=255,
        help_text="DOI of the article",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="publications",
        help_text="The project that the article is related to (if any)",
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the article, from where information was retrieved (e.g H2020, FP7, ...)",
    )
    source_id = models.CharField(
        null=True,
        blank=True,
        default=None,
        max_length=255,
        help_text="ID of the article in the source database",
    )

    def __str__(self):
        return f"{self.title} by {self.authors}"


class ArticleSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "skill"], name="unique_article_skill"
            )
        ]

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The article that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="articles",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with an article.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.article.title}"


class Course(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_course"
            )
        ]

        indexes = [
            GinIndex(
                fields=["title", "description"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops"],
                name="course_search",
            )
        ]

    title = models.CharField(max_length=16384, help_text="Title of the course")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the course"
    )
    last_updated = models.DateField(
        null=True, blank=True, help_text="Creation date of the course"
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Rating of the course (0-10)",
        null=True,
        blank=True
    )
    price = models.FloatField(null=True, blank=True, help_text="Price of the course")
    url = models.URLField(max_length=2048, help_text="URL of the course")
    source = models.CharField(
        max_length=255,
        help_text="Source of the course, from where information was retrieved (e.g Udemy, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the course in the source database",
    )

    def __str__(self):
        return self.title


class CourseSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "skill"], name="unique_course_skill"
            )
        ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The course that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="courses",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a course.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.course.title}"


class Job(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_job"
            )
        ]

        indexes = [
            GinIndex(
                fields=["title", "description", "location", "type", "experience_level"],
                opclasses=[
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                ],
                name="job_search",
            ),
        ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="jobs",
        null=True,
        blank=True,
        help_text="The organization that the job is part of.",
    )

    title = models.CharField(max_length=255, help_text="Title of the job")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the job."
    )
    experience_level = models.CharField(
        max_length=16384,
        null=True,
        blank=True,
        help_text="Experience level required for the job. E.g Junior, Senior, ...",
    )
    type = models.CharField(
        max_length=16384,
        null=True,
        blank=True,
        help_text="Type of the job. E.g Full-time, Part-time, ...",
    )
    location = models.CharField(
        max_length=16384, null=True, blank=True, help_text="Location of the job."
    )
    upload_date = models.DateField(
        null=True, blank=True, help_text="Date when the job was uploaded."
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the job, from where information was retrieved (e.g LinkedIn, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the job in the source database",
    )

    def __str__(self):
        return self.title


class JobSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["job", "skill"], name="unique_job_skill")
        ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The job that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="jobs",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a job.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.job.title}"


class JobOccupation(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "occupation"], name="unique_job_occupation"
            )
        ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="occupations",
        help_text="The job that is matched with an occupation.",
    )
    occupation = models.ForeignKey(
        IscoOccupation,
        related_name="jobs",
        on_delete=models.CASCADE,
        help_text="The occupation that is matched with a job.",
    )

    def __str__(self):
        return f"{self.occupation.label} - {self.job.title}"


class Profile(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_profile"
            )
        ]

        indexes = [
            GinIndex(
                fields=["full_name", "location", "content", "occupation"],
                opclasses=[
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                    "gin_trgm_ops",
                ],
                name="profile_search",
            )
        ]

    full_name = models.CharField(
        null=True, blank=True, max_length=16384, help_text="Name of the user."
    )
    location = models.CharField(
        null=True, blank=True, max_length=16384, help_text="Location of the user."
    )
    content = models.TextField(
        null=True, blank=True, help_text="The content of the user's profile."
    )
    occupation = models.CharField(
        null=True, blank=True, max_length=16384, help_text="Occupation of the user."
    )
    url = models.URLField(
        null=True,
        blank=True,
        max_length=1024,
        help_text="The URL of the user's profile.",
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the profile, from where information was retrieved (e.g LinkedIn, StackOverflow...)",
    )
    source_id = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="ID of the profile in the source database",
    )

    def __str__(self):
        return self.full_name


class ProfileSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "skill"], name="unique_profile_skill"
            )
        ]

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The profile that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="profiles",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a profile.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.profile.full_name}"


class LawPolicy(models.Model):
    class Meta:
        verbose_name_plural = "Law policies"
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_law_policy"
            )
        ]
        indexes = [
            GinIndex(
                fields=["title", "summary", "authors"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops", "gin_trgm_ops"],
                name="law_policy_search",
            ),
        ]

    title = models.CharField(max_length=16384, help_text="Title of the law/policy")
    summary = models.TextField(
        null=True, blank=True, help_text="Summary of the law/policy"
    )
    authors = models.TextField(
        null=True, blank=True, help_text="Authors of the law/policy"
    )
    publication_date = models.DateField(
        null=True, blank=True, help_text="Publication date of the law/policy"
    )
    page_count = models.IntegerField(
        null=True, blank=True, help_text="Number of pages in the law/policy"
    )
    type = models.CharField(
        null=True,
        blank=True,
        max_length=2048,
        help_text="Type of the law/policy",
    )
    url = models.URLField(
        max_length=2048,
        null=True,
        blank=True,
        help_text="URL of the law/policy",
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the law/policy, from where information was retrieved (e.g open-europa, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the law/policy in the source database",
    )

    def __str__(self):
        return self.title


class LawPolicySkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["law_policy", "skill"], name="unique_law_policy_skill"
            )
        ]

    law_policy = models.ForeignKey(
        LawPolicy,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The law/policy that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="law_policies",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a law.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.law_policy.title}"


class LawPublication(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"], name="unique_source_law_publication"
            )
        ]
        indexes = [
            GinIndex(
                fields=["title", "authors", "summary"],
                opclasses=["gin_trgm_ops", "gin_trgm_ops", "gin_trgm_ops"],
                name="law_publication_search",
            )
        ]

    title = models.CharField(max_length=16384, help_text="Title of the law publication")
    authors = models.TextField(
        null=True, blank=True, help_text="Authors of the law publication"
    )
    publication_date = models.DateField(
        null=True, blank=True, help_text="Publication date of the law publication"
    )
    summary = models.TextField(
        null=True, blank=True, help_text="Summary of the law publication"
    )
    url = models.URLField(
        max_length=2048,
        null=True,
        blank=True,
        help_text="URL of the law publication",
    )
    isbn = models.CharField(
        max_length=1024, null=True, blank=True, help_text="ISBN of the law publication"
    )
    source = models.CharField(
        max_length=255,
        help_text="Source of the law publication, from where information was retrieved (e.g open-europa, ...)",
    )
    source_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="ID of the law publication in the source database",
    )


class LawPublicationSkill(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["law_publication", "skill"], name="unique_law_publication_skill"
            )
        ]

    law_publication = models.ForeignKey(
        LawPublication,
        on_delete=models.CASCADE,
        related_name="skills",
        help_text="The law publication that is matched with a skill.",
    )
    skill = models.ForeignKey(
        EscoSkill,
        related_name="law_publications",
        on_delete=models.CASCADE,
        help_text="The skill that is matched with a law publication.",
    )

    def __str__(self):
        return f"{self.skill.label} - {self.law_publication.title}"


class KeyValue(models.Model):
    key = models.CharField(max_length=512, unique=True)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"
