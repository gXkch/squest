import json

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404

from service_catalog.filters.instance_filter import InstanceFilter
from service_catalog.models import Instance, Support
from service_catalog.views import instance_new_support, instance_support_details


@user_passes_test(lambda u: u.is_superuser)
def admin_instance_list(request):
    f = InstanceFilter(request.GET, queryset=Instance.objects.all())
    return render(request, 'admin/instance/instance-list.html', {'filter': f})


@user_passes_test(lambda u: u.is_superuser)
def admin_instance_details(request, instance_id):
    instance = get_object_or_404(Instance, id=instance_id)
    spec_json_pretty = json.dumps(instance.spec)

    supports = Support.objects.filter(instance=instance)
    context = {'instance': instance,
               'spec_json_pretty': spec_json_pretty,
               'supports': supports}

    return render(request, 'admin/instance/instance-details.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def admin_instance_new_support(request, instance_id):
    return instance_new_support(request, instance_id)


@user_passes_test(lambda u: u.is_superuser)
def admin_instance_support_details(request, instance_id, support_id):
    return instance_support_details(request, instance_id, support_id)
