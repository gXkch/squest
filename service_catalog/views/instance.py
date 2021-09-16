import json

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from django_fsm import can_proceed

from guardian.decorators import permission_required_or_403

from service_catalog.forms import InstanceForm, OperationRequestForm, SupportRequestForm
from service_catalog.forms.common_forms import SupportMessageForm
from service_catalog.models import Instance, Support, Operation, InstanceState, OperationType, SupportMessage


@user_passes_test(lambda u: u.is_superuser)
def instance_edit(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    form = InstanceForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('service_catalog:instance_details', instance.id)
    breadcrumbs = [
        {'text': 'Instances', 'url': reverse('service_catalog:instance_list')},
        {'text': f"{instance.name} ({instance.id})",
         'url': reverse('service_catalog:instance_details', args=[instance_id])},
    ]
    context = {'form': form, 'instance': instance, 'breadcrumbs': breadcrumbs}
    return render(request, 'service_catalog/admin/instance/instance-edit.html', context)


@permission_required_or_403('service_catalog.change_instance', (Instance, 'id', 'instance_id'))
def instance_request_new_operation(request, instance_id, operation_id):
    instance = get_object_or_404(Instance, id=instance_id)
    if instance.state not in [InstanceState.AVAILABLE, InstanceState.UPDATING]:
        raise PermissionDenied
    operation = get_object_or_404(Operation, id=operation_id)
    allowed_operations = Operation.objects.filter(service=instance.service,
                                                  type__in=[OperationType.UPDATE, OperationType.DELETE])
    if operation not in allowed_operations:
        raise PermissionDenied
    parameters = {
        'operation_id': operation_id,
        'instance_id': instance_id
    }
    if request.method == 'POST':
        form = OperationRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            form.save()
            return redirect('service_catalog:request_list')
    else:
        form = OperationRequestForm(request.user, **parameters)
    context = {'form': form, 'operation': operation, 'instance': instance}
    return render(request, 'service_catalog/customer/instance/instance-request-operation.html', context)


@permission_required_or_403('service_catalog.change_instance', (Instance, 'id', 'instance_id'))
def instance_archive(request, instance_id):
    target_instance = get_object_or_404(Instance, id=instance_id)
    if request.method == "POST":
        if not can_proceed(target_instance.archive):
            raise PermissionDenied
        target_instance.archive()
        target_instance.save()

        return redirect('service_catalog:instance_list')
    context = {
        "instance": target_instance
    }
    return render(request, "service_catalog/customer/instance/instance-archive.html", context)


@permission_required_or_403('service_catalog.change_instance', (Instance, 'id', 'instance_id'))
def instance_new_support(request, instance_id):
    target_instance = get_object_or_404(Instance, id=instance_id)
    breadcrumbs = [
        {'text': 'Instances', 'url': reverse('service_catalog:instance_list')},
        {'text': f"{target_instance.name} ({target_instance.id})",
         'url': reverse('service_catalog:instance_details', args=[instance_id])},
    ]
    parameters = {
        'instance_id': instance_id
    }
    if request.method == 'POST':
        form = SupportRequestForm(request.user, request.POST, **parameters)
        if form.is_valid():
            form.save()
            return redirect('service_catalog:instance_details', target_instance.id)
    else:
        form = SupportRequestForm(request.user, **parameters)
    context = {'form': form, 'instance': target_instance, 'breadcrumbs': breadcrumbs}
    return render(request, 'service_catalog/common/support-create.html', context)


@permission_required_or_403('service_catalog.change_instance', (Instance, 'id', 'instance_id'))
def instance_support_details(request, instance_id, support_id):
    instance = get_object_or_404(Instance, id=instance_id)
    support = get_object_or_404(Support, id=support_id)
    messages = SupportMessage.objects.filter(support=support)
    breadcrumbs = [
        {'text': 'Instances', 'url': reverse('service_catalog:instance_list')},
        {'text': f"{instance.name} ({instance.id})",
         'url': reverse('service_catalog:instance_details', args=[instance_id])},
        {'text': 'Support', 'url': ""},
        {'text': support.title, 'url': ""},
    ]
    if request.method == "POST":
        form = SupportMessageForm(request.POST or None)
        if "btn_close" in request.POST:
            if not can_proceed(support.do_close):
                raise PermissionDenied
            support.do_close()
            support.save()
        if "btn_re_open" in request.POST:
            if not can_proceed(support.do_open):
                raise PermissionDenied
            support.do_open()
            support.save()
        if form.is_valid():
            if form.cleaned_data["content"] is not None and form.cleaned_data["content"] != "":
                new_message = form.save()
                new_message.support = support
                new_message.sender = request.user
                new_message.save()
            return redirect('service_catalog:instance_support_details', instance.id, support.id)
    else:
        form = SupportMessageForm()
    context = {
        "form": form,
        "instance": instance,
        "messages": messages,
        "support": support,
        'breadcrumbs': breadcrumbs
    }
    return render(request, "service_catalog/common/instance-support-details.html", context)


@permission_required_or_403('service_catalog.view_instance', (Instance, 'id', 'instance_id'))
def instance_details(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    spec_json_pretty = json.dumps(instance.spec)
    supports = Support.objects.filter(instance=instance)
    operations = Operation.objects.filter(service=instance.service,
                                          type__in=[OperationType.UPDATE, OperationType.DELETE])
    breadcrumbs = [
        {'text': 'Instances', 'url': reverse('service_catalog:instance_list')},
        {'text': f"{instance.name} ({instance.id})", 'url': ""},
    ]
    context = {'instance': instance,
               'spec_json_pretty': spec_json_pretty,
               'supports': supports,
               'operations': operations,
               'breadcrumbs': breadcrumbs
               }
    return render(request, 'service_catalog/common/instance-details.html', context=context)