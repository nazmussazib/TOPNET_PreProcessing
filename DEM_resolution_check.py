__author__ = 'shams'

from hydrogate import HydroDS
import settings
# Create HydroDS object passing user login account for HydroDS api server
HDS = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)
workingDir = "F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\C22Watershed\work_30M"
# Domain bounding box in geographic coordinates left, top, right, bottom.  Must enclose watershed of interest
#Logan River
leftX, topY, rightX, bottomY = -93.254, 31.174, -92.716, 30.637
# Grid projection
epsgCode = 102003 ## albers conic projection
dx,dy  = 30,30 #  Grid cell sizes (m) for reprojection
# Set parameters for watershed delineation
streamThreshold =1000
pk_min_threshold=1000
pk_max_threshold=10000
pk_num_thershold=12
watershedName = 'WhLA3M'
#lat_outlet = 41.744
#lon_outlet = -111.7836
#### model start and end dates
start_year=1995
end_year=2010
usgs_gage_number='08014500'


#DEM_30M=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\dem_C22_30M.tif'
#upload_30m_DEM =HDS.upload_file(file_to_upload=DEM_30M) ##file is projected
#upload DEM 10m for C22 Watershed
#DEM="F:\\USU_Research_work_update_March_30_2014\\DEM_SSURGO\\C22Watershed\\work_3M\\demC223m_final.tif'
#upload_DEM =HDS.upload_file(file_to_upload=DEM) ## file is projected
upload_DEM ='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/dem_C22_30M1.tif'
##uploading look up table file
lutlc=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\C22Watershed\work_10M\lutluc.txt'
upload_lutlcfile =HDS.upload_file(file_to_upload=lutlc) ##file is projected
lutkc=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\C22Watershed\work_10M\lutkc.txt'
upload_lutkcfile=HDS.upload_file(file_to_upload=lutkc) ##file is projected
#upload shapefile
outlet=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\C22Watershed\work_10M\outlet_C22.zip'
upload_shapefile=HDS.upload_file(file_to_upload=outlet) ## file is projected
#upload soil file extent of DEM and check resolution
soil=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\C22Watershed\work_30M\soil_C22_30M.tif' ## soil must be in the same dimension of watershed otherwise will not work
upload_SOIL =HDS.upload_file(file_to_upload=soil) ##file is projected





nlcd_raster_resource = 'nlcd2011CONUS.tif'
#uploading look up table file
""" Subset DEM and Delineate Watershed"""
# input_static_DEM='nedWesternUS.tif'
# subsetDEM_request = HDS.subset_raster(input_raster=upload_DEM, left=leftX, top=topY, right=rightX,
#                                     bottom=bottomY,output_raster=watershedName + 'DEM84.tif')
#
# myWatershedDEM = watershedName + 'Proj' + str(dx) + '.tif'
# WatershedDEM = HDS.project_resample_raster(input_raster_url_path=subsetDEM_request['output_raster'],
#                                                      cell_size_dx=dx, cell_size_dy=dy, epsg_code=epsgCode,
#                                                       output_raster=myWatershedDEM,resample='bilinear')

# outlet_shapefile_result = HDS.create_outlet_shapefile(point_x=lon_outlet, point_y=lat_outlet,
#                                                      output_shape_file_name=watershedName+'Outlet.shp')
# project_shapefile_result = HDS.project_shapefile(outlet_shapefile_result['output_shape_file_name'],
#                                                  watershedName + 'OutletProj.shp',
#                                                epsg_code=epsgCode)


Watershed_prod = HDS.delineate_watershed_peuker_douglas(input_raster_url_path=upload_DEM,
                                threshold=streamThreshold,peuker_min_threshold=pk_min_threshold,
                                peuker_max_threshold=pk_max_threshold,peuker_number_threshold=pk_num_thershold,
                                input_outlet_shapefile_url_path=upload_shapefile,
                                output_watershed_raster=watershedName + str(dx) +'WS.tif',
                                output_outlet_shapefile=watershedName + 'moveOutlet2.shp',
                                output_streamnetfile=watershedName+'net.shp',
                                output_treefile=watershedName+'tree.txt',
                                output_coordfile=watershedName+'coord.txt',
                                output_slopearea_raster=watershedName+'slparr.tif',
                                output_distance_raster=watershedName+'dist.tif')


"""getting and processed climate data"""
download_process_climatedata=HDS.get_daymet_data(input_raster_url_path=Watershed_prod['output_watershedfile'],
                                    start_year=start_year,end_year=end_year,
                                    output_gagefile='Climate_Gage.shp',output_rainfile='rain.dat',
                                    output_temperaturefile='tmaxtmintdew.dat',output_cliparfile='clipar.dat')



"""create nodelink and reachlink information"""
Create_Reach_Nodelink=HDS.reachlink(input_DEM_raster_url_path=upload_DEM,input_watershed_raster_url_path=Watershed_prod['output_watershedfile']
                                    ,input_treefile=Watershed_prod['output_treefile'],input_coordfile=Watershed_prod['output_coordfile'],
                                    output_reachfile='rchlink.txt',output_nodefile='nodelinks.txt',output_reachareafile='rchareas.txt',output_rchpropertiesfile='rchproperties.txt')


##get distribution
Create_wet_distribution=HDS.distance_wetness_distribution(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
                                   input_sloparearatio_raster_url_path=Watershed_prod['output_slopareafile'],input_distancnetostream_raster_url_path=Watershed_prod['output_distancefile'],
                                   output_distributionfile='distribution.txt')

