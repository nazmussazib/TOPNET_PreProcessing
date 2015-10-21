__author__ = 'shams'

import shapefile
import numpy as np
from numpy import zeros
from numpy import logical_and
import pandas as pd
import  os
import time
from osgeo import ogr,osr,gdal
import rasterio.features
import numpy as np
from affine import Affine
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import fiona
import itertools
from osgeo import gdal
import sys
from rasterstats import zonal_stats
start_time = time.time()


def Raster_to_Polygon(input_file):

   gdal.UseExceptions()
   src_ds = gdal.Open(input_file)
   print(input_file)
   #target = osr.SpatialReference()
   wkt =src_ds.GetProjection()
   print(wkt)
   src =osr.SpatialReference()
   print(src)
   ds=src.ImportFromWkt(wkt)
   #srcband = src_ds.GetRasterBand(1)
   myarray =(src_ds.GetRasterBand(1).ReadAsArray())
   #print(myarray)
   T0 = Affine.from_gdal(*src_ds.GetGeoTransform())
   tx=[T0[0], T0[1], T0[2], T0[3],T0[4], T0[5]]
   epsg_code=[]
   #if (src.IsProjected()):
      #  ds=epsg_code.append(int(src.GetAuthorityCode("PROJCS")))
       # print(ds)

  # else:
     #  epsg_code.append(int(src.GetAuthorityCode("GEOGCS")))
   target = osr.SpatialReference()
   target.ImportFromEPSG(102003)
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



   drv = ogr.GetDriverByName("ESRI Shapefile")
   if os.path.exists('temp.shp'):
     drv.DeleteDataSource('temp.shp')

   dst_layername ='temp'
   dst_ds = drv.CreateDataSource('temp'+ ".shp" )

   dst_layer = dst_ds.CreateLayer(dst_layername, srs=target)
   gdal.Polygonize( srcband,srd, dst_layer, -1, [], callback=None)
   src_ds=None


def reclassify_and_stats_raster(input_raster,lookup_table_in,lookup_table_out,watershed_shapefile):
    input_raster= input_raster
    ds = gdal.Open(input_raster)
    band = ds.GetRasterBand(1)
    classification_values =lookup_table_in
    classification_output_values = lookup_table_out
#

    block_sizes = band.GetBlockSize()
    x_block_size = block_sizes[0]
    y_block_size = block_sizes[1]

    xsize = band.XSize
    ysize = band.YSize

    max_value = band.GetMaximum()
    min_value = band.GetMinimum()

    if max_value == None or min_value == None:
      stats = band.GetStatistics(0, 1)
      max_value = stats[1]
      min_value = stats[0]

    format = "GTiff"
    driver = gdal.GetDriverByName( format )
    dst_ds = driver.Create("tempraster.tif", xsize, ysize, 1, gdal.GDT_Float64 )
    dst_ds.SetGeoTransform(ds.GetGeoTransform())
    dst_ds.SetProjection(ds.GetProjection())

    for i in range(0, ysize, y_block_size):
      if i + y_block_size < ysize:
        rows = y_block_size
      else:
          rows = ysize - i
      for j in range(0, xsize, x_block_size):
        if j + x_block_size < xsize:
            cols = x_block_size
        else:
            cols = xsize - j

        data = band.ReadAsArray(j, i, cols, rows)
        r = zeros((rows, cols), np.uint8)

        for k in range(len(classification_values) - 1):
            if classification_values[k] <= max_value and (classification_values[k + 1] > min_value ):
                r = r + classification_output_values[k] * logical_and(data >= classification_values[k], data < classification_values[k + 1])
        if classification_values[k + 1] < max_value:
            r = r + classification_output_values[k+1] * (data >= classification_values[k + 1])

        dst_ds.GetRasterBand(1).WriteArray(r,j,i)

    dst_ds = None
    stats2 = zonal_stats(watershed_shapefile, "tempraster.tif",stats=['mean'])
    mean_val=([d['mean'] for d in stats2])
    result = pd.DataFrame(mean_val)
    return(result)


