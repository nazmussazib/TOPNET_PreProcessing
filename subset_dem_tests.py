__author__ = 'Pabitra'

""" This is an example usage of the 'subset_raster' HydroDS client api """

from hydrogate import HydroDS
import settings

# Create HydroDS object passing user login account for HydroDS api server
hds = HydroDS(username=settings.USER_NAME, password=settings.PASSWORD)

try:
    # param: output_raster is optional
    # param: save_as: is optional (use this to download the output file to the specified directory)
    response_data = hds.subset_raster(left=-111.97, top=42.11, right=-111.35, bottom=41.66,
                                      input_raster='nedWesternUS.tif', output_raster='subset_dem_logan_3.tif',
                                      save_as=r'E:\Scratch\HydroGateClientDemo\nedLogan_2C.tif')

    output_subset_dem_url = response_data['output_raster']

    # print the url path for the generated raster file
    print(output_subset_dem_url)
except Exception as ex:
    print(ex.message)

print ">>>> DONE ..."