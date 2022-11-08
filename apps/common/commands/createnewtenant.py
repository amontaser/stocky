from django.core.management.base import BaseCommand
from apps.marchants.models import Marchant
from tenant_users.tenants.utils import create_public_tenant
from tenant_users.tenants.tasks import provision_tenant


class Command(BaseCommand):
    help = 'creates new public tenant'

    def handle(self, *args, **kwargs):
        # create your public tenant
        create_public_tenant("dokkan.eg", "admin@dokkan.eg")
        Marchant.objects.create_user(email="amontaser@dokkan.eg", password='password', is_staff=True)
        Marchant.objects.create_user(email="demo@dokkan.eg", password='password', is_staff=True)
        provision_tenant("Demo", "demo", "demo@dokkan.eg", is_staff=True)