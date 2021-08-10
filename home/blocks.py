from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


#class ColumnBlock(blocks.StreamBlock):
   # heading = blocks.CharBlock(classname="full title")
   # intro = blocks.RichTextBlock()
    #image = ImageChooserBlock()

    #class Meta:
        #template = 'home/blocks/column_block.html'


class TwoColumnBlock(blocks.StructBlock):
    left_column = blocks.StreamBlock([
        ('heading', blocks.CharBlock(classname="full title")),
        ('intro', blocks.RichTextBlock()),

        ('image', ImageChooserBlock(icon="image")),
    ], icon='arrow-left', label='Left column content')

    right_column = blocks.StreamBlock([
        ('heading', blocks.CharBlock(classname="full title")),
        ('intro', blocks.RichTextBlock()),

        ('image', ImageChooserBlock(icon="image")),
    ], icon='arrow-right', label='Right column content')

    class Meta:
        template = 'home/blocks/two_column_block.html'
        icon = 'edit'
        label = 'Two Columns'