__author__ = 'pkdash'

from django.core.exceptions import ValidationError

from rest_framework import serializers
from usu_data_service.utils import *
from usu_data_service.servicefunctions.static_data import get_static_data_file_path

class InputRasterURLorStaticRequestValidator(serializers.Serializer):
    input_raster = serializers.CharField(required=True)

    def validate_input_raster(self, value):
        # check first if it is a valid url file path
        try:
            validate_url_file_path(value)
        except ValidationError:
            # assume this a static file name
            static_file_path = get_static_data_file_path(value)
            if static_file_path is None:
                raise serializers.ValidationError("Invalid static data file name:%s" % value)

        return value


class SubsetDEMRequestValidator(InputRasterURLorStaticRequestValidator):
    xmin = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    xmax = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    ymin = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    ymax = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    output_raster = serializers.CharField(required=False)


class SubsetUSGSNEDDEMRequestValidator(serializers.Serializer):
    xmin = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    xmax = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    ymin = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    ymax = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    output_raster = serializers.CharField(required=True)


class SubsetProjectResampleRasterRequestValidator(SubsetDEMRequestValidator):
    resample = serializers.CharField(min_length=1, required=False, default='near')
    dx = serializers.IntegerField(required=True)
    dy = serializers.IntegerField(required=True)


class SubsetProjectResampleRasterEPSGRequestValidator(SubsetProjectResampleRasterRequestValidator):
    epsg_code = serializers.IntegerField(required=True)


class InputRasterRequestValidator(serializers.Serializer):
    input_raster = serializers.URLField(required=True)


class InputNetCDFURLRequestValidator(serializers.Serializer):
    input_netcdf = serializers.URLField(required=True)


class InputNetCDFURLorStaticRequestValidator(serializers.Serializer):
    input_netcdf = serializers.CharField(required=True)

    def validate_input_netcdf(self, value):
        # check first if it is a valid url file path
        try:
            validate_url_file_path(value)
        except ValidationError:
            # assume this a static file name
            static_file_path = get_static_data_file_path(value)
            if static_file_path is None:
                raise serializers.ValidationError("Invalid static data file name:%s" % value)

        return value


class DelineateWatershedRequestValidator(serializers.Serializer):
    outletPointX = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    outletPointY = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    epsgCode = serializers.IntegerField(required=True)
    streamThreshold = serializers.IntegerField(required=True)
    input_DEM_raster = serializers.URLField(required=True)
    output_raster = serializers.CharField(required=True)
    output_outlet_shapefile = serializers.CharField(required=True)


class DelineateWatershedAtShapeFileRequestValidator(serializers.Serializer):
    streamThreshold = serializers.IntegerField(required=True)
    input_DEM_raster = serializers.URLField(required=True)
    input_outlet_shapefile = serializers.URLField(required=True)
    output_raster = serializers.CharField(required=True)
    output_outlet_shapefile = serializers.CharField(required=True)

    def validate_input_outlet_shapefile(self, value):
        try:
            validate_url_file_path(value)
        except NotFound:
            raise serializers.ValidationError("Invalid input outlet shapefile:%s" % value)

        if not value.endswith('.zip'):
            raise serializers.ValidationError("Invalid input outlet shapefile. Shapefile needs to be a zip file:%s" % value)

        return value

    def validate_output_outlet_shapefile(self, value):
        if not value.endswith('.shp'):
            raise serializers.ValidationError("Invalid output outlet shapefile. Shapefile needs to be a .shp file:%s" % value)

        return value

class CreateOutletShapeRequestValidator(serializers.Serializer):
    outletPointX = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    outletPointY = serializers.DecimalField(required=True, max_digits=12, decimal_places=8)
    output_shape_file_name = serializers.CharField(required=False)


class RasterToNetCDFRequestValidator(InputRasterRequestValidator):
    output_netcdf = serializers.CharField(required=False)
    increasing_x = serializers.BooleanField(required=False)
    increasing_y = serializers.BooleanField(required=False)
    output_varname = serializers.CharField(required=False)

