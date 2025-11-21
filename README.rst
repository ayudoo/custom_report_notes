Custom Report Notes
===================

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

**This is the Odoo 18 branch**

**This module is in beta state. Feel free to provide feedback.**

Add reusable notes to you sales orders, delivery slips and invoices.

**Table of contents**

.. contents::
   :local:


Overview
--------

Odoo report templates are very flexible and can be overridden and styled as you like.
However, managing these templates separately can be cumbersome or become quite an
overhead.

This module adds configurable `Custom Report Notes` to your `Sales Orders`,
`Delivery Slips` and `Invoices`. These documents are similar in kind and you can
enhance them with your reusable notes.


Usage
-----

In ``General Settings`` -> ``Document Layout`` open `Custom Report Notes`. Note, that
you need permissions of group `System` to be able to create new notes.

You can choose the type of report, its state, and where exactly to insert the note by
selecting one of the fields ``Address``, ``Heading``, ``Table``, ``Signature/Comment``
and ``Bottom``, as well as whether to place it ``before`` or ``after``.

They provide the full power of the Odoo wysiwyg editor, use it with caution.


Limitations
^^^^^^^^^^^

* links don't open a new page when printed on paper
* with DIN 5008 document layout, custom report notes around address and above heading don't work


Bug Tracker
-----------

Bugs are tracked on `GitHub Issues <https://github.com/ayudoo/custom_report_notes/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/ayudoo/custom_report_notes/issues/new?body=**Steps%20to%20reproduce**%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
-------

Authors
^^^^^^^

* Michael Jurke
* Ayudoo Ltd <support@ayudoo.bg>
