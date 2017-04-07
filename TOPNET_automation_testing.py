__author__ = 'shams'
from hydrogate import HydroDS
import os
import settings
# Create HydroDS object passing user login account for HydroDS api server
HDS = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)
workingDir = "E:\\USU_Research_work\\TOPNET_Web_Processing\\Testing_results\\TestLogan"
# Domain bounding box in geographic coordinates left, top, right, bottom.  Must enclose watershed of interest
#Logan River
leftX, topY, rightX, bottomY = -111.822, 42.128, -111.438, 41.686
# Grid projection
epsgCode = 102003 ## albers conic projection
dx,dy  = 30,30  #  Grid cell sizes (m) for reprojection
# Set parameters for watershed delineation
streamThreshold = 100
pk_min_threshold=500
pk_max_threshold=5000
pk_num_thershold=12
watershedName = 'LoganRiver'
lat_outlet = 41.744
lon_outlet = -111.7836
#### model start and end dates
start_year=2000
end_year=2014
usgs_gage_number='10109001'

# nlcd_raster_resource = 'nlcd2011CONUS.tif'
# #uploading look up table file
# """ Subset DEM and Delineate Watershed"""
# input_static_DEM='nedWesternUS.tif'
# input_static_Soil_mukey='soil_mukey_westernUS.tif'
# upload_lutkcfile=HDS.upload_file(os.path.join(workingDir,"lutkc.txt"))
# #upload topnet control and watermangement files
# upload_lutlcfile=HDS.upload_file(os.path.join(workingDir,"lutluc.txt"))
#
# subsetDEM_request = HDS.subset_raster(input_raster=input_static_DEM, left=leftX, top=topY, right=rightX,
#                                       bottom=bottomY,output_raster=watershedName + 'DEM84.tif')
#
# myWatershedDEM = watershedName + 'Proj' + str(dx) + '.tif'
# WatershedDEM = HDS.project_resample_raster(input_raster_url_path=subsetDEM_request['output_raster'],
#                                                       cell_size_dx=dx, cell_size_dy=dy, epsg_code=epsgCode,
#                                                        output_raster=myWatershedDEM,resample='bilinear')
#
# # subsetSoil_request = HDS.subset_raster(input_raster=input_static_Soil_mukey, left=leftX, top=topY, right=rightX,
# #                                       bottom=bottomY,output_raster=watershedName + 'Soil84.tif')
# # myWatershedSoil= watershedName + 'ProjSoil' + str(dx) + '.tif'
# # WatershedSoil = HDS.project_resample_raster(input_raster_url_path=subsetSoil_request['output_raster'],
# #                                                       cell_size_dx=dx, cell_size_dy=dy, epsg_code=epsgCode,
# #                                                        output_raster=myWatershedSoil,resample='bilinear')
#
#
# outlet_shapefile_result = HDS.create_outlet_shapefile(point_x=lon_outlet, point_y=lat_outlet,
#                                                       output_shape_file_name=watershedName+'Outlet.shp')
# project_shapefile_result = HDS.project_shapefile(outlet_shapefile_result['output_shape_file_name'],
#                                                  watershedName + 'OutletProj.shp',
#                                                  epsg_code=epsgCode)
# Watershed_prod = HDS.delineate_watershed_peuker_douglas(input_raster_url_path=WatershedDEM['output_raster'],
#                                 threshold=streamThreshold,peuker_min_threshold=pk_min_threshold,
#                                 peuker_max_threshold=pk_max_threshold,peuker_number_threshold=pk_num_thershold,
#                                 input_outlet_shapefile_url_path=project_shapefile_result['output_shape_file'],
#                                 output_watershed_raster=watershedName + str(dx) +'WS.tif',
#                                 output_outlet_shapefile=watershedName + 'moveOutlet2.shp',
#                                 output_streamnetfile=watershedName+'net.shp',
#                                 output_treefile=watershedName+'tree.txt',
#                                 output_coordfile=watershedName+'coord.txt',
#                                 output_slopearea_raster=watershedName+'slparr.tif',
#                                 output_distance_raster=watershedName+'dist.tif')
#
#
# """getting and processed climate data"""
# download_process_climatedata=HDS.get_daymet_data(input_raster_url_path=Watershed_prod['output_watershedfile'],
#                                     start_year=start_year,end_year=end_year,
#                                     output_gagefile='Climate_Gage.shp',output_rainfile='rain.dat',
#                                     output_temperaturefile='tmaxtmintdew.dat',output_cliparfile='clipar.dat')
#
#
#
# """create nodelink and reachlink information"""
# Create_Reach_Nodelink=HDS.reachlink(input_DEM_raster_url_path=WatershedDEM['output_raster'],input_watershed_raster_url_path=Watershed_prod['output_watershedfile']
#                                     ,input_treefile=Watershed_prod['output_treefile'],input_coordfile=Watershed_prod['output_coordfile'],
#                                     output_reachfile='rchlink.txt',output_nodefile='nodelinks.txt',output_reachareafile='rchareas.txt',output_rchpropertiesfile='rchproperties.txt')
#
#
# ##get distribution
# Create_wet_distribution=HDS.distance_wetness_distribution(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
#                                    input_sloparearatio_raster_url_path=Watershed_prod['output_slopareafile'],input_distancnetostream_raster_url_path=Watershed_prod['output_distancefile'],
#                                    output_distributionfile='distribution.txt')
#
# ##getting landcover data
#
# subset_NLCD_result = HDS.project_clip_raster(input_raster=nlcd_raster_resource,ref_raster_url_path=Watershed_prod['output_watershedfile'],output_raster='lulcmmef.tif')
# ##mukey_raster_resource='soil_mukey_westernUS.tif'
# ##soil_raster='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/watershed_mukey.tif'
# #http://hydrods-dev.uwrl.usu.edu:20199/api/dataservice/projectandcliprastertoreference?input_raster=soil_mukey_westernUS.tif&reference_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiver30WS.tif&output_raster=nlncd_spwan_proj_clip.tif
#
# #subset_soil_data= HDS.project_clip_raster(input_raster=mukey_raster_resource,ref_raster_url_path=ref_raster_url_path,output_raster='watershed_mukey.tif')
# #
# ##soil_raster=HDS.subset_raster_to_reference(WatershedSoil['output_raster'], Watershed_prod['output_watershedfile'],'Soil_Mukey_all.tif', save_as=None)
#
# soil_data=HDS.get_soil_data(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],output_f_raster='f.tif',output_k_raster='ko.tif',output_dth1_raster='dth1.tif'
#                          ,output_dth2_raster='dth2.tif',output_psif_raster='psif.tif',output_sd_raster='sd.tif',output_tran_raster='trans.tif')
# #create parameterspecificationfile
#
#  #http://hydrods-dev.uwrl.usu.edu:20199/api/dataservice/downloadsoildata?Watershed_Raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiver30WS.tif&
#                     #  &output_f_file=f.tif&output_k_file=ko.tif&output_dth1_file=dth1.tif
#                         #  &output_dth2_file=dth2.tif&output_psif_file=psif.tif&output_sd_file=sd.tif&output_tran_file=trans.tif
# #create parameterspecificationfile
#
#
#
#
#
#
# paramlisfile=HDS.createparameterlistfile(input_watershed_raster_url_path=WatershedDEM['output_raster'],output_file=watershedName+'param.txt')
#
# ##creating basinparameter file
# basinparfile=HDS.create_basinparamterfile(input_DEM_raster_url_path=WatershedDEM['output_raster'],input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
#                                           input_f_url_path=soil_data['output_f_file'],input_dth1_url_path=soil_data['output_dth1_file'],
#                                           input_dth2_url_path=soil_data['output_dth2_file'],input_k_url_path=soil_data['output_k_file'],
#                                           input_sd_url_path=soil_data['output_sd_file'],input_psif_url_path=soil_data['output_psif_file'],
#                                           input_tran_url_path=soil_data['output_tran_file'],
#                                           input_lulc_url_path=subset_NLCD_result['output_raster'],input_lutlc_url_path=upload_lutlcfile,
#                                           input_lutkc_url_path=upload_lutkcfile,input_parameterspecfile_url_path=paramlisfile['output_parspcfile'],
#                                           input_nodelinksfile_url_path=Create_Reach_Nodelink['output_nodefile'], output_basinparameterfile='basinpars.txt')
#
#
#
# #create rainweight file
# ### Subset DEM and Delineate Watershed
# input_static_prismrainfall  = 'PRISM_ppt_30yr_normal_800mM2_annual_bil.bil'
# subsetprismrainfall_request = HDS.subset_raster(input_raster=input_static_prismrainfall , left=leftX-0.05, top=topY+0.05, right=rightX+0.05,
#                                       bottom=bottomY-0.05,output_raster=watershedName + 'prism84.tif')
# ## notes problem no such function susetrastertobbox is supported
# myWatershedPRISM= watershedName + 'ProjPRISM' + str(dx) + '.tif'
# WatershedPRISMRainfall= HDS.project_resample_raster(input_raster_url_path=subsetprismrainfall_request['output_raster'],
#                                                       cell_size_dx=dx, cell_size_dy=dy, epsg_code=epsgCode,
#                                                       output_raster=myWatershedPRISM,resample='bilinear')
#
# project_climate_shapefile_result = HDS.project_shapefile(download_process_climatedata['output_gagefile'], 'ClimateGageProj.shp',
#                                                  epsg_code=epsgCode)
#
# create_rainweightfile=HDS.create_rainweight(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],input_raingauge_shapefile_url_path=project_climate_shapefile_result['output_shape_file'],
#                                         input_annual_rainfile=WatershedPRISMRainfall['output_raster'],input_nodelink_file=Create_Reach_Nodelink['output_nodefile'],output_rainweightfile='rainweights.txt')
#
# ##create latlonfromxy file
# creat_latlonxyfile=HDS.createlatlonfromxy(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],output_file='latlongfromxy.txt')
#
# ##get streamflow file
# streamflow=HDS.download_streamflow(usgs_gage=usgs_gage_number,start_year=start_year, end_year=end_year, output_streamflow='streamflow_calibration.dat')
#
#
# #
##need to upload biunry flow data
##need to copy rainweights.txt as interpweight,dat
#other wise it will not work
# # #### upload wind file - there is no wind data in Daymet
# HDS.upload_file(os.path.join(workingDir,"wind.dat"))
# #upload topnet control and watermangement files
# HDS.upload_file(os.path.join(workingDir,"topinp.dat"))
# HDS.upload_file(os.path.join(workingDir,"snowparam.dat"))
# HDS.upload_file(os.path.join(workingDir,"snow.in"))
# HDS.upload_file(os.path.join(workingDir,"modelspc.dat"))
# ##upload water management files
# HDS.upload_file(os.path.join(workingDir,"MeasuredFlowInfo.txt"))
# HDS.upload_file(os.path.join(workingDir,"MonthlyDemandFraction.txt"))
# HDS.upload_file(os.path.join(workingDir,"bcpar.dat"))
# HDS.upload_file(os.path.join(workingDir,"dc.dat"))
# HDS.upload_file(os.path.join(workingDir,"rainfill.txt"))
# HDS.upload_file(os.path.join(workingDir,"Reservoir.txt"))
# HDS.upload_file(os.path.join(workingDir,"ReturnFlow.txt"))
# HDS.upload_file(os.path.join(workingDir,"Rights.txt"))
# HDS.upload_file(os.path.join(workingDir,"SeasonsDefn.txt"))
# HDS.upload_file(os.path.join(workingDir,"Source.txt"))
# HDS.upload_file(os.path.join(workingDir,"SourceMixing.txt"))
# HDS.upload_file(os.path.join(workingDir,"user.txt"))
# HDS.upload_file(os.path.join(workingDir,"WatermgmtControl.txt"))

