# -*- coding: utf-8 -*-

"""Functions to support the display of a view."""
import copy

from django.utils.translation import ugettext_lazy as _
import django_tables2 as tables

from ontask import models
from ontask.core import OperationsColumn
from ontask.table.services.errors import OnTaskTableCloneError


class ViewTable(tables.Table):
    """Table to display the set of views handled in a workflow."""

    name = tables.Column(verbose_name=_('Name'))

    description_text = tables.Column(
        empty_values=[],
        verbose_name=_('Description'))

    operations = OperationsColumn(
        verbose_name=_('Operations'),
        template_file='table/includes/partial_view_operations.html',
        template_context=lambda record: {'id': record['id']},
    )

    class Meta:
        """Select the model and specify fields, sequence and attributes."""

        model = models.View
        fields = ('operations', 'name', 'description_text')
        sequence = ('operations', 'name', 'description_text')
        attrs = {
            'class': 'table table-hover table-bordered shadow',
            'style': 'width: 100%;',
            'id': 'view-table',
        }


def do_clone_view(
    user,
    view: models.View,
    new_workflow: models.Workflow = None,
    new_name: str = None,
) -> models.View:
    """Clone a view.

    :param user: User requesting the operation
    :param view: Object to clone
    :param new_workflow: Non empty if it has to point to a new workflow
    :param new_name: Non empty if it has to be renamed.
    :result: New clone object
    """
    id_old = view.id
    name_old = view.name

    # Proceed to clone the view
    if new_name is None:
        new_name = view.name
    if new_workflow is None:
        new_workflow = view.workflow

    new_view = models.View(
        name=new_name,
        description_text=view.description_text,
        workflow=new_workflow,
        formula=copy.deepcopy(view.formula),
    )
    new_view.save()

    try:
        # Update the many to many field.
        new_view.columns.set(list(view.columns.all()))
    except Exception:
        raise OnTaskTableCloneError(
            message=_('Error while cloning table view.'),
            to_delete=[new_view]
        )

    view.log(
        user,
        models.Log.VIEW_CLONE,
        id_old=id_old,
        name_old=name_old)

    return new_view


def save_view_form(
    user,
    workflow: models.Workflow,
    view: models.View
):
    """Save the data attached to a view.

    :param user: user requesting the operation
    :param workflow: Workflow being processed
    :param view: View being processed.
    :return: AJAX Response
    """
    view.workflow = workflow
    view.save()
    view.log(
        user,
        models.Log.VIEW_CREATE if view.id is None else models.Log.VIEW_EDIT)
