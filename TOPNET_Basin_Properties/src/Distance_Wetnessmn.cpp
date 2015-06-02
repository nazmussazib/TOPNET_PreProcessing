/*  DinfDistUpmn main program to compute distance to ridge in DEM 
    based on D-infinity flow direction model.
     
  David Tarboton, Teklu K Tesfa
  Utah State University  
  May 23, 2010 
  
*/

/*  Copyright (C) 2010  David Tarboton, Utah State University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
version 2, 1991 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the full GNU General Public License is included in file 
gpl.html. This is also available at:
http://www.gnu.org/copyleft/gpl.html
or from:
The Free Software Foundation, Inc., 59 Temple Place - Suite 330, 
Boston, MA  02111-1307, USA.

If you wish to use or incorporate this program (or parts of it) into 
other software that does not meet the GNU General Public License 
conditions contact the author to request permission.
David G. Tarboton  
Utah State University 
8200 Old Main Hill 
Logan, UT 84322-8200 
USA 
http://www.engineering.usu.edu/dtarb/ 
email:  dtarb@usu.edu 
*/

//  This software is distributed from http://hydrology.usu.edu/taudem/

#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "commonLib.h"
#include "shape/shapefile.h"
//#include "tardemlib.h"

int twidistsetup(char *mefile, char *twifile, char *disfile,  char *distsfile);//function defined //

//========================

int main(int argc,char **argv) 

{
char mefile[MAXLN],twifile[MAXLN],disfile[MAXLN],distsfile[MAXLN]; //initializing of the inputs file//
   int err,i;
      
   if(argc < 2)
    {  
	   printf("Error: To run this program, use either the Simple Usage option or\n");
	   printf("the Usage with Specific file names option\n");
	   goto errexit;
    }
    else if(argc > 2)
	{
		i = 1;
//		printf("You are running %s with the Specific File Names Usage option.\n", argv[0]);
	}
	else {
		i = 2;
//		printf("You are running %s with the Simple Usage option.\n", argv[0]);
	}
	while(argc > i)
	{
		if(strcmp(argv[i],"-me")==0) //string comparison for model element file name//
		{
			i++;
			if(argc > i)
			{
				strcpy(mefile,argv[i]);//copy model element file name//
				i++;
			}
			else goto errexit;
		}
		else if(strcmp(argv[i],"-twi")==0) //string comparison for atanb file name//
		{
			i++;
			if(argc > i)
			{
				strcpy(twifile,argv[i]);//copy atanb file name//
				i++;
			}
			else goto errexit;
		}
		else if(strcmp(argv[i],"-dis")==0) //string comparison for dis file name//
		{
			i++;
			if(argc > i)
			{
				strcpy( disfile,argv[i]); //copy dis file name//
				i++;
			}
			else goto errexit;
		}
		
		else if(strcmp(argv[i],"-dists")==0) //string comparison for modelspc file name//
		{
			i++;
			if(argc > i)
			{
				strcpy(distsfile,argv[i]);//copy modelspc file name//
				i++;
			}
			else goto errexit;
		}
		
		else 
		{
			goto errexit;
		}
	}
 
if((err=twidistsetup(mefile,twifile,disfile,distsfile)) != 0) // calling atanbdisdistribution function for running the program//
        printf("rainweight error %d\n",err);   

	return 0;

	errexit:
	   printf("Incorrect input\n",argv[0]); //exit if the inputs are incorrect//
       exit(0);
} 