# topnet_inputPackage_dict = ['topinp.dat','snowparam.dat','modelspc.dat','bcpar.dat','dc.dat','wind.dat','rain.dat','clipar.dat','tmaxtmintdew.dat','streamflow_calibration.dat',
#                           'rchproperties.txt', 'rchlink.txt', 'rchareas.txt', 'nodelinks.txt', 'distribution.txt', 'rainweights.txt','latlongfromxy.txt','basinpars.txt',
#                           'MonthlyDemandFraction.txt', 'MeasuredFlowInfo.txt', 'WatermgmtControl.txt', 'user.txt', 'SourceMixing.txt', 'Source.txt','rainfill.txt',
#                           'SeasonsDefn.txt','Rights.txt','ReturnFlow.txt','Reservoir.txt']
#
# zip_files_result = HDS.zip_files(files_to_zip=topnet_inputPackage_dict, zip_file_name='topenet'+'.zip')
#### save UEB input package as HydroShare resource
hs_title = 'TOPNET input package for the watershed'
hs_abstract = hs_title +'It was created by the CI-WATER HydroDS' + 'Input variables were re-sampled into '+ ' m grid cells'
hs_keywords=['HydroShare', 'HydroDS', 'DEM', 'LoganWS']
HDS.set_hydroshare_account(username='Nazmus', password='')
HDS.create_hydroshare_resource(file_name='topenet.zip', resource_type ='GenericResource', title= hs_title, abstract= hs_abstract, keywords= hs_keywords)
# print('Finished TOPNET input setup')
