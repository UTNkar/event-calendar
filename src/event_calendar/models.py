from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """The user manager for custom user model."""

    def create_user(self, email, password, group):
        """Create a new user."""
        group_instance = Group.objects.get(pk=group)
        user = self.model(
            email=email,
            group=group_instance
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, group):
        """Create a user and make it a superuser."""
        user = self.create_user(email, password, group)

        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """The user."""

    email = models.EmailField(unique=True)

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )

    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    objects = UserManager()

    is_active = True
    is_staff = True

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['group']

    def has_perm(self, perm, obj=None):  # noqa
        return True

    def has_module_perms(self, app_label):  # noqa
        return True


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
        related_name='posts'
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


class EventCoHost(models.Model):
    """A co host to an event."""

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
        through="EventCoHost"
    )
    categories = models.ManyToManyField(
        'Category',
        verbose_name=_("Event categories"),
        related_name="categories"
    )
    # TODO: Remove image from system automatically when event is deleted
    cover_photo = models.ImageField()
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
        null=True,
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
    contact = models.CharField(
        max_length=512
    )
    location = models.CharField(
        max_length=256,
        blank=True
    )
    price = models.CharField(
        max_length=256,
        blank=True
    )
    link = models.URLField(
        blank=True,
        verbose_name=_("URL"),
        help_text=_(
            "If your event has an important URL, "
            "such as a Zoom-link or Facebook page, enter it here."
        ),
    )

    def __str__(self):  # noqa
        return self.title_en + " by " + self.host.name_en
