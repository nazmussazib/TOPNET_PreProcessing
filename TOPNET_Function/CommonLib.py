
import os
import subprocess
import gdal,ogr
import sys

def watershed_delineation(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Outlet,Src_threshold,Min_threshold,Max_threshold,Number_threshold):
    os.system(PITREMOVE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(D8FLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(D8CONTRIBUTING_AREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(THRESHOLD(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Src_threshold))
    os.system(MOVEOUTLETTOSTREAMS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Outlet))
    os.system(PEUKERDOUGLAS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(ACCUMULATING_STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(DROP_ANALYSIS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Min_threshold,Max_threshold,Number_threshold))
    fileHandle = open (os.path.join(In_Out_dir,Input_Dem+"drp.txt"),"r")
    lineList = fileHandle.readlines()
    fileHandle.close()
    LL= lineList[-1]
    thres=LL[25:35]
    if(thres>0):
        thres=thres
    else:
        thres=float(Max_threshold)

    os.system(STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,thres))
    os.system(StreamNet(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(WETNESS_INDEX(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))
    os.system(DISTANCE_DOWNSTREAM(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem))


def PITREMOVE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-n");commands.append(str(np));commands.append("--allow-run-as-root")
    commands.append(os.path.join(TauDEM_dir, "pitremove"));commands.append("-z")
    commands.append(os.path.join(In_Out_dir,Input_Dem+".tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def D8FLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "d8flowdir"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-sd8")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"sd8.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def D8CONTRIBUTING_AREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "aread8"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DINFFLOWDIRECTIONS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "dinfflowdir"));commands.append("-ang")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ang.tif"));commands.append("-slp")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"slp.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"fel.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DINFCONTRIBUTINGAREA(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "areadinf"));commands.append("-ang")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ang.tif"));commands.append("-sca")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"sca.tif"));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command


def THRESHOLD(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Src_threshold):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "threshold"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"src.tif"));commands.append("-thresh");commands.append(str(Src_threshold))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def MOVEOUTLETTOSTREAMS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Outlet):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "moveoutletstostrm"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir, Input_Dem+"src.tif"));commands.append("-o");commands.append(os.path.join(In_Out_dir, Outlet+".shp"))
    commands.append("-om");commands.append(os.path.join(In_Out_dir, "outlets_moved.shp"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def PEUKERDOUGLAS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "peukerdouglas"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-ss")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ss.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command


def ACCUMULATING_STREAM_SOURCE(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "aread8"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-o")
    commands.append(os.path.join(In_Out_dir, "outlets_moved.shp"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-wg")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ss.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DROP_ANALYSIS(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem,Min_threshold,Max_threshold,Number_threshold):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "dropanalysis"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-drp")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"drp.txt"));commands.append("-o")
    commands.append(os.path.join(In_Out_dir, "outlets_moved.shp"));commands.append("-par")
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
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "threshold"));commands.append("-ssa")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ssa.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src2.tif"));commands.append("-thresh")
    commands.append(str(thershold))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command



def StreamNet(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "streamnet"));commands.append("-fel")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"fel.tif"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-ad8")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src2.tif"));commands.append("-ord")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ord2.tif"));commands.append("-tree")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"tree.txt"));commands.append("-coord")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"coord.txt"));commands.append("-net")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"net2.shp"));commands.append("-w")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"w.tif"));commands.append("-o")
    commands.append(os.path.join(In_Out_dir,"outlets_moved.shp"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def WETNESS_INDEX(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "slopearearatio"));commands.append("-slp")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"sd8.tif"));commands.append("-sca")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"ad8.tif"));commands.append("-sar")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"sar.tif"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command

def DISTANCE_DOWNSTREAM(MPI_dir,np,TauDEM_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpirun"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(TauDEM_dir, "d8hdisttostrm"));commands.append("-p")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"));commands.append("-src")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"src.tif"));commands.append("-dist")
    commands.append(os.path.join(In_Out_dir,Input_Dem+"dist.tif"));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    return fused_command



