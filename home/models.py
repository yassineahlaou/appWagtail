from wagtail.core.models import Page,Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel,InlinePanel,MultiFieldPanel,FieldRowPanel
from django.db import models
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .blocks import TwoColumnBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from django.db import models


from modelcluster.models import ClusterableModel

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from wagtailyoast.edit_handlers import YoastPanel
from wagtail.core.models import Page
from wagtailmetadata.models import MetadataPageMixin

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from django import template

from wagtailmetadata import tags

register = template.Library()







class HomePage(MetadataPageMixin,Page):
    body = RichTextField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    keywords = models.CharField(default='', blank=True, max_length=100)

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading=('Content')),
        ObjectList(Page.promote_panels, heading=('Promotion')),
        ObjectList(Page.settings_panels, heading=('Settings')),
        YoastPanel(
            keywords='keywords',
            title='seo_title',
            search_description='search_description',
            slug='slug'
        ),
    ])

#class AboutUs(Page):
    #intro = RichTextField(blank=True)
    #search_fields = Page.search_fields + [
#   index.SearchField('intro'),
#]
#   content_panels = Page.content_panels + [

#       FieldPanel('intro', classname="full"),
#       InlinePanel('gallery_images', label="Gallery images"),

   # ]

class AboutUs(MetadataPageMixin,Page):
    template="home/about_us.html "
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('intro', blocks.RichTextBlock()),
        ('two_columns', TwoColumnBlock()),
        ('image', ImageChooserBlock(icon="image")),

    ],null=True,blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]





#class AboutUsGalleryImage(Orderable):
   # page = ParentalKey(AboutUs, on_delete=models.CASCADE, related_name='gallery_images')
    #image = models.ForeignKey(
    #    'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
   # )
   # caption = models.CharField(blank=True, max_length=250)

  #  panels = [
     #   ImageChooserPanel('image'),
     #   FieldPanel('caption'),
    #]

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')

class FormPage(MetadataPageMixin,WagtailCaptchaEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()


class TextPage(MetadataPageMixin,Page):
    text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('text', classname='full'),
    ]


class MetadataMixin(object):
    """
    An object that can be shared on social media.
    """

    def get_meta_url(self):
        """The full URL to this object, including protocol and domain."""
        raise NotImplementedError()

    def get_meta_title(self):
        raise NotImplementedError()

    def get_object_title(self):
        return self.get_meta_title()

    def get_meta_description(self):
        raise NotImplementedError()

    def get_meta_image_url(self, request):
        """
        Get the image url to use for this object.
        Can be None if there is no relevant image.
        """
        return None

    def get_meta_image_dimensions(self):
        """
        Return width, height (in pixels)
        """
        return None, None

    def get_twitter_card_type(self, request):
        """
        Get the Twitter card type for this object.
        See https://dev.twitter.com/cards/types.
        Defaults to 'summary' if the object has an image,
        otherwise 'summary'.
        """
        if self.get_meta_image_url(request) is not None:
            return 'summary_large_image'
        else:
            return 'summary'


class WagtailImageMetadataMixin(MetadataMixin):
    """
    Subclass of MetadataMixin that uses a Wagtail Image for the image-based metadata
    """
    def get_meta_image(self):
        raise NotImplementedError()

    def get_meta_image_rendition(self):
        meta_image = self.get_meta_image()
        if meta_image:
            filter = getattr(settings, "WAGTAILMETADATA_IMAGE_FILTER", "original")
            rendition = meta_image.get_rendition(filter=filter)
            return rendition
        return None

    def get_meta_image_url(self, request):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return request.build_absolute_uri(meta_image.url)
        return None

    def get_meta_image_dimensions(self):
        meta_image = self.get_meta_image_rendition()
        if meta_image:
            return meta_image.width, meta_image.height
        return None, None


class MetadataPageMixin(WagtailImageMetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=ugettext_lazy('Search image')
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
        ], ugettext_lazy('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_image(self):
        return self.search_image

    class Meta:
        abstract = True



@register.simple_tag(takes_context=True)
def meta_tags(context, model=None):
    request = context.get('request', None)
    if not model:
        model = context.get('self', None)

    return tags.meta_tags(request, model)