#  Makefile for building executables on a UNIX System.
#
#    David Tarboton, Dan Watson, Jeremy Neff
#    Utah State University
#    May 23, 2010
#
#  Copyright (C) 2010  David Tarboton, Utah State University
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License 
#  version 2, 1991 as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  A copy of the full GNU General Public License is included in file 
#  gpl.html. This is also available at:
#  http://www.gnu.org/copyleft/gpl.html
#  or from:
#  The Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
#  Boston, MA  02111-1307, USA.
#
#  If you wish to use or incorporate this program (or parts of it) into 
#  other software that does not meet the GNU General Public License 
#  conditions contact the author to request permission.
#  David G. Tarboton  
#  Utah State University 
#  8200 Old Main Hill 
#  Logan, UT 84322-8200 
#  USA 
#  http://www.engineering.usu.edu/dtarb/ 
#  email:  dtarb@usu.edu 
#
#
#  This software is distributed from http://hydrology.usu.edu/taudem/



#SHAPEFILES includes all files in the shapefile library
#These should be compiled using the makefile in the shape directory
SHAPEFILES = shape/cell.o shape/dbf.o shape/exception.o shape/field.o shape/item.o \
             shape/point.o shape/record.o shape/shape.o shape/shapefile.o \
             shape/shapemain.o shape/shp_point.o shape/shp_polygon.o shape/shp_polyline.o \
	     shape/ReadOutlets.o

#OBJFILES includes classes, structures, and constants common to all files
OBJFILES = commonLib.o tiffIO.o

BAPARM = Basin_parammn.o Basin_param.o $(OBJFILES) $(SHAPEFILES)
DISWET = Distance_Wetnessmn.o Distance_Wetness.o $(OBJFILES) 
RAINWEIGHT= RainWeightmn.o triangle.o rainweight.o $(OBJFILES) $(SHAPEFILES)
REACHLINK = Reach_Linkmn.o Reach_Link.o  $(OBJFILES) $(SHAPEFILES)

#The following are compiler flags common to all building rules
CC =mpic++
CFLAGS +=-O2

DEBUG = -g
CFLAGS  = -std=c++0x $(DEBUG)

LARGEFILEFLAG= -D_FILE_OFFSET_BITS=64
LDLIBS = -L"/home/A01769693/gdal/lib" -lgdal




#Rules: when and how to make a file
all : ../BasinParam ../DistWetness ../RainWeight ../ReachLink 
../BasinParam : $(BAPARM)
	$(CC) $(CFLAGS) -o $@ $(LIBDIRS) $(BAPARM) $(LDLIBS) $(LDFLAGS)

../DistWetness : $(DISWET)
	$(CC) $(CFLAGS) -o $@ $(LIBDIRS) $(DISWET) $(LDLIBS) $(LDFLAGS)

../RainWeight : $(RAINWEIGHT)
	$(CC) $(CFLAGS) -o $@ $(LIBDIRS) $(RAINWEIGHT) $(LDLIBS) $(LDFLAGS)

../ReachLink : $(REACHLINK)
	$(CC) $(CFLAGS) -o $@ $(LIBDIRS) $(REACHLINK) $(LDLIBS) $(LDFLAGS)
	
#Inference rule - states a general rule for compiling .o files
%.o : %.cpp
	$(CC) $(CFLAGS) $(INCDIRS) -c $<

clean :
	rm *.o 