def REACH_LINK(MPI_dir,np,Exe_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpiexec"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(Exe_dir,"ReachLink"))
    commands.append("-me");commands.append(os.path.join(In_Out_dir,Input_Dem+"w.tif"))
    commands.append("-p");commands.append(os.path.join(In_Out_dir,Input_Dem+"p.tif"))
    commands.append("-tree");commands.append(os.path.join(In_Out_dir,Input_Dem+"tree.txt"))
    commands.append("-coord");commands.append(os.path.join(In_Out_dir,Input_Dem+"coord.txt"))
    commands.append("-rchlink");commands.append(os.path.join(In_Out_dir, "rchlink.txt"))
    commands.append("-nodelink");commands.append(os.path.join(In_Out_dir, "nodelinks.txt"))
    commands.append("-nc");commands.append(os.path.join(In_Out_dir, Input_Dem+"nc.tif"))
    commands.append("-dc");commands.append(os.path.join(In_Out_dir, Input_Dem+"dc.tif"))
    commands.append("-rca");commands.append(os.path.join(In_Out_dir, "rchareas.txt"))
    commands.append("-rcp");commands.append(os.path.join(In_Out_dir, "rchproperties.txt"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    #return fused_command
    os.system(fused_command)

def DISTANCE_DISTRIBUTION(MPI_dir,np,Exe_dir,In_Out_dir,Input_Dem):
    commands=[]
    commands.append(os.path.join(MPI_dir,"mpiexec"));commands.append("-np");commands.append(str(np));commands.append("--allow-run-as-root")

    commands.append(os.path.join(Exe_dir,"DistWetness"))
    commands.append("-me");commands.append(os.path.join(In_Out_dir,Input_Dem+"w.tif"))
    commands.append("-twi");commands.append(os.path.join(In_Out_dir, Input_Dem+"sar.tif"))
    commands.append("-dis");commands.append(os.path.join(In_Out_dir, Input_Dem+"dist.tif"))
    commands.append("-dists");commands.append(os.path.join(In_Out_dir, "distribution.txt"));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

# """download soil data """

def download_Soil_Data(Watershed_Raster,Western_Soil_Raster,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Raster))
    wateshed_Dir=str(head)
    watershed_raster_name=str(tail)
    os.chdir(wateshed_Dir)
    Raster_to_Polygon(watershed_raster_name,'Watershed_Shape')
    #watershedfile=os.path.join(wateshed_Dir,'Watershed_Shape.shp')

    extent=findGDALCoordinates(Watershed_Raster)
    Extract_by_Boundary='gdalwarp -te'+" "+str(extent[0]) + " "+ str(extent[1]) + " "+  str(extent[2])+ " "+  str(extent[3]) + " "+ Western_Soil_Raster+" " +'clipped_output.tif'
    os.system(Extract_by_Boundary)
    Extarct_Raster="gdalwarp -dstnodata -32768 -cutline " +" " +'Watershed_Shape.shp' +" " + 'clipped_output.tif' + " " + ' Soil_Raster_Watershed.tif'
    os.system(Extarct_Raster)

    Soil_script = os.path.join(R_Code_Path,'Extract_Soil_Data.r')
    os.chdir(R_EXE_Path)
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(Soil_script);commands.append(str(wateshed_Dir))
    commands.append(str('Soil_Raster_Watershed.tif'))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

def daymet_download(Watershed_Raster,Start_year,End_year,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    daymet_download_script= os.path.join(R_Code_Path,'daymet_download.r')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(daymet_download_script);commands.append(str(watershed_dir))
    commands.append(str(wateshed_name));commands.append(str(Start_year));commands.append(str(End_year));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

def getLULCdata(nlcd_CONUS,Watershed_Raster,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Raster))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    lulc_script= os.path.join(R_Code_Path,'lulc_data.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(lulc_script);commands.append(str(nlcd_CONUS))
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)


def Create_Parspcfile(Watershed_Name_Dir,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Name_Dir))
    watershed_dir=str(head)
    watershed_base=os.path.basename(Watershed_Name_Dir)
    wateshed_name=os.path.splitext(str(watershed_base))[0]
    parspc_script= os.path.join(R_Code_Path,'create_parspc_file.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(parspc_script)
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)




def BASIN_PARAM(Exe_dir,Input_Dem_Name_Dir):
    head,tail=os.path.split(str(Input_Dem_Name_Dir))
    Dem_dir=str(head)
    Dem_base=os.path.basename(Input_Dem_Name_Dir)
    Dem_name=os.path.splitext(str(Dem_base))[0]
    commands=[]
    commands.append(os.path.join(Exe_dir,"BasinParammeter"))
    commands.append("-me");commands.append(os.path.join(Dem_dir,Dem_name+"w.tif"))
    commands.append("-parspec");commands.append(os.path.join(Dem_dir,Dem_name+"parspc.txt"))
    commands.append("-node");commands.append(os.path.join(Dem_dir,"nodelinks.txt"))
    commands.append("-mpar");commands.append(os.path.join(Dem_dir, "basinpars.txt"));
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.chdir(Dem_dir)
    os.system(fused_command)


def create_latlonfromxy(Watershed_Name_Dir,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Name_Dir))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    latlonxy_script= os.path.join(R_Code_Path,'latlon_from_xy.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(latlonxy_script)
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)