class ComputeRasterAspectRequestValidator(InputRasterRequestValidator):
    output_raster = serializers.CharField(required=False)


class ComputeRasterSlopeRequestValidator(InputRasterRequestValidator):
    output_raster = serializers.CharField(required=False)


class ReverseNetCDFYaxisRequestValidator(InputNetCDFURLRequestValidator):
    output_netcdf = serializers.CharField(required=False)


class ConvertNetCDFUnitsRequestValidator(InputNetCDFURLRequestValidator):
    output_netcdf = serializers.CharField(required=False)
    variable_name = serializers.CharField(required=True)
    variable_new_units = serializers.CharField(required=False)
    multiplier_factor = serializers.DecimalField(required=False, default=1.0, max_digits=12, decimal_places=8)
    offset = serializers.DecimalField(required=False, default=0, max_digits=12, decimal_places=8)


class ReverseNetCDFYaxisAndRenameVariableRequestValidator(ReverseNetCDFYaxisRequestValidator):
    input_varname = serializers.CharField(required=False)
    output_varname = serializers.CharField(required=False)


class ProjectRasterRequestValidator(InputRasterRequestValidator):
    utmZone = serializers.IntegerField(required=True)
    output_raster = serializers.CharField(required=False)


class CombineRastersRequestValidator(serializers.Serializer):
    input_raster1 = serializers.URLField(required=True)
    input_raster2 = serializers.URLField(required=True)
    output_raster = serializers.CharField(required=False)


class ResampleRasterRequestValidator(InputRasterRequestValidator):
    dx = serializers.IntegerField(required=True)
    dy = serializers.IntegerField(required=True)
    # TODO: may be this should be a choice type field
    resample = serializers.CharField(min_length=1, required=False, default='near')
    output_raster = serializers.CharField(required=False)


class ProjectResampleRasterRequestValidator(ResampleRasterRequestValidator):
    pass


class ProjectResampleRasterUTMRequestValidator(ProjectResampleRasterRequestValidator):
    utm_zone = serializers.IntegerField(required=True)


class ProjectResampleRasterEPSGRequestValidator(ProjectResampleRasterRequestValidator):
    epsg_code = serializers.IntegerField(required=True)


class SubsetRasterToReferenceRequestValidator(InputRasterRequestValidator):
    reference_raster = serializers.URLField(required=True)
    output_raster = serializers.CharField(required=False)


class SubsetNetCDFToReferenceRequestValidator(InputNetCDFURLorStaticRequestValidator):
    reference_raster = serializers.URLField(required=True)
    output_netcdf = serializers.CharField(required=False)


class ProjectNetCDFRequestValidator(InputNetCDFURLRequestValidator):
    utm_zone = serializers.IntegerField(required=True)
    output_netcdf = serializers.CharField(required=False)
    variable_name = serializers.CharField(required=True)


class SubsetNetCDFByTimeDimensionRequestValidator(InputNetCDFURLorStaticRequestValidator):
    time_dim_name = serializers.CharField(required=True)
    start_time_index = serializers.IntegerField(required=True)
    end_time_index = serializers.IntegerField(required=True)
    output_netcdf = serializers.CharField(required=False)

    def validate_start_time_index(self, value):
        if value < 0:
            raise serializers.ValidationError("Invalid start_time_index value:%s. It must be a positive integer." % value)
        return value

    def validate_end_time_index(self, value):
        if value < 0:
            raise serializers.ValidationError("Invalid end_time_index value:%s. It must be a positive integer." % value)
        return value

    def validate(self, data):
        """
        Check that the start_time_index is before the end_time_index.
        """
        if data['start_time_index'] > data['end_time_index']:
            raise serializers.ValidationError("start time index must be a value less than the end time index")

        return data


class ResampleNetCDFRequestValidator(InputNetCDFURLRequestValidator):
    reference_netcdf = serializers.URLField(required=True)
    output_netcdf = serializers.CharField(required=False)
    variable_name = serializers.CharField(required=True)


