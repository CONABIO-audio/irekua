from rest_framework.permissions import IsAuthenticated

from .generic import ReadOnly
from .generic import ReadAndCreateOnly
from .generic import ListAndCreateOnly
from .generic import CreateOnly
from .generic import IsUser
from .generic import IsOwner
from .generic import IsUnauthenticated
from .generic import IsCollectionUser
from .generic import IsCollectionTypeCoordinator
from .generic import IsDeveloper
from .generic import IsModel
from .generic import IsCurator
from .generic import IsAdmin
from .generic import IsFromInstitution

from .utils import PermissionMapping
from .utils import PermissionMappingMixin


__all__ = [
    'ReadOnly',
    'ReadAndCreateOnly',
    'ListAndCreateOnly',
    'CreateOnly',
    'IsUser',
    'IsOwner',
    'IsUnauthenticated',
    'IsCollectionUser',
    'IsCollectionTypeCoordinator',
    'IsDeveloper',
    'IsModel',
    'IsCurator',
    'IsAdmin',
    'IsFromInstitution',
    'PermissionMapping',
    'PermissionMappingMixin',
    'IsAuthenticated',
]
