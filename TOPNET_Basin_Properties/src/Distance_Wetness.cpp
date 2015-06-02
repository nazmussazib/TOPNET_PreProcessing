	#include <iostream>     // std::cout
	#include <algorithm>    // std::unique_copy, std::sort, std::distance
	#include <vector>       // std::vector
	#include <mpi.h>
	#include <math.h>
	#include <queue>
	#include "commonLib.h"
	#include "linearpart.h"
	#include "createpart.h"
	#include "tiffIO.h"
	#include "shape/shapefile.h"
    using namespace std;
    int distribution(int n11,int bn, tdpartition *meData, tdpartition *twiData, tdpartition *disData, float mbinp,double inc, float mbind, double dinc,int rows,int columns,FILE *fp);//function prototype//

	/*; double *pp,inc, *atbout;float *atbls, *atbl;
	int n=0;int i1, nout,n0;*/

	bool myfunction (int i, int j) 
	{
	  return (i==j);
	}
	//atanbdisdistribution function

	int twidistsetup(char *mefile, char *twifile, char *disfile,  char *distsfile)
	{ 
		MPI_Init(NULL,NULL);
		{
		
		//Only used for timing
		int rank,size;
		MPI_Comm_rank(MCW,&rank);
		MPI_Comm_size(MCW,&size);
		if(rank==0)printf("distribution -h version %s\n",TDVERSION);

		/*float wt=1.0,angle,sump,distr,dtss;
		double p;*/

		//  Keep track of time
		double begint = MPI_Wtime();

		//Create tiff object, read and store header info for modelelement/delineated watershed tiff


		tiffIO megrid(mefile, LONG_TYPE);
		long totalX = megrid.getTotalX(); //give total number of rows
		long totalY = megrid.getTotalY(); //give total number of columns
		double dx = megrid.getdxA();   // give pixel size
		double dy = megrid.getdyA();   //pixel size

		//Create tiff object, read and store header info for atanb tiff

		tiffIO twigrid(twifile, FLOAT_TYPE);
	/*	long totalX1= atanbgrid.getTotalX();
		long totalY1 = atanbgrid.getTotalY();
		double dx1 = atanbgrid.getdx();
		double dy1 = atanbgrid.getdy();*/
		if(!megrid.compareTiff(twigrid)) 
		{  //  Here the grid dimensions of atanb do not match
			printf("Mismatch of grid dimensions\n");
			printf("Atanb file: %s\n",twifile);
			printf("Me file: %s\n",mefile);	
			return 1;  //And maybe an unhappy error message
		}

		//Create tiff object, read and store header info for dist tiff

		tiffIO disgrid(disfile, FLOAT_TYPE);
		/*long totalX2= disgrid.getTotalX();
		long totalY2 = disgrid.getTotalY();
		double dx2 = disgrid.getdx();
		double dy2 = disgrid.getdy();*/
		if(!megrid.compareTiff(disgrid)) 
		{  //  Here the grid dimensions of disfile do not match
			printf("Mismatch of grid dimensions\n");
			printf("dis file: %s\n",disfile);
			printf("Me file: %s\n",mefile);	
			return 1;  //And maybe an unhappy error message
		}

		
		//Create partition and read watershed tiff data

		tdpartition *meData;
		meData = CreateNewPartition(megrid.getDatatype(), totalX, totalY, dx, dy, megrid.getNodata());
		int nx = meData->getnx();
		int ny = meData->getny();
		int xstart, ystart;
		meData->localToGlobal(0, 0, xstart, ystart);
		megrid.read(xstart, ystart, ny, nx, meData->getGridPointer());
		 

		//Create partition and read atanb tiff data

		tdpartition *twiData;
		twiData = CreateNewPartition(twigrid.getDatatype(), totalX, totalY, dx, dy, twigrid.getNodata());
		/*int nx1 = atanbData->getnx();
		int ny1 = atanbData->getny();*/
		twiData->localToGlobal(0, 0, xstart, ystart);
		twigrid.read(xstart, ystart, ny, nx, twiData->getGridPointer());

		//Create partition and read dis tiff data

		tdpartition *disData;
		disData = CreateNewPartition(disgrid.getDatatype(), totalX, totalY, dx, dy, disgrid.getNodata());
	/*	int nx2 = disData->getnx();
		int ny2 = disData->getny();*/
		disData->localToGlobal(0, 0, xstart, ystart);
		disgrid.read(xstart, ystart, ny, nx, disData->getGridPointer());

       int n=0;
	   int32_t tempLong1;float *numPixel;
       numPixel=new float [nx*ny]; 
       float mbinp=0.050000000;double inc=0.50000000000000000;
	   float mbind=0.200000000; double dinc=500.0000;

		/*loop through for each of the pixel in model element to find out how many pixel  in  the model element*/
	
		for(int i=0; i<nx; i++)
			for(int j=0; j<ny; j++)
			{
				if( !meData->isNodata(i,j) )
				{   //  Grid cell here is in one of the model elements
					numPixel[n]= meData->getData(i,j,tempLong1); /*add pixel grid value to list of all pixel values*/					
					n=n+1; /*counting how many pixel in total basin*/
					
				}/*end of not nodata if condition*/
			} /*end of for loop over all grid cells*/
	/*sorting the pixel value and find out how many basin in the model element tiff file*/
	



			std::vector<long> myvector (n); 
			std::vector<long>::iterator it;
			it=std::unique_copy (numPixel,numPixel+n,myvector.begin());
			std::sort (myvector.begin(),it);
			it=std::unique_copy (myvector.begin(), it, myvector.begin(), myfunction);
			myvector.resize( std::distance(myvector.begin(),it) ); /*myvector gives the unique pixel value of each basin*/
			FILE *fp; 
			fp=fopen(distsfile,"w"); /*opening file for writing results*/
			
		/*calling distribution function for writing atanb value, their distribution
		and ditance value , their distribution */
			
			for (it=myvector.begin(); it!=myvector.end(); ++it) /*loop through each of the basin */
				

				distribution(n,*it, meData, twiData,disData, mbinp,inc,mbind,dinc,nx,ny,fp); 
			fclose(fp);/*close the file */

		}
	MPI_Finalize();
	return 0;

	}



	/*sorting function copied from the previous topset up code*/

	void sort(int nn, float *ra)
	
		{
			int l,j,ir,i;
		float rra;
		l=(nn>>1)+1;
		ir=nn;
		for(;;)
		{
			if(l>1)

				rra=ra[--l];
			else {
				rra=ra[ir];
				ra[ir]=ra[l];
				if(--ir==1)
				{
					ra[l]=rra;
					return;
				}
			}
			i=l;
			j=l<<1;
			while(j<=ir)
			{

				if(j<ir && ra[j] <ra[j+1]) ++j;
				if(rra<ra[j]){
					ra[i]=ra[j];
					j +=(i=j);
				}
				else j=ir+1;
			}

			ra[i]=rra;
		}

	}


	/*distribution function mainly copied from the previous topsetup code*/

	int distribution( int n11, int bn, tdpartition *meData, tdpartition *twiData, tdpartition *disData, float mbinp,double inc,float mbind, double dinc, int rows,int columns,FILE *fp)
	{
		
		FILE *spc; 
		int i,i1,j,n0,n1=0;
		float redfac; //*atbls, *atbl,*datbl,*datbls;
		double *pp,*atbout;
        int32_t tempLong11; float tempLong2,tempLong3; /*initialiazing variables*/

	  //  atbls=(float *) malloc(sizeof (float) *(n11+2));/*problem with working memory, need to fix*/
		//atbl=atbls+1;
		float *atbls=new float[n11+2];  // C++ preferred memory allocation.  malloc will make people think you are 50+ years old.  It is from C many years ago 
		float *atbl;
		atbl=atbls+1;  // This is for the sort function which uses  base 1 indexing
	    int nout=0;
		for(i=0; i<rows; i++)
			for(j=0; j<columns; j++)
				{   /*check whether model element pixel value is equal to particular 
						basin and grab all  atanb value for that*/
						if(meData->getData(i,j,tempLong11)==bn && twiData->getData(i,j,tempLong2)>=0.)
						  { 
							  atbl[n1]= tempLong2;
							  n1=n1+1; /*storing value in array*/
						  }
				}
		






	   if(n1>1)
    //sorting the atanb values
	   sort(n1,atbls);
	/*atbl is now slope/area ranked from smallest to largest*/
	/*Now mark off bins from the highest atbl corresponing to the lowest 
	atanb  defining a nw bin whenever necessary accroding to two criteria
	1. Not more than a specified portion 'mbinp' of the basin in any one bin
	2. ln(a/tanb) interval not larger than a specified increment 'inc'*/


	n0=-1;
	while(atbl[n0+1]<=0. && n0+1 <n1)
	n0++;

	/* n0 gives subscript of last flat pixel(slope/area=0)*/
	
	if(n0==-1) atbl[n0]=atbl[0]; /* This is to prevent out of bounds in bining*/
	/* initialize*/
	int nbmax=int(n1*mbinp); /*possible maximum number in a bin*/
	int minbpix=10;
	 //maximum difference between two classes
	if(nbmax<minbpix)nbmax=minbpix;
	redfac=(float)exp(-(double)inc);
	
	atbl[n1]=atbl[n1-1]; /* to avoid out of bounds problem on first check*/

	i1=n1;
	
	atbout=new double[n1+2];/* Buffers for output */
	pp=new double[n1+2]; /*Buffers for output*/

	/* Dimensioned for worst case scenario when each pixl is a bin */
	nout=0;
	if(atbl[i1-1]<=0.) /* This occurs if the whole basin in flat */
	{
		atbout[nout]=15.; /*just take ln(a/tanb) as alarge value */
	
	}
	else 
	{
		atbout[nout]=(double) -log(atbl[i1-1]);

	}
	
	pp[nout ++]=(double)0.0;

	i=i1-1;

	while(i>n0)
	
	{ 
			 if(( (float) log( atbl[i-1]) < ( (float)log(atbl[i]) -0.00001) ) && (i1- i>=nbmax || atbl[i-1]/atbl[i1] <redfac))
		
				 /*The first check ensures we go to the end of a run o equal values 
				 the check is one on (float) log because in rare casest the atbl values can be
				 numerically less but  the (float) log values that are output are numerically identical causing a problem*/
		{
			if(nout>n1+1) printf(" %d %d A/tanb array overflow -classes too small\n",n1,nout);
		atbout[nout]=(double) -log( atbl[i]);
		
		pp[nout++ ]=(double) (i1-i)/n1;
		
			i1=i;
		}
	
		i=i-1;
	}
	
		if(n0+1 >0)
		{
				if (nout>n1+1) printf(" %d %d A/tan b array overflow at flats\n",n1,nout);
				if(atbl[n0+1] <=0.)
				{
					atbout[nout]=15.;
				}

		else 
		{
	atbout[nout]=(double) (-log(atbl[n0+1]) +1.);
		}

			pp[nout ++]=(double)(n0+1)/n1;
		}
	

		else
		{
			if(nout >n1+1) 

		 printf("%d %d A/tan b array overflow at last val\n", n1,nout);
				atbout[nout]=(double) -log(atbl[0]);
				pp[nout++]=(double) (i1)/n1;
			}

		/*it can occur that the first two values are the same.Check for this am 
		lump together if this is case */

			n0=0;
			if(atbout[0] >= atbout[1])
			{
				/*if nout is only two do not do this*/
				if(nout>2)
				{
					n0=1;
				pp[2]=pp[2]+pp[1];
				pp[1]=(double)0.;
			    }
			else 
			    {

			   /* arbitrarily add 1 to higher a/tanb 
			   this only occurs for single pixel  basins*/

				atbout[1]=atbout[1]+1.;
			    }
			}
	

			

			//for(int ij=0;ij<nout;ij++)//c
				//printf(" %f %f",atbout[ij],pp[ij]);
			//fprintf(fp,"Basin %d ",bn);
			
			/*fprintf(fp,"%d\n",bn);*/
			fprintf(fp,"Number of points in a/tan b distribution\n");
			fprintf(fp,"%d\n",nout-n0);
			fprintf(fp,"a/tanb : ATB,PKA,ATB,PKA..........\n");
			for(int ij=n0;ij<nout;ij++)
				fprintf(fp,"%.9g %g\n",atbout[ij],pp[ij]);
		
			//wrapping up////

			free(atbout);
			free(pp);
		   free(atbls);
		    
	  

		//////////////Distance distribution function Crated ////////////////
		   /*initializing*/
	atbls=new float[n11+2];  // C++ preferred memory allocation.  malloc will make people think you are 50+ years old.  It is from C many years ago 
		
		atbl=atbls+1;  // This is for the sort function which uses  base 1 indexing
	int n2=0;
		for(i=0; i<rows; i++)
	
			for(j=0; j<columns; j++)

				{
			       /* extract dist value for a particular basin */

						if(meData->getData(i,j,tempLong11)==bn && disData->getData(i,j,tempLong3)>=0.)
						{ 
							atbl[n2]= tempLong3; n2=n2+1;	
						}					
			   }
		

		
			
		if(n2>1) sort(n2,atbls); /* sorting dist values for particilar basin */
	
	/* atbl is now distance ranked from smallest to largest */
  /* Now mark off bins from the lowest atbl corresponing to the lowest a/tanb 
  defining a new bin whenever necessary accoring to two cirteria
  1. Not more than a specified proportion 'mbind' of the basin in any one bin
  2. dist interval not larger than a specified increment 'dinc' */

		/*Intitializing */
		
		
		
		nbmax=(int) (n2*mbind);/*Max number in bin*/
		if(nbmax<minbpix)nbmax=minbpix;
		atbout=new double[n2+1];/* Buffers for output */
	    pp=new double[n2+1]; /*Buffers for output*/
		nout=0;
		atbout[nout]=(double) atbl[0];/*initialiaze  out put*/
		pp[nout ++]=(double) 0.0;/*initialize output */
		i1=0;
		i=1;
		while(i<n2-1)
		{

			if((atbl[i+1] >atbl[i]) &&(i-i1 >=nbmax || atbl[i]-atbl[i1]>=dinc))
				/* The first check ensures we go to the end of a run of equal values
				The subsequent checks implement the stopping criteria*/

			{
				if(nout>n2)printf("%d %d Error distance histogram overflow\n",nout,n2);

				atbout[nout]=(double) atbl[i];
				pp[nout++]=(double)(i+1)/n2; /* THis is cumulative proportion up to location
											  i index from 0*/
				i1=i;
			}

			i=i+1;
		}

		/*Print Last value*/

		if(nout>n2) printf("%d %d Error distance histogram overflow at end\n",nout,n2);
		atbout[nout]=(double)atbl[n2-1];
		pp[nout ++]=(double)1.;
		fprintf(fp,"The number of points in the overland flow distance distribution\n");
		fprintf(fp,"%d\n",nout);
		fprintf(fp,"The values of distribution\n");
		for(i=0;i<nout;i++)
			fprintf(fp,"%.9g % g\n", atbout[i],pp[i]);
	   fprintf(fp,"The default initial conditions, sr0, zbar0, cv0\n");
	   float sro=0.0200,zbaro=0.4000,cvo=0.0005000;
	   fprintf(fp,"%f %f %f\n", sro,zbaro,cvo);
		/*printf("%f % f", atbout[i],pp[i]);*/

		/* wrapping up */

		free(atbout);
			free(pp);
			free(atbls);

		return 0;
		
	}
		




	
	
	
	





		












	
	
	
	
	
	

