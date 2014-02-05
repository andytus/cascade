from rest_framework import serializers
from cascade.apps.report_builder.models import Report, ReportFiles
from utilities import CleanRelatedField, NullSerializerPatch



class ReportFileSerializer(serializers.ModelSerializer, NullSerializerPatch):
    report__root_model = CleanRelatedField(source='report.root_model.model')
    report__name = CleanRelatedField(source='report.name')
    report__id = CleanRelatedField(source='report.id')
    site__name = CleanRelatedField(source='site.name')
    report__user_created__username = CleanRelatedField(source='report.user_created.username')
    file = CleanRelatedField(source='file_path.url')
    description = CleanRelatedField(source='report.description')
    update_in_progress = CleanRelatedField(source='update_in_progress')

    class Meta:
        model = ReportFiles
        fields = ('id', 'report__name', 'report__id', 'report__user_created__username', 'file', 'last_generated'
                  , 'description', 'update_in_progress')




