from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, help_text=_("The person who created the project"), verbose_name=_("Owner"))
    name = models.CharField(max_length=255, help_text=_("A label used to describe the project"), verbose_name=_("Name"))
    description = models.TextField(default="", blank=True, help_text=_("More in-depth description of the project"), verbose_name=_("Description"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_("Creation date"), verbose_name=_("Created at"))
    deleting = models.BooleanField(db_index=True, default=False, help_text=_("Whether this project has been marked for deletion. Projects that have running tasks need to wait for tasks to be properly cleaned up before they can be deleted."), verbose_name=_("Deleting"))
    tags = models.TextField(db_index=True, default="", blank=True, help_text=_("Project tags"), verbose_name=_("Tags"))


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")