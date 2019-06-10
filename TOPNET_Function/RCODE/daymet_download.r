args<-commandArgs(TRUE)
# args<-c(watershed_dir, watershed_name, startdate, enddate, output_gagefile)
# args<-c("/home/ahmet/ciwater/usu_data_service/workspace/5940e8bc470c4539a7987f9bddf4f305",
# "Logantopnet300WS.tif" ,
# "2010",
# "2010",
# "/home/ahmet/ciwater/usu_data_service/workspace/5940e8bc470c4539a7987f9bddf4f305/Climate_Gage.shp")

print ('Progresss --> The daymet_download function started')

#suppressMessages(require(downloader))
dyn.load('/usr/local/lib/libgeos_c.so', local=FALSE)

suppressMessages(require(rgeos))
suppressMessages(require(proj4))
suppressMessages(require(rgdal))
suppressMessages(require(raster))
suppressMessages(require(shapefiles))
#suppressMessages(require(deldir))
suppressMessages(require(spsurvey))
#suppressMessages(require(Day))
suppressMessages(require(daymetr))
suppressMessages(require(tools))
require(maptools)
#print ('The arguments................')
print (args)
#setwd('E:\\USU_Research_work\\TOPNET_Web_Processing\\TOPNET_Web_services\\Test_Results\\DelineatedWatershed')
setwd(args[1])
#dr=args[1]
newproj="+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs +ellps=GRS80 +towgs84=0,0,0"
#rs=raster('demc1w.tif')
rs=raster(args[2])
print("Progress --> Packages requred for daymet_download.R loaded")

z=projectRaster(rs,crs=newproj,res=4*1000)
print(args[1])

top=rasterToPoints(z)
#print("essspsruvey")

lat_lon_rg1=albersgeod(top[,1], top[,2], sph="GRS80", clon=-96, clat=23, sp1=29.5, sp2=45.5)
#print("nospsruvey")

shapefile=file_path_sans_ext(args[5])

df2=data.frame(X=lat_lon_rg1[,1],Y=lat_lon_rg1[,2],ID=as.integer(seq(1,length(top[,1]),1)))

#print (df2)

lots <- SpatialPointsDataFrame( coords = cbind(df2$X,df2$Y), data = df2,proj4string=CRS(as.character("+proj=longlat +datum=WGS84")))
#print ('lots is:')
lots
print(shapefile)
# writeOGR( lots, dsn = args[1] , layer=shapefile ,driver='ESRI Shapefile',overwrite=TRUE) # initially, layer  =shapefile
#dir.create("tempdir")
#setwd(args[1])
#print()
dt=as.character(getwd())
print(dt)
td <- file.path(tempdir(), "rgdal_examples"); dir.create(td)
#writeOGR(lots,dsn=td,layer=shapefile,driver='ESRI Shapefile')

print ('Written to OGR')
len=(nrow(lat_lon_rg1))
fl_nm=matrix(NA,len,1)
for(i in 1:len){
  fl_nm[i]=paste("filename",i,sep="")
  print(i)
}


MyData=cbind(fl_nm,lat_lon_rg1[,2],lat_lon_rg1[,1])
write.table(MyData, file = "MyData.csv", sep=",", row.names=FALSE, col.names=TRUE)

for(i in 1:len){
  cat("filename",i, file="latlon.csv", sep="",append=TRUE)
  cat(",", file="latlon.csv", append=TRUE)
  cat(lat_lon_rg1[i,2],lat_lon_rg1[i,1],file="latlon.csv", sep=",",append=TRUE)
  cat(",", "\n",file="latlon.csv", append=TRUE)
  #cat("ignore stuff",i, file="latlon.txt", sep=",",append=TRUE)
  #cat("\n", file="latlon.csv", append=TRUE)
}

#close(file="latlon.csv")
#download.daymet(site="Oak",lat=36.0133,lon=-84.2625,start_yr=1980,end_yr=2010,internal=TRUE)
download_daymet_batch(file_location='MyData.csv',start=as.numeric(args[3]),end=as.numeric(args[4]),internal=FALSE,path=args[1])
