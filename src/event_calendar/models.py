from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    """The user."""
    pass


class Category(models.Model):
    """The categories an event can have."""

    name_sv = models.CharField(
        max_length=128,
        verbose_name=_("Swedish name")
    )
    name_en = models.CharField(
        max_length=128,
        verbose_name=_("English name")
    )

    def __str__(self):  # noqa
        return self.name_en


class Post(models.Model):
    """
    Text posts where the event hosts can write updates.

    Text posts written by the event hosts that will be displayed on the
    event main page. Can contain information, updates, release links etcetera.
    If has_been_edited is true, the post will be displayed as 'edited'.
    """

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        verbose_name=_("Related event"),
    )
    content = models.TextField(
        verbose_name=_("Post contents"),
    )
    created_by = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_("Post creator"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Time of posting"),
    )
    has_been_edited = models.BooleanField(
        default=False,
        verbose_name=_("Has been edited"),
    )

    def __str__(self):  # noqa
        return "In {} posted by {} at {}.".format(
            self.event,
            self.created_by,
            self.created_at
        )

    def save(self, *args, **kwargs):
        """If post has been edited, update has_been_edited."""
        if self.id:
            self.has_been_edited = True
        return super(Post, self).save(*args, **kwargs)


class Group(models.Model):
    """The group that events belong to, e.g. Forskå or E-sektionen."""

    name_en = models.CharField(
        max_length=128,
        verbose_name=_("English name"),
    )
    name_sv = models.CharField(
        max_length=128,
        verbose_name=_("Swedish name"),
    )
    description_en = models.TextField(
        verbose_name=_("English description"),
        blank=True
    )
    description_sv = models.TextField(
        verbose_name=_("Swedish description"),
        blank=True
    )

    def __str__(self):  # noqa
        return self.name_en


class EventInvite(models.Model):
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=32,
        choices=(
            ("invited", _("Invited")),
            ("accepted", _("Accepted"))
        ),
        default="invited"
    )


class Event(models.Model):
    """The event model itself."""

    title_sv = models.CharField(
        max_length=256,
        verbose_name=_("Swedish event title"),
    )
    title_en = models.CharField(
        max_length=256,
        verbose_name=_("English event title")
    )
    host = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_("Event host"),
    )
    cohosts = models.ManyToManyField(
        'Group',
        verbose_name=_("Event co-hosts"),
        related_name="cohosted_events",
        through="EventInvite"
    )
    categories = models.ManyToManyField(
        'Category',
        verbose_name=_("Event categories"),
        related_name="categories"
    )

    description_en = models.TextField(
        verbose_name=_("English event description"),
    )
    description_sv = models.TextField(
        verbose_name=_("Swedish event description"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last modified"),
    )
    date_start = models.DateTimeField(
        verbose_name=_("Event start date"),
        help_text=_("Date and time when the event will start."),
    )
    date_end = models.DateTimeField(
        blank=True,
        verbose_name=_("Event end date"),
        help_text=_("Leave empty if the event has no specific end time.")
    )
    published = models.BooleanField(
        default=False
    )
    membership_required = models.BooleanField(
        verbose_name=_("Membership required"),
        help_text=_("If the event requires a section or UTN membership."),
    )

    def __str__(self):  # noqa
        return self.title_en + " by " + self.host.name_en