def dissolve_polygon(input_raster,output_file):
    #os.chdir(dir)
    ds = gdal.Open(input_raster)
   # print(ds)
   #print(input_raster)
    if os.path.exists(output_file):
      drv.DeleteDataSource(output_file)
    grid_code=[]

    band =  ds.GetRasterBand(1)

    myarray =(ds.GetRasterBand(1).ReadAsArray())
    #print(myarray)
    T0 = Affine.from_gdal(*ds.GetGeoTransform())
    tx=[T0[0], T0[1], T0[2], T0[3],T0[4], T0[5]]
    drv = ogr.GetDriverByName("ESRI Shapefile")

    for shp, val in rasterio.features.shapes(myarray,transform=tx):
    # print('%s: %s' % (val, shape(shp)))
     if(val>=0):
       grid_code.append(float(val))
    #add_filed_existing_shapefile('temp1.shp',np.asarray(grid_code))
    pj=[]
    with fiona.open('temp.shp') as input:
     meta = input.meta
    with fiona.open('temp.shp', 'r') as source:

    # Copy the source schema and add two new properties.
      sink_schema = source.schema.copy()
      sink_schema['properties']['ID'] = 'float'


    # Create a sink for processed features with the same format and
    # coordinate reference system as the source.
      with fiona.open(
            'temp2.shp', 'w',
            crs=source.crs,
            driver=source.driver,
            schema=sink_schema,
            ) as sink:
        i=0
        for f in source:
                #print(f)


                # Add the signed area of the polygon and a timestamp
                # to the feature properties map.
                f['properties'].update(
                    ID=grid_code[i],
                   )
                i+=1
                sink.write(f)



      pj=[]
      with fiona.open('temp2.shp') as input:
       meta = input.meta
       print('srt')
       with fiona.open('final.shp', 'w',**meta) as output:
        # groupby clusters consecutive elements of an iterable which have the same key so you must first sort the features by the 'STATEFP' field
         e = sorted(input, key=lambda k: k['properties']['ID'])
         #print(e)
         # group by the 'STATEFP' field
         for key, group in itertools.groupby(e, key=lambda x:x['properties']['ID']):
            properties, geom = zip(*[(feature['properties'],shape(feature['geometry'])) for feature in group])
            # write the feature, computing the unary_union of the elements in the group with the properties of the first element in the group
            output.write({'geometry': mapping(unary_union(geom)), 'properties': properties[0]})
