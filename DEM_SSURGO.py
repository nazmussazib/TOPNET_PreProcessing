__author__ = 'shams'

##this code is for testing

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
HDS = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

workingDir = "F:\\USU_Research_work_update_March_30_2014\\DEM_SSURGO"
# Domain bounding box in geographic coordinates left, top, right, bottom.  Must enclose watershed of interest





# Set parameters for watershed delineation
streamThreshold = 100
pk_min_threshold=1000
pk_max_threshold=10000
pk_num_thershold=12

#watershedName = 'LittleBear'




#### model start and end dates
startDateTime = "2010/10/01 0"
endDateTime = "2011/06/01 0"
start_year=2000
end_year=2010
"""*************************************************************************"""
#
# # #upload DEM 30 m for C22 Watershed
# #DEM_30M=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\dem_C22_30M.tif'
# #upload_30m_DEM =HDS.upload_file(file_to_upload=DEM_30M) ##file is projected
# #upload DEM 10m for C22 Watershed
# DEM_10M=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\dem_C22_10M.tif'
# upload_10m_DEM =HDS.upload_file(file_to_upload=DEM_10M) ## file is projected
# ##uploading look up table file
# lutlc=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\lutluc.txt'
# upload_lutlcfile =HDS.upload_file(file_to_upload=lutlc) ##file is projected
# lutkc=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\lutkc.txt'
# upload_lutkcfile=HDS.upload_file(file_to_upload=lutkc) ##file is projected
# #upload shapefile
# #outlet=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\outletC221.zip'
# #upload_shapefile=HDS.upload_file(file_to_upload=outlet) ## file is projected
# #upload soil file extent of DEM and check resolution
# soil_10M=r'F:\USU_Research_work_update_March_30_2014\DEM_SSURGO\soil.tif' ## soil must be in the same dimension of watershed otherwise will not work
# upload_10m_soil =HDS.upload_file(file_to_upload=soil_10M) ##file is projected



##delineate watershed using DEM and given x and y
#
watershedName = 'WhLA10'
# Watershed_prod = HDS.delineate_watershed_peuker_douglas(input_raster_url_path=upload_10m_DEM, threshold=streamThreshold,
#                                                         peuker_min_threshold=pk_min_threshold,peuker_max_threshold=pk_max_threshold,peuker_number_threshold=pk_num_thershold,input_outlet_shapefile_url_path=upload_shapefile,
#                                                         output_watershed_raster=watershedName+ 'WS.tif',output_outlet_shapefile=watershedName + 'moveOutlet2.shp',
#                                                         output_treefile=watershedName+'tree.txt',output_coordfile=watershedName+'coord.txt',output_streamnetfile=watershedName+'net.shp',
#                                                         output_slopearea_raster=watershedName+'slparr.tif',output_distance_raster=watershedName+'dist.tif')
#
#
# ##get distribution
# Create_wet_distribution=HDS.distance_wetness_distribution(input_watershed_raster_url_path=Watershed_prod['output_watershedfile'],
#                                     input_sloparearatio_raster_url_path=Watershed_prod['output_slopareafile'],input_distancnetostream_raster_url_path=Watershed_prod['output_distancefile'],
#                                     output_distributionfile='distribution.txt')
#
#
# ##create reach link
Watershed_Raster='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/WhLA10WS.tif'
tree='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/WhLA10tree.txt'
coor='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/WhLA10coord.txt'
#Create_Reach_Nodelink=HDS.reachlink(input_DEM_raster_url_path=upload_10m_DEM,input_watershed_raster_url_path=Watershed_Raster
                                    #,input_treefile=tree,input_coordfile=coor,
                                    #output_reachfile='reachlink.txt',output_nodefile='nodelinks.txt',output_rchpropertiesfile='rchproperties.txt')
#
#
# ##getting and processed climate data
# download_process_climatedata=HDS.get_daymet_data(input_raster_url_path=Watershed_prod['output_watershedfile'],start_year=start_year,end_year=end_year,
#                                             output_gagefile='Climate_Gage.shp',output_rainfile='rain.dat',output_temperaturefile='tmaxtmintdew.dat',output_cliparfile='clipar.dat')

##getting soil data

