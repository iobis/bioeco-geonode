#########################################################################
#
# Copyright (C) 2021 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
import ast
import typing
import logging

from datetime import datetime
from inspect import signature, Signature, Parameter

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from geonode.celery_app import app
from geonode.base.models import ResourceBase
from geonode.resource.manager import resource_manager
from geonode.tasks.tasks import (
    AcquireLock,
    FaultTolerantTask)

from .utils import resolve_type_serializer
from ..models import ExecutionRequest

logger = logging.getLogger(__name__)


def _get_param_value(_param, _input_value):
    _param_value = None
    if _param.annotation == typing.Union[object, None]:
        _param_value = resolve_type_serializer(_input_value)[0]
    elif _param.annotation == settings.AUTH_USER_MODEL:
        _param_value = get_user_model().objects.get(username=_input_value)
    elif _param.annotation in (dict, list, tuple) and isinstance(_input_value, str):
        _param_value = _param.annotation(ast.literal_eval(_input_value))
        for _key in ['user', 'owner']:
            _username = _param_value.pop(_key, None)
            if _username:
                _param_value[_key] = get_user_model().objects.get(username=_username)
    else:
        _param_value = _param.annotation(_input_value)
    return _param_value


@app.task(
    bind=True,
    base=FaultTolerantTask,
    queue='geonode',
    acks_late=False,
    ignore_result=False,
)
def resouce_service_dispatcher(self, execution_id: int):
    """Performs a Resource Service request asynchronously.

    This function

    """
    lock_id = f'{self.request.id}'
    with AcquireLock(lock_id) as lock:
        if lock.acquire() is True:
            _exec_request = ExecutionRequest.objects.filter(exec_id=execution_id)
            if _exec_request.exists():
                _request = _exec_request.get()
                if _request.status == ExecutionRequest.STATUS_READY:
                    _exec_request.update(
                        status=ExecutionRequest.STATUS_RUNNING
                    )
                    _request.refresh_from_db()
                    if hasattr(resource_manager, _request.func_name):
                        try:
                            _signature = signature(getattr(resource_manager, _request.func_name))
                            _args = []
                            _kwargs = {}
                            for _param_name in _signature.parameters:
                                if _request.input_params and _request.input_params.get(_param_name, None):
                                    _param = _signature.parameters.get(_param_name)
                                    _param_value = _get_param_value(
                                        _param, _request.input_params.get(_param_name))
                                    if _param.kind == Parameter.POSITIONAL_ONLY:
                                        _args.append(_param_value)
                                    else:
                                        _kwargs[_param_name] = _param_value

                            _bindings = _signature.bind(*_args, **_kwargs)
                            _bindings.apply_defaults()

                            _output = getattr(resource_manager, _request.func_name)(*_bindings.args, **_bindings.kwargs)
                            _output_params = {}
                            if _output is not None and _signature.return_annotation != Signature.empty:
                                if _signature.return_annotation.__module__ == 'builtins':
                                    _output_params = {
                                        "output": _output
                                    }
                                elif _signature.return_annotation == ResourceBase or isinstance(_output, ResourceBase):
                                    _output_params = {
                                        "output": {
                                            "uuid": _output.uuid
                                        }
                                    }
                            else:
                                _output_params = {
                                    "output": None
                                }
                            _exec_request.update(
                                status=ExecutionRequest.STATUS_FINISHED,
                                finished=datetime.now(),
                                output_params=_output_params
                            )
                            _request.refresh_from_db()
                        except Exception as e:
                            logger.exception(e)
                            _exec_request.update(
                                status=ExecutionRequest.STATUS_FAILED,
                                finished=datetime.now(),
                                output_params={
                                    "error": _(f"Error occurred while executin the operation: '{_request.func_name}'"),
                                    "exception": str(e)
                                }
                            )
                            _request.refresh_from_db()
                    else:
                        _exec_request.update(
                            status=ExecutionRequest.STATUS_FAILED,
                            finished=datetime.now(),
                            output_params={
                                "error": _(f"Could not find the operation name: '{_request.func_name}'")
                            }
                        )
                        _request.refresh_from_db()