def crop_PRISM_Rain(Watershed_Name_Dir,PRISM_Name_Dir,R_EXE_Path,R_Code_Path):
    head,tail=os.path.split(str(Watershed_Name_Dir))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    prism_script= os.path.join(R_Code_Path,'annrain_prism.r')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(prism_script)
    commands.append(str(PRISM_Name_Dir))
    commands.append(str(watershed_dir));commands.append(str(wateshed_name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)




def Create_rain_weight(Exe_Dir,Watershed_Name_Dir):
    head,tail=os.path.split(str(Watershed_Name_Dir))
    watershed_dir=str(head)
    wateshed_name=str(tail)
    Rain_GaugeDir=os.path.join(watershed_dir,"Rain_Gauge")
    commands=[]
    commands.append(os.path.join(Exe_Dir,"rainweight"))
    commands.append("-w");commands.append(os.path.join(watershed_dir, wateshed_name))
    commands.append("-rg");commands.append(os.path.join(Rain_GaugeDir, "Rain_Gauge.shp"))
    commands.append("-ar");commands.append(os.path.join(watershed_dir, "annrain.tif"))
    commands.append("-tri");commands.append(os.path.join(watershed_dir, "triout.tif"))
    commands.append("-wt");commands.append(os.path.join(watershed_dir, "weights.txt"))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)


def format_Rain_Weight(Weight_file_dir,R_EXE_Path,R_Code_Path):
    format_rainweight_script= os.path.join(R_Code_Path,'format_rainweight.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(format_rainweight_script)
    commands.append(str(Weight_file_dir))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)


def create_rain_dat(climate_file_dir,Start_year, End_year,R_EXE_Path,R_Code_Path):
    raindat_script= os.path.join(R_Code_Path,'create_rain.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(raindat_script)
    commands.append(str(climate_file_dir));commands.append(str(Start_year));commands.append(str(End_year))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

def create_tmaxtmin_dat(climate_file_dir,Start_year, End_year,R_EXE_Path,R_Code_Path):
    tmaxtmin_script= os.path.join(R_Code_Path,'create_tmaxtmintdew.r')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(tmaxtmin_script)
    commands.append(str(climate_file_dir));commands.append(str(Start_year));commands.append(str(End_year))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

def create_clipar_dat(climate_file_dir,Watershed_Raster_Name,Start_year, End_year,R_EXE_Path,R_Code_Path):
    clipar_script= os.path.join(R_Code_Path,'create_clipar.R')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(clipar_script)
    commands.append(str(climate_file_dir));commands.append(str(Start_year));commands.append(str(End_year))
    commands.append(str(Watershed_Raster_Name))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)


def download_streamflow(USGS_gage,Start_Year, End_Year,Output_Dir,R_EXE_Path,R_Code_Path):
    start=str(Start_Year)+"-01-01"
    end=str(End_Year)+"-12-31"
    streamflow_script= os.path.join(R_Code_Path,'get_USGS_streamflow.r')
    commands=[]
    commands.append(os.path.join(R_EXE_Path,"Rscript"));commands.append(streamflow_script)
    commands.append(str(USGS_gage));commands.append(str(start));commands.append(str(end))
    commands.append(str(Output_Dir))
    fused_command = ''.join(['"%s" ' % c for c in commands])
    os.system(fused_command)

def Raster_to_Polygon(input_file,output_file):
   gdal.UseExceptions()
   src_ds = gdal.Open(input_file)
   if src_ds is None:
     #print 'Unable to open %s' % src_filename
     sys.exit(1)
   try:
      srcband = src_ds.GetRasterBand(1)
      srd=srcband.GetMaskBand()
   except RuntimeError, e:
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




















