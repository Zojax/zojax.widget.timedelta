##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import datetime

from zope import component, interface, schema
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from z3c.form import converter
from z3c.form.browser import widget
from z3c.form.widget import Widget, FieldWidget
from z3c.form.interfaces import NOVALUE, IFormLayer, IFieldWidget
from zojax.widget.timedelta.interfaces import ITimedelta, ITimedeltaWidget


class TimedeltaWidget(widget.HTMLInputWidget, Widget):
    interface.implements(ITimedeltaWidget)

    hourMin = 0
    hourMax = 15
    hourStep = 1
    minuteStep = 15

    def update(self):
        super(TimedeltaWidget, self).update()

        if self.value is None:
            self.value = [None, None]

        self.hours = self.value[0]
        self.minutes = self.value[1]

        self.hourValues = SimpleVocabulary(
            [SimpleTerm(-1, '--', '--')] +
            [SimpleTerm(v, str(v), unicode(v))
             for v in range(self.hourMin,
                            self.hourMax+self.hourStep, self.hourStep)])

        self.minuteValues = SimpleVocabulary(
            [SimpleTerm(v, str(v), unicode(v))
             for v in range(0, 60, self.minuteStep)])

    def extract(self, default=NOVALUE):
        request = self.request

        hour = request.get(self.name + '.hour', u'')
        minute = request.get(self.name + '.minute', u'')

        if not hour or hour == '--':
            if minute:
                try:
                    return [None, int(minute)]
                except:
                    pass

            return default

        if not minute:
            return default

        try:
            return [int(hour), int(minute)]
        except:
            return default


class TimedeltaDataConverter(converter.BaseDataConverter):
    """
    >>> from zojax.widget.list import SimpleList
    >>> list = SimpleList()

    >>> converter = ListDataConverter(list, None)

    >>> converter.toWidgetValue(None)
    u''

    >>> print converter.toWidgetValue(['line1', 'line2', 'line3'])
    line1
    line2
    line3

    >>> print converter.toFieldValue('line5 \\n line8\\n line10')
    ['line5', 'line8', 'line10']

    >>> ListFieldWidget(list, None)
    <ListWidget ''>
    """
    component.adapts(ITimedelta, ITimedeltaWidget)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        if isinstance(value, datetime.timedelta):
            seconds = value.days*86400 + value.seconds
            hours, seconds = divmod(seconds, 3600)
            return [hours, divmod(seconds, 60)[0]]

        return [None, None]

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if value is None or value is NOVALUE:
            return self.field.default

        try:
            hours, minutes = value
            return datetime.timedelta(
                0, hours*3600 + minutes * 60)
        except:
            return self.field.default


@interface.implementer(IFieldWidget)
@component.adapter(ITimedelta, IFormLayer)
def TimedeltaFieldWidget(field, request):
    return FieldWidget(field, TimedeltaWidget(request))