def create_basin_param(watershed_shapefile,lancover_raster,lutluc,lutkc,paramfile,nodelinkfile,output_basinfile):
  import numpy as np
  input_datalist=pd.read_csv(paramfile,header=None,error_bad_lines=False)
  print(input_datalist)
  data_length=len(input_datalist.index)
  print(data_length)
  #print input_datalist[0][1]
  lulc_table=pd.read_csv(lutluc,delim_whitespace=True,header=None,skiprows=1)
  lukc_table=pd.read_csv(lutkc,delim_whitespace=True,header=None,skiprows=1)
  lulc_base=np.asarray(lulc_table[0].tolist())
  lukc_base=np.asarray(lukc_table[0].tolist())
  #print lulc_table[1]
  watershed_shapefile=watershed_shapefile
  head,tail=os.path.split(str(lancover_raster))
 # print(tail)
  from osgeo import gdal
  import numpy as np
  ds = gdal.Open(str(tail))
  band =  ds.GetRasterBand(1)
  myarray = (band.ReadAsArray())
  unique_values = np.unique(myarray)

  features = fiona.open(watershed_shapefile)
  grid_code=[]
  for feat in features:
     grid_code.append(feat['properties']['ID'])
  basin_num=len(grid_code)
  #this function need for calculating land use land cover with look up table


  #nodfile_data=pd.read_csv(nodelinkfile,header=None)
  df = pd.DataFrame(grid_code,columns=[str('DrainId')])
  for i in range(0,data_length):
    soil_pro_file=input_datalist[1][i]
    print(soil_pro_file)
    if(soil_pro_file==0):
        print (input_datalist[2][i])
        stats = zonal_stats(watershed_shapefile, str(input_datalist[2][i]),stats=['mean'])
        mean_val=([d['mean'] for d in stats])
        df1 = pd.DataFrame(mean_val)
        df[str(input_datalist[0][i])]=df1
    elif(soil_pro_file==2):
         col_ind=int(input_datalist[4][i])
         cl_val=np.asarray(lulc_table[col_ind].tolist())
         df2=pd.DataFrame(reclassify_and_stats_raster(str(input_datalist[2][i]),lulc_base,cl_val,watershed_shapefile))

         df[str(input_datalist[0][i])]=df2
    elif(soil_pro_file==1):
         col_ind=int(input_datalist[4][i])
         cl_val=np.asarray(lukc_table[col_ind].tolist())
         df3=pd.DataFrame(reclassify_and_stats_raster(str(input_datalist[2][i]),lukc_base,cl_val,watershed_shapefile))
         df[str(input_datalist[0][i])]=df3

    else:
        val=[input_datalist[2][i]]*basin_num
        df4 = pd.DataFrame(val,dtype=np.float32)
        df[str(input_datalist[0][i])]=df4

  #print(df)
  nodfile_data=pd.read_csv(nodelinkfile, dtype= {'NodeId':np.int,'DownNodeId':np.int,'DrainId':np.int,'ProjNodeId':np.int,'DOutFlag':np.int,'ReachId':np.int,'Area':np.float64,'AreaTotal':np.float64,'X':np.float64,'Y':np.float64})
  nd_df = pd.DataFrame(nodfile_data)
  nd_df.columns = ['NodeId', 'DownNodeId' , 'DrainId' , 'ProjNodeId',  'DOutFlag', 'ReachId','Area','AreaTotal', 'X','Y']
  nd_df['Area']=nd_df['Area']*1000000
  #print (nd_df)
 # CatchID,DownCatchID,DrainID,NodeId,Reach_number,Outlet_X,Outlet_Y,direct_area,

  df.columns = ['DrainId', 'f', 'ko','dth1','dth2','soildepth','c','psif','chv','cc','cr','albedo','LapseRate','AverageElevation','ImperviousFraction','TileDrainedFraction','DitchDrainedFraction',
               'TileCoeff','DitchCoef','IrrigatedFraction','SprinklerFractionofIrrigation','IrrigationEfficiency','D_Thres','Z_Max','D_Goal',
                'kc_1','kc_2','kc_3','kc_4','kc_5','kc_6','kc_7','kc_8','kc_9','kc_10','kc_11','kc_12','Transmissivity','FractionForest']
  nd_df.columns = ['NodeId', 'DownNodeId' , 'DrainId' , 'ProjNodeId',  'DOutFlag', 'ReachId','Area','AreaTotal', 'X','Y']
  print(df)
  result = pd.merge(df,nd_df,
         left_on=['DrainId'],
         right_on=['DrainId'],
         how='inner')
  result.sort_index(by=['NodeId'], ascending=[True],inplace=True)
  dd=result.ix[:,1:(data_length+1)]
  #print(dd)
  node_df=nd_df[['NodeId', 'DownNodeId','DrainId','ProjNodeId','X','Y' ,'ReachId','Area']]
  result2 = pd.concat([node_df,dd], axis=1)
  #result2['Area']=result2['Area']*float(1000000)
  result2.to_csv(output_basinfile, header=True, index=None, sep=',', mode='w')





##example:
os.chdir('E:\USU_Research_work\TOPNET_Web_Processing\LittleBearRiverDemo')
# ds = gdal.Open(str('LittleBear30WS.tif'))
# band =  ds.GetRasterBand(1)
# myarray = (band.ReadAsArray())
# unique_values = np.unique(myarray)
# basin_val=unique_values[unique_values>-1]
# lulc_table=pd.read_csv('lutluc.txt',delim_whitespace=True,header=None,skiprows=1)
# print(lulc_table[1])
# ad=np.asarray(lulc_table[3].tolist())
# bc=np.asarray(lulc_table[0].tolist())
# print(ad)
# ds=reclassify_and_stats_raster('lulcmmef.tif',bc,ad,'final.shp')
# print(ds)
Raster_to_Polygon('LittleBear30WS.tif')
dissolve_polygon('LittleBear30WS.tif','final.shp')
create_basin_param('final.shp','lulcmmef.tif','lutluc.txt','lutkc.txt','LittleBearparam.txt','nodelinks.txt','basin2.txt')
