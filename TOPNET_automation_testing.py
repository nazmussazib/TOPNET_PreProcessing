__author__ = 'shams'

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
HDS = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

workingDir = "E:\\USU_Research_work\\TOPNET_Web_Processing\\TOPNET_Web_services\\Test_using_hydrogate"
# Domain bounding box in geographic coordinates left, top, right, bottom.  Must enclose watershed of interest

#Little Bear River Watershed upstream of Hyrum Reservoir
leftX, topY, rightX, bottomY = -111.97, 41.629, -111.48, 41.36
leftX, topY, rightX, bottomY = -111.97, 41.629, -111.48, 41.36

# Grid projection
epsgCode = 102003 ## albers conic projection
dx,dy  = 30,30  #  Grid cell sizes (m) for reprojection

# Set parameters for watershed delineation
streamThreshold = 100
pk_min_threshold=500
pk_max_threshold=5000
pk_num_thershold=12

watershedName = 'LittleBear'

# Little Bear outlet at Hyrum Reservoir (may be approximate as move outlets to stream is used to position outlet on streams defined using streamThreshold)
lat_outlet = 41.596
lon_outlet = -111.855



#### model start and end dates
startDateTime = "2010/10/01 0"
endDateTime = "2011/06/01 0"
start_year=2000
end_year=2010
"""*************************************************************************"""

#### Subset DEM and Delineate Watershed
input_static_DEM  = 'nedWesternUS.tif'
subsetDEM_request = HDS.subset_raster(input_raster=input_static_DEM, left=leftX, top=topY, right=rightX,
                                      bottom=bottomY,output_raster=watershedName + 'DEM84.tif')
## notes problem no such function susetrastertobbox is supported

#Options for projection with epsg full list at: http://spatialreference.org/ref/epsg/
myWatershedDEM = watershedName + 'Proj' + str(dx) + '.tif'
WatershedDEM = HDS.project_resample_raster(input_raster_url_path=subsetDEM_request['output_raster'],
                                                      cell_size_dx=dx, cell_size_dy=dy, epsg_code=epsgCode,
                                                      output_raster=myWatershedDEM,resample='bilinear')
outlet_shapefile_result = HDS.create_outlet_shapefile(point_x=lon_outlet, point_y=lat_outlet,
                                                      output_shape_file_name=watershedName+'Outlet.shp')
project_shapefile_result = HDS.project_shapefile(outlet_shapefile_result['output_shape_file_name'], watershedName + 'OutletProj.shp',
                                                 epsg_code=epsgCode)



##delineate watershed using DEM and given x and y

Watershed_prod = HDS.delineate_watershed_peuker_douglas(input_raster_url_path=WatershedDEM['output_raster'], threshold=streamThreshold,
                                                        peuker_min_threshold=pk_min_threshold,peuker_max_threshold=pk_max_threshold,peuker_number_threshold=pk_num_thershold,input_outlet_shapefile_url_path=project_shapefile_result['output_shape_file'],
                                                        output_watershed_raster=watershedName + str(dx) + 'WS2.tif',output_outlet_shapefile=watershedName + 'moveOutlet2.shp',
                                                        output_treefile=watershedName+'tree.dat',output_coordfile=watershedName+'coord.dat',
                                                        output_slope_raster='tee2.tif',output_distance_raster='ter2.tif')


##create reach link
#
# Create_Reach_Nodelink=HDS.reachlink(input_DEM_raster_url_path=WatershedDEM['output_raster'],input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
#                                     input_treefile=Watershed_prod['output_treefile'],input_coordfile=Watershed_prod['output_coordfile'],
#                                     output_reachfile='reachlink.dat' ,output_nodefile='nodelinks.dat',output_rchpropertiesfile='rchproperties.dat')


##getting and processed climate data
#
# download_process_climatedata=HDS.get_daymet_data(input_raster_url_path=Watershed_prod['output_watershedfile'],start_year=start_year,end_year=end_year,
#                                               output_rainfile='rain.dat',output_temperaturefile='tmaxtmintdew.dat',output_cliparfile='clipar.dat')





##getting soil data
##need some geoprocessing work
##this uploading need to download from the geospatial data gateway system:
#
# upload_soil_MUKEY_all=
# soil_MUKEY_watershed_raster=HDS.subset_raster_to_reference(input_raster_url_path=, output_raster='watershed_MUKEY.tif')
# soil_data=HDS.get_soil_data(input_raster_url_path=soil_MUKEY_watershed_raster['output_raster'],output_f_raster='f.tif',output_k_raster='k.tif',output_dth1_raster='dth1.tif'
#                             ,output_dth2_raster='dth2.tif',output_psif_raster='psif.tif',output_sd_raster='sd.tif',output_tran_raster='Trans.tif')



##getting landcover data

##creating parameterspecfile list

##uploading look up table file

##creating basinparameter file

##creating rainwweight file

##creating streamflow file





##uploading other necessary file

##share datasets into hydroshare as zip file

