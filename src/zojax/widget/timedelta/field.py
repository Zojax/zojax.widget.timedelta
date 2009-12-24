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

from zope import interface
from zope.schema import Timedelta
from zope.schema.interfaces import IFromUnicode
from zojax.widget.timedelta.interfaces import ITimedelta


class Timedelta(Timedelta):
    interface.implements(ITimedelta, IFromUnicode)

    def fromUnicode(self, s):
        """
        >>> td = Timedelta()
        >>> td.fromUnicode('3:15')
        datetime.timedelta(0, 11700)
        >>> td.fromUnicode('3.15')
        datetime.timedelta(0, 11700)
        >>> td.fromUnicode(':15')
        datetime.timedelta(0, 900)
        >>> td.fromUnicode('.15')
        datetime.timedelta(0, 900)

        >>> td.fromUnicode('3')
        datetime.timedelta(0, 10800)
        >>> td.fromUnicode('3:')
        datetime.timedelta(0, 10800)
        >>> td.fromUnicode('3.')
        datetime.timedelta(0, 10800)

        >>> td.fromUnicode('3/15')
        Traceback (most recent call last):
        ...
        ValueError: invalid literal: 3/15

        >>> td.fromUnicode('tt:cc')
        Traceback (most recent call last):
        ...
        ValueError: invalid literal: tt:cc
        """

        hours = 0
        mins = 0

        d = ''

        if ':' in s:
            d = ':'
        elif '.' in s:
            d = '.'

        if not d:
            try:
                hours = int(s)
            except ValueError:
                raise ValueError, 'invalid literal: %s'%s
        else:
            parts = [p.strip() for p in s.split(d)]

            try:
                if parts[0]:
                    hours = int(parts[0])
                if parts[1]:
                    mins = int(parts[1])
            except ValueError:
                raise ValueError, 'invalid literal: %s'%s

        v = datetime.timedelta(hours=hours, minutes=mins)
        self.validate(v)
        return v
