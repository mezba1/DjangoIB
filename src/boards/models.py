import requests

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.core.files.storage import DefaultStorage
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from djangoib.utils import upload_image, parse_post_body

file_storage = DefaultStorage()
rpost = requests.post


def _validate_file_size(value):
    filesize = value.size

    if filesize > 20000000:
        raise ValidationError('The maximum image size that can be uploaded is 20MB')
    else:
        return value


class CustomBaseModel(models.Model):
    file = models.FileField(
        blank=True,
        help_text=_('Maximum allowed size is 20MB.'),
        null=True,
        storage=file_storage,
        validators=[_validate_file_size],
    )
    file_delete_hash = models.CharField(
        blank=True,
        help_text=_('Autopopulated by the system. Will be used to delete uploaded file from imgur.'),
        max_length=64,
        null=True,
    )
    file_height = models.IntegerField(
        blank=True,
        help_text=_('Autopopulated by the system. Indicates the height of the image file.'),
        null=True,
    )
    file_name = models.CharField(
        blank=True,
        default=None,
        help_text=_('Autopopulated by the system. The name of the image file.'),
        max_length=256,
        null=True,
    )
    file_size = models.IntegerField(
        blank=True,
        help_text=_('Autopopulated by the system. Indicates the size of the image file in bytes.'),
        null=True,
    )
    file_url = models.CharField(
        blank=True,
        help_text=_('Autopopulated by the system. Indicates the direct link to the image file.'),
        max_length=64,
        null=True,
    )
    file_width = models.IntegerField(
        blank=True,
        help_text=_('Autopopulated by the system. Indicates the width of the image file.'),
        null=True,
    )

    class Meta:
        abstract = True

    def _clear_file_fields(self):
        self.file_delete_hash = None
        self.file_height = None
        self.file_name = None
        self.file_size = None
        self.file_url = None
        self.file_width = None

    def has_image(self):
        if all([self.file_delete_hash, self.file_height, self.file_name, self.file_size, self.file_url,
                self.file_width]):
            return True
        else:
            return False

    def get_image_url(self):
        return self.file_url

    def get_small_thumbnail(self):
        return self.get_thumbnail('s')

    def get_thumbnail(self, modifier='m'):
        if self.has_image():
            a, b = self.get_image_url().rsplit('.', 1)
            return '{}{}.{}'.format(a, modifier, b)
        else:
            return None

    def get_image_download_url(self):
        if self.has_image():
            a, _ = self.get_image_url().rsplit('.', 1)
            _, b = a.rsplit('/', 1)
            return 'https://imgur.com/download/{}'.format(b)
        else:
            return None

    def _process_file_fields(self):
        if self.has_image():
            pass
        else:
            self._clear_file_fields()

    def process_image(self):
        if self.file:
            r = upload_image(self.file.file)
            if r:
                succeeded = r.get('success')
                if succeeded:
                    data = r.get('data')
                    self.file_delete_hash = data.get('deletehash')
                    self.file_height = data.get('height')
                    self.file_name = self.file.file.name
                    self.file_size = data.get('size')
                    self.file_url = data.get('link')
                    self.file_width = data.get('width')
            else:
                self._process_file_fields()
            self.file = None
        else:
            self._process_file_fields()


class Board(CustomBaseModel):
    is_sfw = models.BooleanField(
        default=False,
        help_text=_('Indicates whether this board is safe-for-work (sfw) or not.'),
        null=False,
    )
    tagline = models.CharField(
        blank=True,
        help_text=_('Tagline of this board.'),
        max_length=128,
        null=True,
    )
    title = models.CharField(
        help_text=_('Title of this board.'),
        max_length=64,
        null=False,
    )
    slug = models.CharField(
        help_text=_('Identifier of this board (slug). Will be used in urls.'),
        max_length=4,
        null=False,
        unique=True,
    )

    objects = models.Manager()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '/{}/ - {}'.format(self.slug, self.title)

    def get_absolute_url(self):
        return reverse('dib-board-index', args=[self.slug])

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            self.updated_at = timezone.now()
        self.process_image()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['slug']


class Post(CustomBaseModel):
    board = models.ForeignKey(
        help_text=_('Required. Indicates which board this post belongs to.'),
        null=False,
        on_delete=models.CASCADE,
        to=Board,
    )
    body = models.CharField(
        blank=True,
        help_text=_(
            "Required if, 1. this post is a thread and no title is provided or "
            "2. this post is a reply and no title or file is provided. "
            "Main text content/body of current post which appears after it's title."
        ),
        max_length=2048,
        null=False,
    )
    ip_address = models.GenericIPAddressField(
        default='0.0.0.0',
        help_text=_('Indicates the ip address of the creator.'),
        null=False,
    )
    is_archived = models.BooleanField(
        default=False,
        help_text=_('Indicates whether this post is archived or not.'),
        null=False,
    )
    is_locked = models.BooleanField(
        default=False,
        help_text=_('Indicates whether this post is locked or not.'),
        null=False,
    )
    is_sticky = models.BooleanField(
        default=False,
        help_text=_('Indicates whether this post is sticky or not.'),
        null=False,
    )
    name = models.CharField(
        max_length=32,
        help_text=_('Self-given name of the creator.'),
        null=True,
        blank=True,
    )
    parent = models.ForeignKey(
        blank=True,
        help_text=_('Required. Indicates which thread this post belongs to.'),
        null=True,
        on_delete=models.CASCADE,
        to='self',
    )
    quoted_posts = models.ManyToManyField(related_name='quoted_in_set', symmetrical=False, to='self')
    title = models.CharField(
        blank=True,
        help_text=_(
            "Required if this post is a thread and no body is provided. "
            "Title of this post. N.B. replies must not have title."
        ),
        max_length=64,
        null=True,
    )
    user = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        to=User,
    )

    objects = models.Manager()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.parent:
            return '#{}/{} (/{}/ - {})'.format(self.parent.pk, self.pk, self.board.slug, self.board.title)
        else:
            return '#{} (/{}/ - {})'.format(self.pk, self.board.slug, self.board.title)

    def get_absolute_url(self):
        return reverse('dib-thread-index', args=[self.board.slug, self.pk])

    def process_body(self):
        if self.body and self.parent:
            quotable_post_ids = []
            op_id = self.parent.pk
            if self.parent:
                quotable_post_ids = list(self.parent.post_set.all().values_list('pk', flat=True))
            quotable_post_ids.append(op_id)
            self.body, quoted_post_ids = parse_post_body(self.body, quotable_post_ids, op_id)
            return quoted_post_ids
        else:
            return []

    def clean(self):
        if not self.parent:
            if not self.file and not self.has_image():
                raise ValidationError({'file': ['File is required for a thread (post having no parent).']})
            if not self.body and not self.title:
                raise ValidationError('Provide a title or some content or both.')
        else:
            if not self.body and not self.file and not self.has_image():
                raise ValidationError('Provide an image or some content or both.')
            if self.is_archived:
                self.is_archived = False
            if self.is_locked:
                self.is_locked = False
            if self.is_sticky:
                self.is_sticky = False

        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            self.updated_at = timezone.now()
            instance = super().save(*args, **kwargs)
        else:
            self.process_image()
            quoted_post_ids = self.process_body()
            instance = super().save(*args, **kwargs)
            for i in quoted_post_ids:
                self.quoted_posts.add(i)
        if self.parent:
            self.parent.updated_at = self.updated_at
            self.parent.save()

        return instance

    class Meta:
        ordering = ['is_sticky', '-updated_at']