class ConcatenateNetCDFRequestValidator(serializers.Serializer):
    input_netcdf1 = serializers.URLField(required=True)
    input_netcdf2 = serializers.URLField(required=True)
    output_netcdf = serializers.CharField(required=False)


class ProjectSubsetResampleNetCDFRequestValidator(ResampleNetCDFRequestValidator):
    pass


class ProjectClipRasterRequestValidator(InputRasterURLorStaticRequestValidator):
    output_raster = serializers.CharField(required=False)
    reference_raster = serializers.CharField(required=True)


class GetCanopyVariablesRequestValidator(serializers.Serializer):
    in_NLCDraster = serializers.URLField(required=True)
    out_ccNetCDF = serializers.CharField(required=False)
    out_hcanNetCDF = serializers.CharField(required=False)
    out_laiNetCDF = serializers.CharField(required=False)


class GetCanopyVariableRequestValidator(serializers.Serializer):
    in_NLCDraster = serializers.URLField(required=True)
    output_netcdf = serializers.CharField(required=True)
    variable_name = serializers.CharField(required=True)

    def validate_variable_name(self, value):
        if value not in ('cc', 'hcan', 'lai'):
            raise serializers.ValidationError("Invalid canopy variable name:%s. " % value)
        return value

class ProjectShapeFileUTMRequestValidator(serializers.Serializer):
    input_shape_file = serializers.URLField(required=True)
    output_shape_file = serializers.CharField(required=False)
    utm_zone = serializers.IntegerField(required=True)


class ProjectShapeFileEPSGRequestValidator(serializers.Serializer):
    input_shape_file = serializers.URLField(required=True)
    output_shape_file = serializers.CharField(required=False)
    epsg_code = serializers.IntegerField(required=True)


class ZipMyFilesRequestValidator(serializers.Serializer):
    file_names = serializers.CharField(min_length=5, required=True)
    zip_file_name = serializers.CharField(min_length=5, required=True)

    def validate_file_names(self, value):
        file_names = value.split(',')
        if len(file_names) == 0:
            raise serializers.ValidationError("No file name provided to be zipped")

        for file_name in file_names:
            if not validate_file_name(file_name):
                raise serializers.ValidationError("%s is not a valid file name" % file_name)

        return file_names

    def validate_zip_file_name(self, value):
        if not value.endswith('.zip'):
            raise serializers.ValidationError("%s is not a valid zip file name" % value)

        if not validate_file_name(value):
                raise serializers.ValidationError("%s is not a valid file name" % value)

        return value


class HydroShareCreateResourceRequestValidator(serializers.Serializer):
    hs_username = serializers.CharField(min_length=1, required=True)
    hs_password = serializers.CharField(min_length=1, required=True)
    file_name = serializers.CharField(min_length=5, required=True)
    resource_type = serializers.CharField(min_length=5, required=True)
    title = serializers.CharField(min_length=5, max_length=200, required=False)
    abstract = serializers.CharField(min_length=5, required=False)
    keywords = serializers.CharField(required=False)

    def validate_keywords(self, value):
        if value:
            kws = value.split(',')
            if len(kws) == 0:
                raise serializers.ValidationError("%s must be a comma separated string" % value)
            return kws

class DownloadStreamflowRequestValidator(serializers.Serializer):
    USGS_gage = serializers.CharField(required=True)
    Start_Year = serializers.IntegerField(required=True)
    End_Year = serializers.IntegerField(required=True)
    output_streamflow = serializers.CharField(required=True)

class DownloadClimatedataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    Start_Year = serializers.IntegerField(required=True)
    End_Year = serializers.IntegerField(required=True)
    output_rainfile = serializers.CharField(required=True)
    output_temperaturefile = serializers.CharField(required=True)
    output_cliparfile = serializers.CharField(required=True)
    output_gagefile = serializers.CharField(required=True)
    def validate_output_gagefile(self, value):
        if not value.endswith('.shp'):
            raise serializers.ValidationError("Invalid output outlet shapefile. Shapefile needs to be a .shp file:%s" % value)

        return value

