#include <mpi.h>
#include <math.h>
#include<sstream>

#include<string>
#include <queue>
#include <omp.h>
#include <algorithm>    // std::sort
#include <vector>
#include "commonLib.h"
#include "linearpart.h"
#include "createpart.h"
#include "tiffIO.h"
#include "shape/shapefile.h"
//// Defines needed for triangle
//#define REAL double
//#define ANSI_DECLARATORS
//#include "triangle.h"
using namespace std;


//subsidiary function used in mepsetup(main ) function//

bool myfunction (int i,int j);
int readTextFile(std::ifstream& infile, std::string **playList);
float pavgwovat (int bn, tdpartition *meData,tdpartition *mepinData,int rows,int columns);
float pavgwvat (int bn, tdpartition *meData,tdpartition *mepinData,int rows,int columns, int nl,float **lookup,int ch);
float addition(int MaxRows,float *data);
string dummyLine;
//Main function//

int mepsetup (char *mefile, char*parspecfile, char *nodelinkfile, char *meparfile)
{
	

	MPI_Init(NULL,NULL);
	{
		

	//Only used for timing
			int rank,size;
			MPI_Comm_rank(MCW,&rank);
			MPI_Comm_size(MCW,&size);
			if(rank==0)printf("model element parameter -h version %s\n",TDVERSION);

			//  Keep track of time
			double begint = MPI_Wtime();
			
			//varibale declaration//
			int i,j,k,n=0,n1,nlmax1,nlmax2,nlmax; int32_t tempLong1;
			long *basin,*basin1;FILE *fp, *fpn, *fp1;string **fileList; float **lookup,**mat1, **cnet;
			char dummy[MAXLN];
			int RPINTDTYPE=1;int RPFLTDTYPE=3;	
	
			//read model element file//
	
			tiffIO megrid(mefile, LONG_TYPE);
			long totalX = megrid.getTotalX();
			long totalY = megrid.getTotalY();
			double dx = megrid.getdxA();
			double dy = megrid.getdyA();
			tdpartition *meData;
			meData = CreateNewPartition(megrid.getDatatype(), totalX, totalY, dx, dy, megrid.getNodata());
			int nx = meData->getnx();
			int ny = meData->getny();
			int xstart, ystart;
			meData->localToGlobal(0, 0, xstart, ystart);
			megrid.read(xstart, ystart, ny, nx, meData->getGridPointer());
			basin=new long [nx*ny]; 
				basin1=new long [nx*ny]; 
				
			for(int i=0; i<nx; i++)
					for(int j=0; j<ny; j++)
					 {
						if( !meData->isNodata(i,j) )

						   {   //  Grid cell here is in one of the model elements
							   basin[n]= meData->getData(i,j,tempLong1); /*add pixel grid value to list of all pixel values*/					
							   n=n+1; /*counting how many pixel in total basin*/
					
						   }/*end of not nodata if condition*/

				      } /*end of for loop over all grid cells*/
	

	
			std::vector<long> myvector (n); 
			std::vector<long>::iterator it;
			it=std::unique_copy (basin,basin+n,myvector.begin());
			std::sort (myvector.begin(),it);
			it=std::unique_copy (myvector.begin(), it, myvector.begin(), myfunction);
			myvector.resize( std::distance(myvector.begin(),it) );

		


			
	       //read parspecfile//
            
			fp=fopen(parspecfile,"r");
			if(fp==NULL) return (9);

			//count length of file //
			i=0;
			nlmax1=-1;
			while(i!=EOF)
			{
				i=readline(fp,dummy);
				nlmax1++;
			}

			printf("%d",nlmax1);
			fclose(fp);
                     nlmax1=nlmax1+1;
			fp=fopen(parspecfile,"r");
			fileList = new string *[nlmax1];
			for ( int i = 0 ; i < (nlmax1) ; i++)

			fileList[i] = new string [nlmax1*10];//need to check//




std::string s; 
                        string var= parspecfile;
						char *varname=new char[var.size()+1];
			
			ifstream infile(var.c_str());
			int y;
			if (infile.is_open())
			     {
					y=readTextFile(infile, fileList);
					infile.close();
				  }
			else
				  printf( "Error Opening file" );
		
		
			
	


             mat1 = new float*[n];//need to work 
					for ( int i = 0 ; i < n ; i++)
                        mat1[i] = new float [500]; //need to wrok
	         fp1=fopen(meparfile,"w");
			 for (n1=0;n1<(nlmax1);n1++)

				      { std::string s; 
                        string var= fileList[n1][0];
						char *varname=new char[var.size()+1];
					    strcpy(varname,var.c_str());
						printf("%s",varname);
			 }
			 //loop over the each of the input file that contains in parspecc txt file//				 
		
			for (n1=0;n1<(nlmax1);n1++)

			     {      
					  if (stoi(fileList[n1][1])<=-1) //check wether parameter is based on the value attribute table or not//
						                  {
									          for (it=myvector.begin(); it!=myvector.end(); it++) 
											//for (int h=0;h<155;h++) //
											
											
										          mat1[*it][n1]=stof(fileList[n1][2]);
											
						                  }	
					 
					 
					 if (stoi(fileList[n1][1])>-1) 
					 { 
					 
					    	
                        std::string s; 
                        string mepin= fileList[n1][2];//mepin=modle element primary input e.g. soildepth.tiff
		                char *mepinfile=new char[mepin.size()+1];
					    strcpy(mepinfile,mepin.c_str());
		 
		                tiffIO mepingrid(mepinfile, FLOAT_TYPE);
						if(!megrid.compareTiff(mepingrid)) 

							{  //  Here the grid dimensions of dem do not match
						printf("Mismatch of grid dimensions\n");
						printf("dem file: %s\n",mepinfile);
						printf("Me file: %s\n",mefile);	
							return 1;  //And maybe an unhappy error message
							}
 
		
						tdpartition *mepinData;
						mepinData = CreateNewPartition(mepingrid.getDatatype(), totalX, totalY, dx, dy, mepingrid.getNodata());
						mepinData->localToGlobal(0, 0, xstart, ystart);
						mepingrid.read(xstart, ystart, ny, nx, mepinData->getGridPointer());
					

						if (stoi(fileList[n1][1])==0) //check wether parameter is based on the value attribute table or not//
						                  {
									          for (it=myvector.begin(); it!=myvector.end(); it++) 
											//for (int h=0;h<17;h++) 
											
											
										          mat1[*it][n1]=pavgwovat (*it,meData,mepinData,nx,ny);
											
						                  }	
						            
						               
						
						 
						if (stoi(fileList[n1][1])==1)
						          {           
										    
											std::string s; 
											string mesin= fileList[n1][3]; //mesin = model element secondary input e.g. lutluc.txt : look up table information
										    char *mesinfile=new char[mesin.size()+1];
											strcpy(mesinfile,mesin.c_str());

											fp=fopen(mesinfile,"r");
											if(fp==NULL) return (9);
											//count length of file //
											i=0;
											nlmax2=-1;
											while(i!=EOF)
											   {
												    i=readline(fp,dummy);
												    nlmax2++;
											   }

											fclose(fp);
											lookup = new float*[nlmax2+1];
											for ( int i = 0 ; i < (nlmax2+1) ; i++)
											lookup[i] = new float[nlmax2+1];

											fp=fopen(mesinfile,"r");
											if(fp==NULL) return (10);
											int atcn=stoi(fileList[n1][4]);//atcn: attribute table column number;
										

											for(j=0;j<(nlmax2+1);j++)
											     {
												    for (  k=0;k<(atcn+1) ;k++)//as we always need two table information, one is pixelidentifier and another is atcn
													fscanf(fp,"%f", &lookup[k][j]);
													eol(fp);
												 }

										    lookup[1][3];
											
										 
	                                          for (it=myvector.begin(); it!=myvector.end(); it++) 
											  {
							                     
												 mat1[*it][n1]=pavgwvat(*it,meData,mepinData,nx,ny,(nlmax2+1),lookup,atcn);
											  }          		    
			                              
						      }
						 
  

			}
		}	

	fpn=fopen(nodelinkfile,"r");

	

	if(fpn==NULL) return (10);
	
	i=0;
	nlmax=-1;
	while(i!=EOF)
	{
		//int readline2(FILE *fp, char *fline);
		i=readline(fpn,dummy);
		//if(i >0)
			nlmax++;
	}
	
	fclose(fpn); /*close the file */
	cnet = new float*[10];
    for ( int i = 0 ; i <10 ; i++)
    cnet[i] = new float[nlmax];
	 
	
	fpn=fopen(nodelinkfile,"r");
	if(fpn==NULL) return (10);


 
                        string var2= nodelinkfile;
						char *varname2=new char[var2.size()+1];

	ifstream stream(var2.c_str());
    
    getline(stream, dummyLine);
	
	
	for(j=0;j<nlmax;j++)
	{
		for ( int ii=0;ii<10;ii++)
		{
			fscanf(fpn,"%f%*c", &cnet[ii][j]);
		}
		//eol2(fpn);
	}
	fclose(fpn);


	



	fprintf(fp1,"%s,%s,%s,%s,%s,%s,%s,%s,","CatchID","DownCatchID","DrainID","NodeId","Reach_number","Outlet_X","Outlet_Y","direct_area");

		  for (i=0;i<(nlmax1);i++) 
		{ std::string s; 
                        string var= fileList[i][0];
						char *varname=new char[var.size()+1];
					    strcpy(varname,var.c_str());
						fprintf(fp1,"%s,",varname);
			 }
		  fprintf(fp1,"%\n");



		  mat1[0][3];
    


    //      for (int g=0; g<(nlmax-1); g++) // as one line is header file
		  // {
			 //  fprintf(fp1,"%d,",g);
			 //  fprintf(fp1,"%d,", int(cnet[1][g]));
				//fprintf(fp1,"%d,",int (cnet[2][g]));
				//fprintf(fp1,"%d,", int(cnet[3][g]));
				//fprintf(fp1,"%d,",int (cnet[5][g]));
				//fprintf(fp1,"%g,", cnet[8][g]);
				//fprintf(fp1,"%g,", cnet[9][g]);
				//fprintf(fp1,"%g,",cnet[6][g]*1000000);//convert area to mm2
		  //    break;
		  int g=0;
			for (it=myvector.begin(); it!=myvector.end(); it++) 
			    {

					fprintf(fp1,"%d,",g+1);
			   fprintf(fp1,"%d,", int(cnet[1][g]));
				fprintf(fp1,"%d,",int (cnet[2][g]));
				fprintf(fp1,"%d,", int(cnet[3][g]));
				fprintf(fp1,"%d,",int (cnet[5][g]));
				fprintf(fp1,"%g,", cnet[8][g]);
				fprintf(fp1,"%g,", cnet[9][g]);
				fprintf(fp1,"%g,",cnet[6][g]*1000000);

					for (int ij=0;ij<(nlmax1);ij++) 
						fprintf(fp1,"%g,",mat1[*it][ij]);
			
			   fprintf(fp1,"%\n");
			   g=g+1;
		  }

		  

	        fclose(fp1);





	

	   } 

    MPI_Finalize();
	
    return 0;
   }

