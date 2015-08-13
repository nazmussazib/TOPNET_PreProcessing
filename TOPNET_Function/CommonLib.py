
import os
import subprocess
import gdal,ogr
import sys
import glob
import shapefile
import fiona
import sys
import os
from osgeo import ogr
from osgeo import osr
from usu_data_service.servicefunctions.utils import *
from usu_data_service.servicefunctions.watershedFunctions import *
R_Code_Path = '/home/ahmet/ciwater/usu_data_service/topnet_data_service/TOPNET_Function/RCODE'
MPI_dir='/usr/local/bin'
np=8
TauDEM_dir='/home/ahmet/ciwater/usu_data_service/topnet_data_service/TauDEM'
Exe_dir='/home/ahmet/ciwater/usu_data_service/topnet_data_service/TOPNET_Basin_Properties'
Base_Data_dir='/home/ahmet/ciwater/usu_data_service/topnet_data_service/Base_Data/'

def watershed_delineation(DEM_Raster,Outlet_shapefile,Src_threshold,Min_threshold,Max_threshold,Number_threshold, output_pointoutletshapefile,output_watershedfile,output_treefile,output_coordfile,output_slopareafile,output_distancefile):

    head,tail=os.path.split(str(DEM_Raster))

    In_Out_dir=str(head)
    base_name=os.path.basename(DEM_Raster)
    Input_Dem=os.path.splitext(base_name)[0]
    Outlet=Outlet_shapefile

    input_raster = os.path.splitext(DEM_Raster)[0]      #remove the .tif
    # pit remove
    #cmdString = "pitremove -z "+input_raster+".tif"+" -fel "+input_raster+"fel.tif"
    #retDictionary = call_subprocess(cmdString,'pit remove')
    #if retDictionary['success']=="False":
        #return retDictionary



    cmdstring=PITREMOVE(MPI_dir,np,TauDEM_dir, In_Out_dir,Input_Dem)
    print(cmdstring)
    retDictionary=call_subprocess(cmdstring,'pitremove')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(D8FLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'d8flow')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(D8CONTRIBUTING_AREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'d8area')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(THRESHOLD(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Src_threshold),'threshold')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(MOVEOUTLETTOSTREAMS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Outlet,output_pointoutletshapefile),'moveoutlet')
    if retDictionary['success'] == "False":
        return retDictionary
    #
    # driverName = "ESRI Shapefile"
    # driver = ogr.GetDriverByName(driverName)
    # dataset = driver.Open(Outlet_shapefile)
    # layer = dataset.GetLayer()
    # srs = layer.GetSpatialRef()
    # baseName = os.path.splitext(output_pointoutletshapefile)[0]
    # projFile = baseName+".prj"
    # #srsString = "+proj=utm +zone="+str(utmZone)+" +ellps=GRS80 +datum=NAD83 +units=m"
    # #srs = osr.SpatialReference()
    # #srs.ImportFromEPSG(epsgCode)
    # #srs.ImportFromProj4(srsString)
    # srs.MorphFromESRI()
    # file = open(projFile, "w")
    # file.write(srs.ExportToWkt())
    # file.close()

    ##add ID field to move outlets to stream file
    # Read in our existing shapefile
    r = shapefile.Reader(output_pointoutletshapefile)
   # Create a new shapefile in memory
    w = shapefile.Writer()
   # Copy over the existing fields
    w.fields = list(r.fields)
   #  Add our new field using the pyshp API
    w.field("ID", "C", "40")

   # We'll create a counter in this example
   # to give us sample data to add to the records
   #  so we know the field is working correctly.
    i=1

   # Loop through each record, add a column.  We'll
   # insert our sample data but you could also just
   # insert a blank string or NULL DATA number
   # as a place holder
    for rec in r.records():
       rec.append(i)
       i+=1
       # Add the modified record to the new shapefile
       w.records.append(rec)

   # Copy over the geometry without any changes
    w._shapes.extend(r.shapes())
    w.save(output_pointoutletshapefile)

   # Save as a new shapefile


    retDictionary=call_subprocess(PEUKERDOUGLAS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'peuker')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(ACCUMULATING_STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_pointoutletshapefile),'aread8')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary= call_subprocess(DROP_ANALYSIS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Min_threshold,Max_threshold,Number_threshold,output_pointoutletshapefile),'dropana')
    if retDictionary['success'] == "False":
        return retDictionary
    fileHandle = open (os.path.join(In_Out_dir,Input_Dem+"drp.txt"),"r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    LL= lineList[-1]
    thres=float(LL[25:35])
    if(thres>0):
        thres=thres
    else:
        thres=float(Max_threshold)

    retDictionary=call_subprocess(STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,thres),'create strea')
    if retDictionary['success'] == "False":
        return retDictionary

    retDictionary=call_subprocess(StreamNet(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_pointoutletshapefile,output_watershedfile,output_treefile, output_coordfile),'delineatewatershed')
    if retDictionary['success'] == "False":
        return retDictionary

    retDictionary=call_subprocess(WETNESS_INDEX(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_slopareafile),'sloparearatio')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(DISTANCE_DOWNSTREAM(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem, output_distancefile),'distactnetostream')
    if retDictionary['success'] == "False":
        return retDictionary
    return {'success': 'True', 'message': 'Watershed Delineation successful'}


