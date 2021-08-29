# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.commands import CommandSet, ICommand, Command
from pip_services3_commons.convert import TypeCode
from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_commons.run import Parameters
from pip_services3_commons.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema

from pip_service_data_python.data.EntityV1 import EntityV1
from pip_service_data_python.data.EntityV1Schema import EntityV1Schema
from pip_service_data_python.logic.IEntitiesController import IEntitiesController


class EntitiesCommandSet(CommandSet):

    def __init__(self, controller: IEntitiesController):
        super().__init__()

        self.__controller = controller

        self.add_command(self.__make_get_entities_command())
        self.add_command(self.__make_get_entity_by_id_command())
        self.add_command(self.__make_get_entity_by_name_command())
        self.add_command(self.__make_create_entity_command())
        self.add_command(self.__make_update_entity_command())
        self.add_command(self.__make_delete_entity_by_id_command())

    def __make_get_entities_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            filter = FilterParams.from_value(args.get('filter'))
            paging = PagingParams.from_value(args.get('paging'))
            return self.__controller.get_entities(correlation_id, filter, paging)

        return Command(
            'get_entities',
            ObjectSchema(True)
                .with_optional_property('filter', FilterParamsSchema())
                .with_optional_property('paging', PagingParamsSchema()),
            action
        )

    def __make_get_entity_by_id_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            entity_id = args.get_as_string('entity_id')
            return self.__controller.get_entities_by_id(correlation_id, entity_id)

        return Command(
            'get_entity_by_id',
            ObjectSchema(True).with_required_property('entity_id', TypeCode.String),
            action
        )

    def __make_get_entity_by_name_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            name = args.get_as_string('entity_name')
            return self.__controller.get_entity_by_name(correlation_id, name)

        return Command(
            'get_entity_by_name',
            ObjectSchema(True).with_required_property('entity_name', TypeCode.String),
            action
        )

    def __make_create_entity_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            entity = args.get_as_object('entity')
            if isinstance(entity, dict):
                entity = EntityV1(**entity)
            return self.__controller.create_entity(correlation_id, entity)

        return Command(
            'create_entity',
            ObjectSchema(True).with_required_property('entity', EntityV1Schema()),
            action
        )

    def __make_update_entity_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            entity = args.get_as_object('entity')
            if isinstance(entity, dict):
                entity = EntityV1(**entity)
            return self.__controller.update_entity(correlation_id, entity)

        return Command(
            'update_entity',
            ObjectSchema(True).with_required_property('entity', EntityV1Schema()),
            action
        )

    def __make_delete_entity_by_id_command(self) -> ICommand:
        def action(correlation_id: Optional[str], args: Parameters):
            entity_id = args.get_as_string('entity_id')
            return self.__controller.delete_entity_by_id(correlation_id, entity_id)

        return Command(
            'delete_entity_by_id',
            ObjectSchema(True).with_required_property('entity_id', TypeCode.String),
            action
        )

# # -*- coding: utf-8 -*-
# from typing import Optional
#
# from pip_services3_commons.commands import CommandSet, ICommand, Command
# from pip_services3_commons.convert import TypeCode
# from pip_services3_commons.data import FilterParams, PagingParams, DataPage
# from pip_services3_commons.run import Parameters
# from pip_services3_commons.validate import ObjectSchema, FilterParamsSchema, PagingParamsSchema
#
# from pip_service_data_python.data.EntityV1 import EntityV1
# from pip_service_data_python.data.EntityV1Schema import EntityV1Schema
# from pip_service_data_python.logic.IEntitiesController import IEntitiesController
#
#
# class EntitiesCommandSet(CommandSet):
#
#     def __init__(self, controller: IEntitiesController):
#         super().__init__()
#
#         self.__controller = controller
#
#         self.add_command(self.__make_get_entities_command())
#         self.add_command(self.__make_get_entity_by_id_command())
#         self.add_command(self.__make_get_entity_by_name_command())
#         self.add_command(self.__make_create_entity_command())
#         self.add_command(self.__make_update_entity_command())
#         self.add_command(self.__make_delete_entity_by_id_command())
#
#     def __make_get_entities_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             filter = FilterParams.from_value(args.get('filter'))
#             paging = PagingParams.from_value(args.get('paging'))
#
#             result = self.__controller.get_entities(correlation_id, filter, paging)
#
#             items = []
#             for item in result.data:
#                 items.append(item.to_dict())
#
#             return DataPage(items, len(items))
#
#         return Command(
#             'get_entities',
#             ObjectSchema(True)
#                 .with_optional_property('filter', FilterParamsSchema())
#                 .with_optional_property('paging', PagingParamsSchema()),
#             action
#         )
#
#     def __make_get_entity_by_id_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             entity_id = args.get_as_string('entity_id')
#             result = self.__controller.get_entities_by_id(correlation_id, entity_id)
#             return result.to_dict()
#
#         return Command(
#             'get_entity_by_id',
#             ObjectSchema(True).with_required_property('entity_id', TypeCode.String),
#             action
#         )
#
#     def __make_get_entity_by_name_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             name = args.get_as_string('name')
#             result = self.__controller.get_entity_by_name(correlation_id, name)
#             return result.to_dict()
#
#         return Command(
#             'get_entity_by_name',
#             ObjectSchema(True).with_required_property('entity_name', TypeCode.String),
#             action
#         )
#
#     def __make_create_entity_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             entity = args.get_as_object('entity')
#             if isinstance(entity, dict):
#                 entity = EntityV1(**entity)
#             result = self.__controller.create_entity(correlation_id, entity)
#             return result.to_dict()
#
#         return Command(
#             'create_entity',
#             ObjectSchema(True).with_required_property('entity', EntityV1Schema()),
#             action
#         )
#
#     def __make_update_entity_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             entity = args.get_as_object('entity')
#
#             if isinstance(entity, dict):
#                 entity = EntityV1(**entity)
#
#             result = self.__controller.update_entity(correlation_id, entity)
#             return result.to_dict()
#
#         return Command(
#             'update_entity',
#             ObjectSchema(True).with_required_property('entity', EntityV1Schema()),
#             action
#         )
#
#     def __make_delete_entity_by_id_command(self) -> ICommand:
#         def action(correlation_id: Optional[str], args: Parameters):
#             entity_id = args.get_as_string('entity_id')
#             result = self.__controller.delete_entity_by_id(correlation_id, entity_id)
#             return result.to_dict()
#
#         return Command(
#             'delete_entity_by_id',
#             ObjectSchema(True).with_required_property('entity_id', TypeCode.String),
#             action
#         )
