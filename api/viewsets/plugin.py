from http import HTTPMethod
from typing import Any, Dict, List

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models.column import DynamicColumn
from api.models.plugin import Plugin, PluginVersion
from api.serializers.plugin import AddPluginVersionSerializer, PluginSerializer
from api.serializers.table import DynamicTableSerializer
from api.utils import CustomResponseHandler
from drf_yasg.utils import swagger_auto_schema


class PluginViewSet(CustomResponseHandler, viewsets.ModelViewSet):
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
    # All the classic method are provide such as list,create,retrieve,update,partial_update, destroy

    @swagger_auto_schema(request_body=AddPluginVersionSerializer)
    @action(detail=True, methods=[HTTPMethod.POST], url_path="versions")
    def add_version(self, request: Request, pk=None) -> Response:
        plugin = get_object_or_404(Plugin, pk=pk)
        serialized_data = AddPluginVersionSerializer(
            data=request.data, context={"plugin": plugin}
        )

        if not serialized_data.is_valid():
            return self.error_response(
                "Error during plugin version serialization", serialized_data.errors
            )

        plugin_version: PluginVersion = serialized_data.save()
        # Keep tracking the composition of plugin in our databse
        schema = plugin_version.schema
        if not schema:
            return self.success_response(
                "Plugin Version registered but no schema provided", plugin_version
            )

        tables: List[Dict[str, Any]] = schema.get("tables", [])
        if not tables:
            return self.success_response(
                "Plugin Version registered but schema is empty", plugin_version
            )

        try:
            self._process_schema(plugin_version, tables)
        except ValidationError as e:
            return self.error_response(
                "Validation error during schema processing", e.detail
            )
        except Exception as e:
            return self.error_response(
                "Unexpected error during schema processing", str(e)
            )

        return self.success_response("Plugin registered and models created", plugin)

    def _process_schema(
        self, plugin_version: PluginVersion, tables: List[Dict[str, Any]]
    ) -> None:
        """Processes the schema, creating tables and columns dynamically."""
        for table in tables:
            name = table.get("name", None)
            if not name:
                raise ValidationError("All tables must have a name")

            dynamic_table = self._create_dynamic_table(plugin_version, name)

            columns = table.get("columns", [])
            if not columns:
                raise ValidationError(f"Table '{name}' must have at least one column")

            self._create_dynamic_columns(dynamic_table, columns)

    def _create_dynamic_table(self, plugin_version, name: str):
        """Creates a dynamic table associated with the plugin."""
        serialized_table = DynamicTableSerializer(
            data={"plugin_version": plugin_version.id, "name": name}
        )
        if not serialized_table.is_valid():
            raise ValidationError(serialized_table.errors)

        return serialized_table.save()

    def _create_dynamic_columns(
        self, dynamic_table, columns: List[Dict[str, Any]]
    ) -> None:
        """Creates dynamic columns for a given table."""
        for column in columns:
            DynamicColumn.objects.create(
                table=dynamic_table,
                name=column["name"],
                type=column["type"],
                is_primary=column.get("primary", False),
            )