def PITREMOVE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))
    commands.append(os.path.join(TauDEM_dir, "pitremove"));commands.append("-z")
    commands.append(os.path.join(In_Out_dir,Input_Dem+".tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def D8FLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));

    commands.append(os.path.join(TauDEM_dir, "d8flowdir"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-sd8")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"sd8.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def D8CONTRIBUTING_AREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));

    commands.append(os.path.join(TauDEM_dir, "aread8"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DINFFLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "dinfflowdir"));commands.append("-ang")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ang.tif"));commands.append("-slp")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"slp.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DINFCONTRIBUTINGAREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "areadinf"));commands.append("-ang")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ang.tif"));commands.append("-sca")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"sca.tif"));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command


def THRESHOLD(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Src_threshold):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "threshold"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"src.tif"));commands.append("-thresh");commands.append(str(Src_threshold))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def MOVEOUTLETTOSTREAMS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Outlet,output_pointoutletshapefile):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "moveoutletstostrm"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"src.tif"));commands.append("-o");commands.append(os.path.join((In_Out_dir+Outlet), Outlet))
    commands.append("-om");commands.append(os.path.join(In_Out_dir, output_pointoutletshapefile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def PEUKERDOUGLAS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "peukerdouglas"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-ss")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ss.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command


def ACCUMULATING_STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_pointoutletshapefile):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "aread8"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-o")
    commands.append(os.path.join(In_Out_dir, output_pointoutletshapefile));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-wg")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ss.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DROP_ANALYSIS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Min_threshold,Max_threshold,Number_threshold,output_pointoutletshapefile):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))
    commands.append(os.path.join(TauDEM_dir, "dropanalysis"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-drp")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"drp.txt"));commands.append("-o")
    commands.append(os.path.join(In_Out_dir, output_pointoutletshapefile));commands.append("-par")
    commands.append(str(Min_threshold));commands.append(str(Max_threshold));commands.append(str(Number_threshold));commands.append(str(0))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def FIND_OPTIMUM(In_Out_dir,Input_Dem):
    fileHandle = open(os.path.join(In_Out_dir,Input_Dem+"drp.txt"),"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    LL= lineList[-1]
    #global thres
    thres=LL[25:35]

    return thres

def STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,thershold):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "threshold"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src2.tif"));commands.append("-thresh")
    commands.append(str(thershold))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command



def StreamNet(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_pointoutletshapefile,output_watershedfile,output_treefile,output_coordfile):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "streamnet"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src2.tif"));commands.append("-ord")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ord2.tif"));commands.append("-tree")
    commands.append(os.path.join(In_Out_dir,output_treefile));commands.append("-coord")
    commands.append(os.path.join(In_Out_dir,output_coordfile));commands.append("-net")
    commands.append(os.path.join(In_Out_dir,"Stream_network.shp"));commands.append("-w")
    commands.append(os.path.join(In_Out_dir,output_watershedfile));commands.append("-o")
    commands.append(os.path.join(In_Out_dir,output_pointoutletshapefile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def WETNESS_INDEX(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_slopareafile):
    commands=[]
   # commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "slopearearatio"));commands.append("-slp")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"sd8.tif"));commands.append("-sca")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-sar")
    commands.append(os.path.join(In_Out_dir,output_slopareafile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DISTANCE_DOWNSTREAM(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,output_distancefile):
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np))

    commands.append(os.path.join(TauDEM_dir, "d8hdisttostrm"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src.tif"));commands.append("-dist")
    commands.append(os.path.join(In_Out_dir,output_distancefile));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command



def REACH_LINK(DEM_Raster,Watershed_Raster,treefile,coordfile,output_reachfile,output_nodefile,output_rchpropertiesfile):
    head,tail=os.path.split(str(DEM_Raster))
    In_Out_dir=str(head)
    base_name=os.path.basename(DEM_Raster)
    Input_Dem=os.path.splitext(base_name)[0]
    retDictionary=call_subprocess(PITREMOVE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'pitremove')
    if retDictionary['success'] == "False":
        return retDictionary
    retDictionary=call_subprocess(D8FLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'d8flow')
    if retDictionary['success'] == "False":
        return retDictionary
    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(1))

    commands.append(os.path.join(Exe_dir,"ReachLink"))
    commands.append("-me");commands.append(Watershed_Raster)
    commands.append("-p");commands.append(os.path.join(In_Out_dir,Input_Dem+'p.tif'))
    commands.append("-tree");commands.append(treefile)
    commands.append("-coord");commands.append(coordfile)
    commands.append("-rchlink");commands.append(os.path.join(In_Out_dir, output_reachfile))
    commands.append("-nodelink");commands.append(os.path.join(In_Out_dir, output_nodefile))
    commands.append("-nc");commands.append(os.path.join(In_Out_dir, Input_Dem+"nc.tif"))
    commands.append("-dc");commands.append(os.path.join(In_Out_dir, Input_Dem+"dc.tif"))
    commands.append("-rca");commands.append(os.path.join(In_Out_dir, "rchareas.txt"))
    commands.append("-rcp");commands.append(os.path.join(In_Out_dir, output_rchpropertiesfile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    #return fused_command
    os.system(fused_command)
    return {'success': 'True', 'message': 'download daymetdata successful'}

def DISTANCE_DISTRIBUTION(Watershed_Raster,SaR_Raster,Dist_Raster,output_distributionfile):
    head,tail=os.path.split(str(Watershed_Raster))
    In_Out_dir=str(head)


    commands=[]
    #commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(1))

    commands.append(os.path.join(Exe_dir,"DistWetness"))
    commands.append("-me");commands.append(Watershed_Raster)
    commands.append("-twi");commands.append(SaR_Raster)
    commands.append("-dis");commands.append(Dist_Raster)
    commands.append("-dists");commands.append(os.path.join(In_Out_dir, output_distributionfile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    return {'success': 'True', 'message': 'download daymetdata successful'}

# """download soil data """

def download_Soil_Data(Soil_Raster,output_f_file,output_k_file,output_dth1_file,output_dth2_file,output_psif_file,output_sd_file,output_Tran_file):
    head,tail=os.path.split(str(Soil_Raster))
    wateshed_Dir=str(head)
    watershed_raster_name=str(tail)

    Soil_script = os.path.join(R_Code_Path,'Extract_Soil_Data.r')

    commands=[]
    commands.append("Rscript");commands.append(Soil_script);commands.append(str(wateshed_Dir))
    commands.append(str(watershed_raster_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    return {'success': 'True', 'message': 'download daymetdata successful'}

def daymet_download(Watershed_Raster,Start_Year,End_Year,output_rainfile,output_temperaturefile,output_cliparfile):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    daymet_download_script= os.path.join(R_Code_Path,'daymet_download.r')
    commands=[]
    commands.append("Rscript");commands.append(daymet_download_script);commands.append(str(watershed_dir))
    commands.append(str(wateshed_name));commands.append(str(Start_Year));commands.append(str(End_Year))
    fused_command1 = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command1)
    raindat_script= os.path.join(R_Code_Path,'create_rain.R')
    commands=[]
    commands.append("Rscript");commands.append(raindat_script)
    commands.append(str(watershed_dir));commands.append(str(Start_Year));commands.append(str(End_Year));
    commands.append(str(output_rainfile))
    fused_command2 = ''.join(['"%s" ' % c for c in commands])

    os.system(fused_command2)

    tmaxtmin_script= os.path.join(R_Code_Path,'create_tmaxtmintdew.r')
    commands=[]
    commands.append("Rscript");commands.append(tmaxtmin_script)
    commands.append(str(watershed_dir));commands.append(str(Start_Year));commands.append(str(End_Year))
    commands.append(str(output_temperaturefile))
    fused_command3 = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command3)

    clipar_script= os.path.join(R_Code_Path,'create_clipar.R')
    commands=[]
    commands.append("Rscript");commands.append(clipar_script)
    commands.append(str(watershed_dir));commands.append(str(Start_Year));commands.append(str(End_Year))
    commands.append(str(wateshed_name));commands.append(str(output_cliparfile));
    fused_command4 = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command4)
    return {'success': 'True', 'message': 'download daymetdata successful'}



def getLULCdata(Watershed_Raster,output_LULCRaster):
    nlcd_Raster=(os.path.join(Base_Data_dir,'nlcd2011CONUS.tif'))
    subset_raster_to_referenceRaster(nlcd_Raster, output_LULCRaster,Watershed_Raster)
    return {'success': 'True', 'message': 'download LULC data  successful'}
## under consideration

def Create_Parspcfile(Watershed_Raster,output_parspcfile):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    watershed_base=os.path.basename(Watershed_Raster)
    wateshed_name=os.path.splitext(str(watershed_base))[0]
    parspc_script= os.path.join(R_Code_Path,'create_parspc_file.R')
    commands=[]
    commands.append("Rscript");commands.append(parspc_script)
    commands.append(str(watershed_dir));commands.append(str(wateshed_name));commands.append(str(output_parspcfile));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    return {'success': 'True', 'message': 'download LULC data  successful'}

def create_latlonfromxy(Watershed_Raster,output_lalonfromxyfile):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    latlonxy_script= os.path.join(R_Code_Path,'latlon_from_xy.R')
    commands=[]
    commands.append("Rscript");commands.append(latlonxy_script)
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    commands.append(str(output_lalonfromxyfile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    return {'success': 'True', 'message': 'download LULC data  successful'}


def BASIN_PARAM(DEM_Raster,Watershed_Raster,f_raster,k_raster,dth1_raster,dth2_raster,sd_raster,tran_taster,lulc_raster,
                lutlc,lutkc,parameter_specficationfile,nodelinksfile,output_basinfile):

    head,tail=os.path.split(str(DEM_Raster))
    In_Out_dir=str(head)
    base_name=os.path.basename(DEM_Raster)
    Input_Dem=os.path.splitext(base_name)[0]
    retDictionary=call_subprocess(PITREMOVE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem),'pitremove')
    if retDictionary['success'] == "False":
        return retDictionary
    head,tail=os.path.split(str(Watershed_Raster))
    #head_ps,tail_ps=os.path.split(str(parameterfile))
    Dem_dir=str(head)

    #Dem_base=os.path.basename(Watershed_Raster)
    #Dem_name=os.path.splitext(str(Dem_base))[0]
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(1))
    commands.append(os.path.join(Exe_dir,"BasinParammeter"))
    commands.append("-me");commands.append(Watershed_Raster)
    commands.append("-parspec");commands.append(os.path.join(Dem_dir,parameter_specficationfile))
    commands.append("-node");commands.append(os.path.join(Dem_dir,nodelinksfile))
    commands.append("-mpar");commands.append(os.path.join(Dem_dir,output_basinfile))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    #os.chdir(Dem_dir)
    os.system(fused_command)

    return {'success': 'True', 'message': 'download LULC data  successful'}



def Create_rain_weight(Watershed_Raster,Rain_gauge_shapefile,output_rainweightfile):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    head_rg,tail_rg=os.path.split(str(Rain_gauge_shapefile))
    Rain_GaugeDir=str(head_rg)

    prism_script= os.path.join(R_Code_Path,'annrain_prism.r')
    commands=[]
    commands.append("Rscript");commands.append(prism_script)
    commands.append(str(Base_Data_dir))
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    commands=[]
    commands.append(os.path.join(Exe_dir,"RainWeight"))
    commands.append("-w");commands.append(os.path.join(watershed_dir, wateshed_name))
    commands.append("-rg");commands.append(os.path.join(Rain_GaugeDir, "Rain_Gauge.shp"))
    commands.append("-ar");commands.append(os.path.join(watershed_dir, "annrain.tif"))
    commands.append("-tri");commands.append(os.path.join(watershed_dir, "triout.tif"))
    commands.append("-wt");commands.append(os.path.join(watershed_dir, "weights.txt"))
    fused_command1 = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command1)

    format_rainweight_script= os.path.join(R_Code_Path,'format_rainweight.R')
    commands=[]
    commands.append("Rscript");commands.append(format_rainweight_script)
    commands.append(str(watershed_dir));commands.append(str(output_rainweightfile))
    fused_command2 = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command2)
    return {'success': 'True', 'message': 'Creating rainweight file successful'}


def download_streamflow(USGS_gage, Start_Year, End_Year, output_streamflow):
    start=str(Start_Year)+"-01-01"
    end=str(End_Year)+"-12-31"
    Output_Dir = os.path.dirname(output_streamflow)
    #R_EXE_Path='/usr/bin/'
    #R_Code_Path = '/home/ahmet/ciwater/usu_data_service/topnet_data_service/TOPNET_Function/RCODE'
    streamflow_script= os.path.join(R_Code_Path,'get_USGS_streamflow.r')
    commands=[]
    commands.append("Rscript")
    commands.append(streamflow_script)
    #commands.append(os.path.join(R_EXE_Path, "Rscript"));commands.append(streamflow_script)
    commands.append(str(USGS_gage));commands.append(str(start));commands.append(str(end))
    commands.append(str(Output_Dir)); commands.append(str(output_streamflow))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)
    return {'success': 'True', 'message': 'download streamflow successful'}

def Raster_to_Polygon(input_file,output_file):
    gdal.UseExceptions()
    src_ds = gdal.Open(input_file)
    if src_ds is None:
        #print 'Unable to open %s' % src_filename
        sys.exit(1)
    try:
        srcband = src_ds.GetRasterBand(1)
        srd=srcband.GetMaskBand()
    except RuntimeError as e:
        # for example, try GetRasterBand(10)
        #print 'Band ( %i ) not found' % band_num
        #print e
        sys.exit(1)
    dst_layername = output_file
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )
    gdal.Polygonize( srcband,srd, dst_layer, -1, [], callback=None )



def findGDALCoordinates(path):
    if not os.path.isfile(path):
       return []
    data = gdal.Open(path,0)
    if data is None:
       return []
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1]*data.RasterXSize
    miny = maxy + geoTransform[5]*data.RasterYSize
    return [minx,miny,maxx,maxy]
















