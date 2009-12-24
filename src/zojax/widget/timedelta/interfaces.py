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
from zope import interface, schema
from zope.schema import interfaces


class ITimedelta(interfaces.ITimedelta):
    """ simple timedelta field """


class ITimedeltaWidget(interface.Interface):
    """ Timedelta widget """

    hourMin = schema.Int(
        title = u'Minimun hour value',
        default = 0,
        required = True)

    hourMax = schema.Int(
        title = u'Maximum hour value',
        default = 15,
        required = True)

    hourStep = schema.Int(
        title = u'Hour step value',
        default = 1,
        required = True)

    minStep = schema.Int(
        title = u'Minutes step value',
        default = 15,
        required = True)