##getting landcover data

subset_NLCD_result = HDS.project_clip_raster(input_raster=nlcd_raster_resource,ref_raster_url_path=Watershed_prod['output_watershedfile'],output_raster='lulcmmef.tif')
#mukey_raster_resource='soil_mukey_westernUS.tif'
#soil_raster='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/watershed_mukey.tif'
#http://hydrods-dev.uwrl.usu.edu:20199/api/dataservice/projectandcliprastertoreference?input_raster=soil_mukey_westernUS.tif&reference_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiver30WS.tif&output_raster=nlncd_spwan_proj_clip.tif

#subset_soil_data= HDS.project_clip_raster(input_raster=mukey_raster_resource,ref_raster_url_path=ref_raster_url_path,output_raster='watershed_mukey.tif')
#
soil_data=HDS.get_soil_data(input_raster_url_path=upload_SOIL,output_f_raster='f.tif',output_k_raster='ko.tif',output_dth1_raster='dth1.tif'
                         ,output_dth2_raster='dth2.tif',output_psif_raster='psif.tif',output_sd_raster='sd.tif',output_tran_raster='trans.tif')
#create parameterspecificationfile
paramlisfile=HDS.createparameterlistfile(input_watershed_raster_url_path=upload_DEM,output_file=watershedName+'param.txt')

##creating basinparameter file
basinparfile=HDS.create_basinparamterfile(input_DEM_raster_url_path=upload_DEM,input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
                                          input_f_url_path=soil_data['output_f_file'],input_dth1_url_path=soil_data['output_dth1_file'],
                                          input_dth2_url_path=soil_data['output_dth2_file'],input_k_url_path=soil_data['output_k_file'],
                                          input_sd_url_path=soil_data['output_sd_file'],input_psif_url_path=soil_data['output_psif_file'],
                                          input_tran_url_path=soil_data['output_tran_file'],
                                          input_lulc_url_path=subset_NLCD_result['output_raster'],input_lutlc_url_path=upload_lutlcfile,
                                          input_lutkc_url_path=upload_lutkcfile,input_parameterspecfile_url_path=paramlisfile['output_parspcfile'],
                                          input_nodelinksfile_url_path=Create_Reach_Nodelink['output_nodefile'], output_basinparameterfile='basinpars.txt')



#create rainweight file
### Subset DEM and Delineate Watershed
# input_static_prismrainfall  = 'PRISM_ppt_30yr_normal_800mM2_annual_bil.bil'
# subsetprismrainfall_request = HDS.subset_raster(input_raster=input_static_prismrainfall , left=leftX-0.05, top=topY+0.05, right=rightX+0.05,
#                                       bottom=bottomY-0.05,output_raster=watershedName + 'prism84.tif')
#
# subset_NLCD_result = HDS.project_clip_raster(input_raster=nlcd_raster_resource,ref_raster_url_path=Watershed_prod['output_watershedfile'],output_raster='lulcmmef.tif')
#
# ## notes problem no such function susetrastertobbox is supported
# myWatershedPRISM= watershedName + 'ProjPRISM' + str(dx) + '.tif'
# WatershedPRISMRainfall= HDS.project_resample_raster(input_raster_url_path=subsetprismrainfall_request['output_raster'],
#                                                       cell_size_dx=100, cell_size_dy=100, epsg_code=epsgCode,
#                                                       output_raster=myWatershedPRISM,resample='bilinear')
#
#
# project_climate_shapefile_result = HDS.project_shapefile(download_process_climatedata['output_gagefile'], 'ClimateGageProj.shp',
#                                                  epsg_code=epsgCode)
#
#
#
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
# #### upload wind file - there is no wind data in Daymet
# HDS.upload_file(workingDir+'V.dat')
#
# #upload topnet control and watermangement files
# HDS.upload_file(workingDir+'control.dat')
# HDS.upload_file(workingDir+'inputcontrol.dat')
# HDS.upload_file(workingDir+'outputcontrol.dat')
# HDS.upload_file(workingDir+'param.dat')
# HDS.upload_file(workingDir+'siteinitial.dat')
#
# topnet_inputPackage_dict = ['control.dat','inputcontrol.dat','outputcontrol.dat','param.dat','siteinitial.dat','V.dat',
#                          'watershed.nc', 'aspect.nc', 'slope.nc', 'cc.nc', 'hcan.nc', 'lai.nc',
#                          'vp0.nc', 'srad0.nc', 'tmin0.nc', 'tmax0.nc', 'prcp0.nc']
# zip_files_result = HDS.zip_files(files_to_zip=topnet_inputPackage_dict, zip_file_name=watershedName+'.zip')
# #### save UEB input package as HydroShare resource
# hs_title = 'UEB input package for the '+watershedName+' watershed'
# hs_abstract = hs_title +'. It was created by the CI-WATER HydroDS.' + 'Input variables were re-sampled into '+str(dxRes)+ " m grid cells"
# hs_keywords=['HydroShare', 'HydroDS', 'DEM', watershedName+' WS']
# HDS.set_hydroshare_account(settings.HS_USER_NAME, settings.HS_PASSWORD)
# HDS.create_hydroshare_resource(file_name=watershedName+str(dxRes)+'.zip', resource_type ='GenericResource', title= hs_title,
#                                abstract= hs_abstract, keywords= hs_keywords)
# print('Finished TOPNET input setup')