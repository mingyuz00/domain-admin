# -*- coding: utf-8 -*-
"""
log_operation_api.py
"""

from flask import request, g
from playhouse.shortcuts import model_to_dict

from domain_admin.model.log_operation_model import LogOperationModel
from domain_admin.service import common_service


def get_operation_log_list():
    """
    获取操作日志列表
    :return:
    """
    current_user_id = g.user_id

    page = request.json.get('page', 1)
    size = request.json.get('size', 10)

    query = LogOperationModel.select()

    total = query.count()

    lst = []
    if total > 0:
        rows = query.order_by(
            LogOperationModel.create_time.desc(),
            LogOperationModel.id.desc(),
        ).paginate(page, size)

        lst = [model_to_dict(model=row, extra_attrs=[
            'type_label',
            'create_time_label',
        ]) for row in rows]

        common_service.load_user_name(lst)

    return {
        'list': lst,
        'total': total
    }