bool myfunction (int i, int j)
{
  return (i==j);
}

int readTextFile(std::ifstream& infile, std::string **playList)
{
    std::string line;
	int h1=0;
    for (int lineIndex = 0; getline(infile, line); ++lineIndex)
    {
        // skip empty lines:
        if (line.empty()) continue;

        std::string word;
        std::istringstream lineStream(line);
        for (int wordIndex = 0; getline(lineStream, word, ','); ++wordIndex)
        { 
            // skip empty words:
            if (line.empty()) continue;

            playList[lineIndex][wordIndex] = word;
				  h1 =wordIndex;
				  
        }
		
    }
	//printf( "%d",h1);
	return h1;
}

float pavgwovat( int bn, tdpartition *meData,tdpartition *mepinData,int rows,int columns) //paravg is the parameter average based on the direct data//
{
	int i,j,n1=0;
	int32_t tempLong2; float tempFloat3,pwovat=0.0,pwovat_avg=0.0;
    for(i=0; i<rows; i++)
		for(j=0; j<columns; j++)


		    {
				if(meData->getData(i,j,tempLong2)==bn && mepinData->getData(i,j,tempFloat3)>=0.)
					  {
						 pwovat =pwovat+tempFloat3;n1=n1+1;//pwovat is the parameter without value attribute table//
					  }			
		   }
		      

	pwovat_avg= pwovat/n1;
	//fprintf(fp1,"%f\n",pwovat_avg);
	//printf("%f",pwovat_avg);//test//
	return pwovat_avg;
	
}





	
//
float pavgwvat( int bn, tdpartition *meData,tdpartition *mepinData,int rows,int columns,int nl,float **lookup,int ch)//parameter average based on the look up table and input data//
{
	int i,j,n2=0,*x;
	int32_t tempLong2; float tempFloat3; float *nlcd,*lpv;float *cc;	
	nlcd=new float[rows*columns];x=new int[rows*columns];lpv=new float[nl];
   
	
	for(i=0; i<rows; i++)
		for(j=0; j<columns; j++)
            {
				if(meData->getData(i,j,tempLong2)==bn && mepinData->getData(i,j,tempFloat3)>=0.)
					{ 
						nlcd[n2]=tempFloat3;
							n2=n2+1;
					}

		   }
		nlcd[4];//for test

	for (int g=0;g<nl;g++)
		lpv[g]=lookup[0][g]; //lpv : lookup vector
       lpv[22];//for test

	cc = new float [n2];
	//for ( int k = 0 ; k < n2 ; k++)
	//	cc[k] = new float[nc+1];//need to work here//
	for(j=0;j<n2;j++)
	  {
		 x[j] = std::distance(lpv, std::find(lpv, lpv + nl+1, nlcd[j]));
		     //for(int u=1;u<(nc+1);u++)//column 0 is the pixel identifier and column1 ,2 .. are the different attribute value for pixel//
		        cc[j]=lookup[ch][x[j]];	
	  }

	delete nlcd;
	return addition(n2,cc);

	
	//for test//

    
	
}

float addition(int MaxRows, float *data)
{
	
	 float sum=0.00; 
    for(int row=0;row<MaxRows;row++) 
    sum  += data[row];
	printf("%f", sum/MaxRows);
	 

  return (sum/MaxRows);
}




	
	

	