class DownloadSoildataRequestValidator(serializers.Serializer):
 
    Watershed_Raster = serializers.URLField(required=True)
    output_f_file = serializers.CharField(required=True)
    output_dth1_file = serializers.CharField(required=True)
    output_dth2_file = serializers.CharField(required=True)
    output_k_file = serializers.CharField(required=True)
    output_psif_file = serializers.CharField(required=True)
    output_sd_file = serializers.CharField(required=True)
    output_tran_file = serializers.CharField(required=True)



class WatershedDelineationdataRequestValidator(serializers.Serializer):
    DEM_Raster = serializers.URLField(required=True)
    Outlet_shapefile = serializers.URLField(required=True)
    Src_threshold = serializers.IntegerField(required=True)
    Min_threshold = serializers.IntegerField(required=True)
    Max_threshold = serializers.IntegerField(required=True)
    Number_threshold= serializers.IntegerField(required=True)

    output_pointoutletshapefile= serializers.CharField(required=True)
    output_watershedfile= serializers.CharField(required=True)
    output_treefile=serializers.CharField(required=True)
    output_coordfile=serializers.CharField(required=True)
    output_streamnetfile=serializers.CharField(required=True)
    output_slopareafile=serializers.CharField(required=True)
    output_distancefile=serializers.CharField(required=True)

    def validate_Outlet_shapefile(self, value):
        try:
            validate_url_file_path(value)
        except NotFound:
            raise serializers.ValidationError("Invalid input outlet shapefile:%s" % value)

        if not value.endswith('.zip'):
            raise serializers.ValidationError("Invalid input outlet shapefile. Shapefile needs to be a zip file:%s" % value)

        return value

    def validate_output_pointoutletshapefile(self, value):
        if not value.endswith('.shp'):
            raise serializers.ValidationError("Invalid output outlet shapefile. Shapefile needs to be a .shp file:%s" % value)

        return value
    def validate_output_streamnetfile(self, value):
        if not value.endswith('.shp'):
            raise serializers.ValidationError("Invalid output outlet shapefile. Shapefile needs to be a .shp file:%s" % value)

        return value



class ReachLinkdataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    DEM_Raster = serializers.URLField(required=True)
    treefile = serializers.URLField(required=True)
    coordfile = serializers.URLField(required=True)

    output_reachfile= serializers.CharField(required=True)
    output_reachareafile= serializers.CharField(required=True)
    output_nodefile = serializers.CharField(required=True)
    output_rchpropertiesfile = serializers.CharField(required=True)

class dist_wetness_distributiondataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    SaR_Raster = serializers.URLField(required=True)
    Dist_Raster= serializers.URLField(required=True)
    output_distributionfile= serializers.CharField(required=True)

class getprismrainfalldataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    output_raster = serializers.CharField(required=True)

class createrainweightdataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    Rain_gauge_shapefile = serializers.URLField(required=True)
    nodelink_file=serializers.URLField(required=True)
    annual_rainfile=serializers.URLField(required=True)
    output_rainweightfile = serializers.CharField(required=True)
class createbasinparameterdataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    DEM_Raster = serializers.URLField(required=True)
    f_raster = serializers.URLField(required=True)
    k_raster = serializers.URLField(required=True)
    dth1_raster = serializers.URLField(required=True)
    dth2_raster = serializers.URLField(required=True)
    sd_raster = serializers.URLField(required=True)
    tran_raster = serializers.URLField(required=True)
    psif_raster=serializers.URLField(required=True)
    lulc_raster = serializers.URLField(required=True)
    lutlc = serializers.URLField(required=True)
    lutkc = serializers.URLField(required=True)
    parameter_specficationfile = serializers.URLField(required=True)

    nodelinksfile=serializers.URLField(required=True)
    output_basinfile = serializers.CharField(required=True)

class createlatlonfromxydataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    output_latlonfromxyfile = serializers.CharField(required=True)
class createparmfiledataRequestValidator(serializers.Serializer):
    Watershed_Raster = serializers.URLField(required=True)
    output_parspcfile = serializers.CharField(required=True)