#soil_MUKEY_watershed_raster=HDS.subset_raster_to_reference(input_raster_url_path=, output_raster='watershed_MUKEY.tif')
#soil_data=HDS.get_soil_data(input_raster_url_path=upload_10m_soil,output_f_raster='f.tif',output_k_raster='ko.tif',output_dth1_raster='dth1.tif'
 #                         ,output_dth2_raster='dth2.tif',output_psif_raster='psif.tif',output_sd_raster='sd.tif',output_tran_raster='trans.tif')

# ##getting landcover data

NLCD_data=HDS.getlanduse_lancoverdata(input_raster_url_path=Watershed_prod['output_watershedfile'],output_raster='lulcmmef.tif')

#Land cover variables

input_parameterspecfile_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/demC22param.txt'
input_nodelinksfile_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/nodelinks.txt'
#nlcd_raster_resource = 'nlcd2011CONUS.tif'
#subset_NLCD_result = HDS.project_clip_raster(input_raster=nlcd_raster_resource,
 #                               ref_raster_url_path=upload_10m_soil,
 #                               output_raster='lulcmmef1.tif')

#soil_MUKEY_watershed_raster=HDS.subset_raster_to_reference(input_raster_url_path=subset_NLCD_result['output_raster'],
 #                                                        ref_raster_url_path=Watershed_Raster, output_raster='lulcmmef.tif')

# ##creating parameterspecfile list


paramlisfile=HDS.createparameterlistfile(input_watershed_raster_url_path=Watershed_Raster,output_file='demC22param.txt')
#paramlisfile=HDS.createparameterlistfile(input_watershed_raster_url_path=upload_10m_DEM,output_file='demC22param.txt')


#
input_f_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/f.tif'
input_dth1_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/dth1.tif'
input_dth2_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/dth2.tif'
input_k_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/ko.tif'
input_sd_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/sd.tif'
input_psif_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/psif.tif'
input_tran_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/trans.tif'
input_lulc_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/lulcmmef.tif'
input_parameterspecfile_url_path='http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/demC22param.txt'
# ##creating basinparameter file
basinparfile=HDS.create_basinparamterfile(input_DEM_raster_url_path=upload_10m_DEM,input_watershed_raster_url_path=Watershed_Raster,
                                          input_f_url_path=input_f_url_path,input_dth1_url_path=input_dth1_url_path,
                                          input_dth2_url_path=input_dth2_url_path,input_k_url_path=input_k_url_path,
                                          input_sd_url_path=input_sd_url_path,input_psif_url_path=input_psif_url_path,
                                          input_tran_url_path=input_tran_url_path,
                                          input_lulc_url_path=input_lulc_url_path,input_lutlc_url_path=upload_lutlcfile,
                                          input_lutkc_url_path=upload_lutkcfile,input_parameterspecfile_url_path=input_parameterspecfile_url_path,
                                          input_nodelinksfile_url_path=input_nodelinksfile_url_path, output_basinparameterfile='basinpars.txt')


##creating rainwweight file
#
#
http://hydrods-dev.uwrl.usu.edu:20199/api/dataservice/createbasinparameter?DEM_Raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiverProj30.tif&Watershed_Raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiver30WS.tif&parameter_specficationfile=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/LoganRiverparam.txt&nodelinksfile=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/nodelinks.txt
&f_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/f.tif&sd_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/sd.tif&lutlc=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/lutluc.txt&
k_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/ko.tif&psif_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/psif.tif&lutkc=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/lutkc.txt&
dth1_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/dth1.tif&lulc_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/lulcmmef.tif&
dth2_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/dth2.tif&
tran_raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/trans.tif&output_basinfile=basinpars2.txt

#
# #http://hydrods-dev.uwrl.usu.edu:20199/api/dataservice/createbasinparameter?DEM_Raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/demC1.tif&Watershed_Soil_Raster=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/wa.zip&parameter_specficationfile=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/demC1parspc.txt&nodelinksfile=http://hydrods-dev.uwrl.usu.edu:20199/files/data/user_5/nodelinks.txt
#
# ##creating streamflow file
#




##uploading other necessary file

##share datasets into hydroshare as zip file

