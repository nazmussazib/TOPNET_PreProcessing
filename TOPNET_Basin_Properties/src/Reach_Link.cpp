#include <mpi.h>
#include <math.h>
#include <algorithm>    // std::sort
#include <vector>
#include <queue>
#include "commonLib.h"
#include "linearpart.h"
#include "createpart.h"
#include "tiffIO.h"
#include "shape/shapefile.h"


using namespace std;


//extern int **rtable;
//extern float **rprops;
double me_bnd1,me_bnd2,dx;
int **rtable, **nodetable; float **rprops; float **nodevals;
int markthreshg,markthresh;
long *reachnodeids,gmin1;
float ndv;
int ny,nx;
int markbasin ( int *nb, tdpartition *meData, tdpartition *pData,int *nd,int ilink,int **cnet, float ** coord,int *nrch, long *dsnodeid , int prevnode, int prevmoel);
void ldarea(int i, int j, int lab,tdpartition *pData);
void larea(int i, int j, int lab,tdpartition *pData);
int writereachareas(char *fname, FILE *fp, int **rtable, float **rprops, int nrc, int nrch, long *reachnodeids);
//Calling function
static vector < int >*base_arr;
struct compare_index
{
  const vector<int> base_arr;
  compare_index (const vector<int> &arr) : base_arr (arr) {}
 
  bool operator () (int a, int b) const
  {
    return (base_arr[a] < base_arr[b]);
  }
};
//  Global partitions that represent grids used deep in functions
tdpartition *pData;
tdpartition *dcatch;
tdpartition *nodecatch;


int reachlink( char *mefile,  char *pfile,char *treefile, char *coordfile, char *reachlinkfile, char *nodelinkfile, char *dcfile, char *ncfile,char *rchareasfile,char*rchpropertiesfile)
{
	MPI_Init(NULL,NULL);{

	//Only used for timing
	int rank,size;
	MPI_Comm_rank(MCW,&rank);
	MPI_Comm_size(MCW,&size);
	if(rank==0)printf("reachlink -h version %s\n",TDVERSION);

	float wt=1.0,angle,sump,distr,dtss;
	double p;

	//  Keep track of time
	double begint = MPI_Wtime();

	
	FILE *fp, *fp1, *fp2, *fp3;
	int i,j,nc,nlmax,nrc,nhc,nrch,thisreach;
	int **cnet,**cnet1;
	float **coord;
	char dummy[MAXLN];
	
	int *nrl, *nrh, *ncol,*myints; 
	int ivalue;
	float ***pval;
	//int nrc, int nrch, nhc,markthresh,thisreach;

	
	/*reading tree file*/

	fp=fopen(treefile,"r");
	if(fp==NULL) return (9);

	//count length of file //
	i=0;
	nlmax=-1;
	while(i!=EOF)
	{
		//int readline2(FILE *fp, char *fline);
		i=readline(fp,dummy);
		//if(i >0)
			nlmax++;
	}
	
	fclose(fp); /*close the file */
	//nlmax=nlmax+1;
	//cnet=(int **) matalloc(7,nlmax,2);/*allocation of memory */
	//int **cnet1;
	//cnet1=(int **) matalloc(7,nlmax,2);
	//
	
	nlmax=nlmax+1;
	cnet = new int*[7];
   for ( int i = 0 ; i < 7 ; i++)
   cnet[i] = new int[nlmax+1];
	//
	cnet1 = new int*[7];
    for ( int i = 0 ; i < 7 ; i++)
    cnet1[i] = new int[nlmax+1];
	


	fp=fopen(treefile,"r");
	if(fp==NULL) return (10);
	long *dsnodeid,*dsnodeid1;

	dsnodeid=new long [nlmax];
	dsnodeid1=new long [nlmax];
	for(j=0;j<nlmax;j++)
	{
		for ( i=0;i<7;i++)
		
			fscanf(fp,"%d", &cnet[i][j]);
		
		fscanf(fp,"%d", &dsnodeid[j]);
		eol(fp);
	}
	fclose(fp);
	int nr;
    vector < int >arr, idx;
 
   arr.resize (nlmax);
   idx.resize (nlmax);
 
  //cout << "\nEnter the list: ";
  for (int i = 0; i < nlmax; i++)
     arr[i]=cnet[0][i];
    arr[nlmax-1]=-9999;
  /* initialize initial index permutation of unmodified `arr'
   */
  for (int i = 0; i < nlmax; i++)
    {
      idx[i] = i;
    }
 
  base_arr = &arr;

sort (idx.begin (), idx.end (), compare_index (arr));

 
  cout << "\nOriginal list: ";
  for (int i = 0; i < nlmax; i++)
    {
      cout << (*base_arr)[i] << " ";
    }
 
  cout << "\nSorted index: ";
  for (int i = 0; i < nlmax; i++)
    {
      cout << idx[i] << " ";
    }
 
  cout << "\nSorted array using arr[sorted_idx[i]]: ";
  for (int i = 0; i < nlmax; i++)
    {
      cout << (*base_arr)[idx[i]] << " ";
    }
 
  
  for(j=0;j<nlmax;j++)
	{
		for ( int ii=0;ii<7;ii++)
		
		cnet1[ii][j]=cnet[ii][idx[j]];
		dsnodeid1[j]=dsnodeid[idx[j]];
		//fscanf(fp,"%d", &dsnodeid[idx[j]]);
		//eol(fp);
	}
    
   //int myints[];

   myints = new int [nlmax];
 // cnet1[0][6];
  int *ccnet1;//converted cnet1
 
  ccnet1 = new int[nlmax];
  for(j=0;j<nlmax;j++)
	 ccnet1[j]=j;

  for(j=0;j<nlmax;j++)
	 myints[j]=cnet1[0][j];
 myints[0]=-9999;
  std::vector<int> myvector (myints, myints+nlmax); 


  //int myints[] = { 0,3,5,6,7 };
  
   for(j=0;j<nlmax;j++)
	   
   {
			int x1 = std::distance(myints, std::find(myints, myints+nlmax, cnet1[3][j]));
			int x2 = std::distance(myints, std::find(myints, myints+nlmax, cnet1[4][j]));
			int x3 = std::distance(myints, std::find(myints, myints+nlmax, cnet1[5][j]));
			if(cnet1[3][j]>-1)cnet1[3][j]=ccnet1[x1];
			   
			
			if(cnet1[4][j]>-1)cnet1[4][j]=ccnet1[x2];
			if(cnet1[5][j]>-1)cnet1[5][j]=ccnet1[x3];


       
   }

	   
  

    for(j=0;j<nlmax;j++)
	 cnet1[0][j]=j;
	
	//printf("%d",cnet1[0][12]);
    

	/*reading coordfile */

	fp=fopen(coordfile, "r");
	if(fp==NULL) return (10);///problem also here about what shoud b rturn
	i=0;  
	nc=0;
	while(i !=EOF)
	{
		i=readline(fp,dummy);
		nc++;
	}

	//coord= (float **) matalloc( nc,nc,3);
	coord = new float*[5];
    for ( int i = 0 ; i < 5 ; i++)
    coord[i] = new float[nc];
	nc=nc-1;
	fclose(fp);
	fp=fopen(coordfile, "r");
	if(fp==NULL) return (10);
	
	for(j=0;j<nc;j++)
		 for( i=0;i<5;i++) 
			 fscanf(fp, "%f", &coord[i][j]);
	  printf("%f", &coord[i][j]);
	
	fclose(fp);

	
	tiffIO megrid(mefile, LONG_TYPE);
	long totalX = megrid.getTotalX();
	long totalY = megrid.getTotalY();
    double dxA = megrid.getdxA();
	double dyA = megrid.getdyA();
	me_bnd1=megrid.getXLeftEdge();
	me_bnd2=megrid.getYTopEdge();
	
	tiffIO pgrid(pfile, SHORT_TYPE);
	/*long totalX1 = felgrid.getTotalX();
	long totalY1 =felgrid.getTotalY();
    double dx1 = felgrid.getdx();
	double dy1 =felgrid.getdy();*/

	
	
	if(!megrid.compareTiff(pgrid)) 
		{  //  Here the grid dimensions of dem do not match
			printf("Mismatch of grid dimensions\n");
			printf("p file: %s\n",pfile);
			printf("Me file: %s\n",mefile);	
			return 1;  //And maybe an unhappy error message
		}
	/*long totalX= felgrid.getTotalX();
	long totalY2 = felgrid.getTotalY();
	double dx2= felgrid.getdx();
	double dy2= felgrid.getdy();*/
	
	printf("error");

	/*Create partition and read model element data */

	tdpartition *meData;
	meData = CreateNewPartition(megrid.getDatatype(), totalX, totalY, dxA, dyA, megrid.getNodata());
	int nx = meData->getnx();
	int ny = meData->getny();
   int xstart, ystart;
	meData->localToGlobal(0, 0, xstart, ystart);
	megrid.read((long)xstart, (long)ystart, (long)ny, (long)nx, meData->getGridPointer());
	

	/*Create partition and read flow direction data */
	
	tdpartition *pData;   // This is declared as global
	pData = CreateNewPartition(pgrid.getDatatype(), totalX, totalY, dxA, dyA, pgrid.getNodata());
	//int nx2 = felData->getnx();
	//int ny2 = felData->getny();
	
	pData->localToGlobal(0, 0, xstart, ystart);
	pgrid.read((long)xstart, (long)ystart, (long)ny, (long)nx, pData->getGridPointer());

	//create node catchment  and drainage catchment partitions that were declared global earlier
	long catchnodata=MISSINGLONG;
	nodecatch = CreateNewPartition(LONG_TYPE, totalX, totalY, dxA, dyA, catchnodata);
	dcatch = CreateNewPartition(LONG_TYPE, totalX, totalY, dxA, dyA, catchnodata);

//for( int y=0;y<7;y++){
//cnet1[y][1]=cnet1[y][0];
//}


   int count=0;
   int n=0;
   int32_t tempLong1,tempLong3,gmin1,gmin3,gmax1;float tempLong2,gmin2;
   float x, y;
        int nb=0;int nd=0;
		markthreshg=markthresh;
		int prevnode=-1;
		int prevmoel=-1;
		nrc=2*nlmax;
		nrch=nrc-1;
		nhc=5*nlmax-2;
		rtable=imatrix(nrc,nhc,1,3);
		rprops=matrix(nrc,nhc,1,5);
		reachnodeids=lvector(nrc,nhc);
		nodetable=imatrix(1,nlmax,1,9);
		nodevals=matrix(1,nlmax,1,4);
		
			//printf("%d",nlmax);
	
			//nlmax=nlmax-1;
		for (int i=0;i<nlmax;i++)
		{
			
			if(cnet1[3][i]==-1)
				
			{
				thisreach=markbasin( &nb,meData,pData, &nd, i, cnet1,coord, &nrch, dsnodeid1, prevnode, prevmoel);
				//printf("%d",nodetable[i][4]);
			}
		

		}

		printf("%d",nb);
	//  Write grid files
		tiffIO dcIO(dcfile, LONG_TYPE, &catchnodata, pgrid);
		dcIO.write(xstart, ystart, ny, nx, dcatch->getGridPointer());

		tiffIO ncIO(ncfile, LONG_TYPE, &catchnodata, pgrid);
		ncIO.write(xstart, ystart, ny, nx, nodecatch->getGridPointer());

		rprops[1][2];
		rtable[30][1];
		//writng reachlink file//
		fp2=fopen(reachlinkfile, "w");
		fprintf(fp2," Reach linkages\n");
		for(int kk=nrc;kk<=nrch;kk++)
		
			fprintf(fp2,"%5d %4d %4d %f %1f %d\n",rtable[kk][1],rtable[kk][2],rtable[kk][3],rprops[kk][4],rprops[kk][5],reachnodeids[kk]);
		
	
		

		//for(i=1; i <=nb; i++)
	 //  {
		//	   int basinid;
		//	   //if(nodetable[i][5] == 1 )   // Here it is the downstream element or we are using all nodes
		//		 {
		//	
  //               fprintf(fp2,"%d, ",i); 
		//	    fprintf(fp2,"%d, ",nodetable[i][3]);   // Drainage ID
		//		fprintf(fp2,"%d, ",nodetable[i][9]);   //downstreamcatchment ID
		//		fprintf(fp2,"%d, ",nodetable[i][1]);   // Node ID
		//		fprintf(fp2,"%d, ",nodetable[i][6]);   // Reach ID
		//		fprintf(fp2,"%.2f, ",nodevals[i][3]);  // X
		//		fprintf(fp2,"%.2f, ",nodevals[i][4]);  // Y
		//		fprintf(fp2,"\n");

		//        }
  //    }
	
		fclose(fp2);
		fp2=fopen(rchpropertiesfile,"w");
		fprintf(fp2," Reach properties\n");
		float rpd[3];
		 rpd[0]=0.24;
		 rpd[1]=0.00110700;
		 rpd[2]=0.518000;

		for(int in=nrc;in<=nrch;in++)
		{
			fprintf(fp2,"%f ",rprops[in][1]);
		    fprintf(fp2,"%f ",rpd[0]/100);
			fprintf(fp2,"%g ",rpd[1]*pow((double)rprops[in][2],(double)rpd[2])*1000.);
			fprintf(fp2,"%g \n",rprops[in][3]*1000.);
		}

		
			

    fclose(fp2);

	fp3=fopen(nodelinkfile,"w");
 	fprintf(fp3,"NodeId, DownNodeId, DrainId, ProjNodeId, DOutFlag, ReachId, Area, AreaTotal, X, Y\n"); 

	for(i=1;i<=nb;i++)nodetable[i][7]=0;
	int bn;
	for(i=0;i<ny;i++)
		for(j=0;j<nx;j++)
		{
			bn=nodecatch->getData(j,i,tempLong1);
			if(bn>=1 && bn<=nb)
			{
				nodetable[bn][7]+=1;
			}
		}


 	for(int im=1; im <= nb; im++)
	{   
		nodevals[im][1]=nodetable[im][7]*dxA*dyA;
		fprintf(fp3, "%d, ", nodetable[im][4]);
		fprintf(fp3, "%d, ", nodetable[im][2]);
		fprintf(fp3, "%d, ", nodetable[im][3]);
		fprintf(fp3, "%d, ", nodetable[im][1]);
		fprintf(fp3, "%d, ", nodetable[im][5]);
		fprintf(fp3, "%d, ", nodetable[im][6]);
		fprintf(fp3, "%G, ", nodevals[im][1]);
		fprintf(fp3, "%G, ", nodevals[im][2]);
		fprintf(fp3, "%.2f, ", nodevals[im][3]);
		fprintf(fp3, "%.2f", nodevals[im][4]);
		fprintf(fp3,"\n");
	}
	fclose(fp3);

	fp3=fopen(rchareasfile,"w");
	int err;
	//err=writereachareas(rchareasfile, fp, rtable, rprops, nrc, nrch, reachnodeids);
	fclose(fp3);
	}
		MPI_Finalize();

	return 0;
}

int writereachareas(char *fname, FILE *fp, int **rtable, float **rprops, int nrc, int nrch, long *reachnodeids)
{
int err=0, irc,ioutcount,ireccount;
char recoutstring[4096],rnostr[8],alloutstring[4096];
FILE *frap;
frap=fopen(fname,"w");
if(frap == NULL)return(1);
//  initialize reachoutstring
sprintf(recoutstring," ");
sprintf(alloutstring," ");
ioutcount=0;
ireccount=0;

for(irc=nrc; irc <=nrch; irc++)
{
	if(reachnodeids[irc] >= 0)
	{
		fprintf(frap,"%d %g %d %10.0f %10.0f 0 0 Unknown\n",rtable[irc][1], rprops[irc][2],reachnodeids[irc],rprops[irc][4],rprops[irc][5]);
		ioutcount=ioutcount+1;
		sprintf(rnostr,"%d ",rtable[irc][1]);
		if(reachnodeids[irc] > 0)
		{    // Here we have a flow recorder
			ireccount = ireccount+1;
			strcat(recoutstring,rnostr);
		}
		else
		{    // Here we have an end point without flow recorder.  (end points of stream raster flagged by 0)
			strcat(alloutstring,rnostr);
		}
	}
}
if(ioutcount == 0)
{
	//  Here no reaches were output - so output the first one
		irc=1;
		fprintf(frap,"%d %g %d %10.0f %10.0f 0 0 Unknown",rtable[irc][1], rprops[irc][2],reachnodeids[irc],rprops[irc][4],rprops[irc][5]);
		ioutcount=ioutcount+1;
		sprintf(rnostr,"%d",rtable[irc][1]);
		strcat(alloutstring,rnostr);
}

fprintf(fp,"%d %d  nFlowRecorders, nFlowOutLocations   EDIT THESE TO CHANGE MULTIPLE RESPONSES OR OUTFLOWS\n",ireccount,ioutcount);
fprintf(fp,"%s %s  ADD/EDIT REACH NUMBERS TO CHANGE MULTIPLE RESPONSES\n",recoutstring, alloutstring);

return(err);
}



int markbasin ( int *nb, tdpartition *meData,tdpartition *pData,int *nd,int ilink,int **cnet1, float ** coord,int *nrch, long *dsnodeid1 , int prevnode, int prevmoel)
{
	int row,col,iup1,iup2,flag=0,thisreach; //markthreshg=0,nx,ny;
	int n1=0;
	float x, y;
	int32_t tempLong1;
	int nx = meData->getnx();
	int ny = meData->getny();
	double dx = meData->getdxA();

	
	int icend,icbeg,icarea;
	icend=cnet1[2][ilink];
	icbeg=cnet1[1][ilink];
	printf("%d",icend);
   printf("%d",icbeg);
	if(icbeg <icend)
		
	{
		icarea=icend;
		if(cnet1[3][ilink] !=-1)
			
			if( cnet1[4][cnet1[3][ilink]]>0  && cnet1[5][cnet1[3][ilink]] >0)
				icarea=icend-1;

		         if(dsnodeid1[ilink] >-2)
			
			  {   
								*nb=*nb+1;
						x=coord[0][icarea];
						y=coord[1][icarea];
	
						col=(int) floor ((x -me_bnd1)/dx);
						row=(int ) floor((me_bnd2-y)/dx);

						if( row<0 || row>ny || col<0 ||col >nx)
						   {

							return (-2);
						   }


							larea (row,col,*nb,pData);
						

							//conduct not table coneectivity 


							nodetable[*nb][1]=dsnodeid1[ilink];
							nodetable[*nb][2]=prevnode;
							prevnode=*nb;
							nodetable[*nb][3]=meData->getData(col,row,tempLong1);
							nodetable[*nb][4]=*nb;
							nodetable[*nb][5]=1;

							int i;
		
							for(i=1;i<*nb;i++)
							  {

								if(nodetable[i][3]==meData->getData(col,row,tempLong1))nodetable[*nb][5]=0;
							  }

								nodetable[*nb][9]=prevmoel;
		
								if(nodetable[*nb][5]>0)

								   {
									*nd=*nd+1;
									ldarea(row,col,*nd,pData);
									prevmoel=*nd;
								  }

									nodevals[*nb][2]=coord[4][icarea];
									nodevals[*nb][3]=x;
									nodevals[*nb][4]=y;
									nodetable[*nb][6]=*nrch+1;
									nodetable[*nb][8]=*nd;
	           }
  }



	else
	{
		x=coord[icend][0];
		y=coord[icend][1];
		col=(int) floor ((x -me_bnd1)/dx);
		row=(int ) floor((me_bnd2-y)/dx);

		if( row<0 || row>ny || col<0 ||col >nx)
		{

			return (-2);
		}
		icarea=icend;
		flag=1;
	}
	




	//search for upstream basin

	iup1=cnet1[5-1][ilink];
	iup2=cnet1[6-1][ilink];
	
	if(iup1>0 || iup2>0)
	{
		if(flag==1)
		{
			*nrch=*nrch+1;
			thisreach=*nrch;
			rtable[thisreach][1]=thisreach;

			if(iup1>0)
				rtable[thisreach][2]=markbasin(nb,meData,pData,nd,iup1,cnet1, coord, nrch,dsnodeid1,prevnode,prevmoel);
			else
				rtable[thisreach][2]=0;
			if(iup2>0)
				rtable[thisreach][3]=markbasin(nb,meData,pData,nd,iup2,cnet1, coord, nrch,dsnodeid1,prevnode,prevmoel);
			else
				rtable[thisreach][3]=0;

			reachnodeids[thisreach]=dsnodeid1[ilink];
			 rprops[thisreach][1]=0.01f;
			 rprops[thisreach][2]=coord[4][icarea];
			 rprops[thisreach][3]=0.;
			 rprops[thisreach][4]=coord[0][icarea];
			 rprops[thisreach][5]=coord[1][icarea];
		}

		else

		{

			*nrch=*nrch+1;
			thisreach=*nrch;
			rtable[thisreach][1]=thisreach;
			rtable[thisreach][2]=*nb;
			rtable[thisreach][3]=*nrch+1;
			reachnodeids[thisreach]=dsnodeid1[ilink];
			rprops[thisreach][3]=(coord[2][icbeg]-coord[2][icend])/2.;
			rprops[thisreach][2]=coord[4][icarea];
			rprops[thisreach][1]=(coord[3][icbeg] -coord[3][icend])/(2.*(rprops[thisreach][3]));
			rprops[thisreach][4]=coord[0][icarea];
			rprops[thisreach][5]=coord[1][icarea];

			//upper half reach//


          *nrch=*nrch+1;
		  rtable[thisreach +1][1]=*nrch;

		  if(iup1>0)
			  rtable[thisreach+1][2]=markbasin(nb,meData,pData,nd,iup1,cnet1,coord,nrch,dsnodeid1,prevnode, prevmoel);
		  else
			  rtable[thisreach +1][2]=0;
		  if(iup2>0)
        rtable[thisreach+1][3]=markbasin(nb,meData,pData,nd,iup2,cnet1,coord,nrch,dsnodeid1,prevnode,prevmoel);
		  else
			  rtable[thisreach +1][3]=0;
		  reachnodeids[thisreach+1]=-1;
		  rprops[thisreach+1][3]=rprops[thisreach][3];
		  rprops[thisreach+1][2]=rprops[thisreach][2];
		  rprops[thisreach+1][1]=rprops[thisreach][1];
		  rprops[thisreach+1][4]=coord[0][(icarea+icbeg)/2];
		  rprops[thisreach+1][5]=coord[1][(icarea+icbeg)/2];


		}
	}

	else

		//this is an external basin//
	{
		*nrch=*nrch+1;
	thisreach=*nrch;
	rtable[*nrch][1]=*nrch;
	rtable[*nrch][2]=*nb;
	rtable[*nrch][3]=0;
	reachnodeids[thisreach]=dsnodeid1[ilink];
	rprops[thisreach][3]=(coord[2][icbeg]-coord[2][icend])/2.;
	rprops[thisreach][2]=coord[4][icarea];
	rprops[thisreach][1]=(coord[3][icbeg] -coord[3][icend])
		                     /(2.*rprops[thisreach][3]);
	rprops[thisreach][4]=coord[0][icarea];
	rprops[thisreach][5]=coord[1][icarea];
	}

	
	return (thisreach);
	}

	void larea(int i, int j, int lab,tdpartition *pData)
	{
		int32_t tempLong3,tempLong1;
		int in, jn,k;
		int32_t llab=(int32_t)lab;
	//  This is a recursive function to label grid cells that drain to the start cell with the value "lab" by recursively 
	//  identifying all grid cells upstream
	//  if cell is already labeled with "lab", skip.  No need to repeat if already labeled
	//     Is the cell a non edge grid cell with a valid flow direction
			if(nodecatch->getData(j,i,tempLong3)!=llab)
			{
				//	Enter here if not labeled
				//  Is the cell a non edge grid cell with a valid flow direction
			//if(i!=0 && i!=ny-1 && j!=0 && j!=nx-1 && pData->getData(j,i,tempLong3)!=-1)
			if(i!=0 && i!=ny-1 && j!=0 && j!=nx-1 && (!pData->isNodata(j,i)))
			{
				// Label the cell with the input label  DGT
				nodecatch->setData(j,i,llab);
				//  Look for all neighbors
				for (k=1;k<=8;k++)
				{
					in=i+d2[k];
					jn=j+d1[k];
					//  in, jn is the row and column of a neighbor
					//  Does the neighbor point to me
                    if(!pData->isNodata(jn,in)){
						short pdir=pData->getData(jn,in,pdir);
						if(pdir-k==4 || pdir-k==-4)
						{
    						larea(in,jn,lab,pData);
						}
					}
				}
			}
		}
	}

		void ldarea(int i, int j, int lab,tdpartition *pData)
	{
		int32_t tempLong3,tempLong1;
		int in, jn,k;
		int32_t llab=(int32_t)lab;
	//  This is a recursive function to label grid cells that drain to the start cell with the value "lab" by recursively 
	//  identifying all grid cells upstream
	//  if cell is already labeled with "lab", skip.  No need to repeat if already labeled
	//     Is the cell a non edge grid cell with a valid flow direction
			if(dcatch->getData(j,i,tempLong3)!=llab)
			{
				//	Enter here if not labeled
				//  Is the cell a non edge grid cell with a valid flow direction
			//if(i!=0 && i!=ny-1 && j!=0 && j!=nx-1 && pData->getData(j,i,tempLong3)!=-1)
			if(i!=0 && i!=ny-1 && j!=0 && j!=nx-1 && (!pData->isNodata(j,i)))
			{
				// Label the cell with the input label  DGT
				dcatch->setData(j,i,llab);
				//  Look for all neighbors
				for (k=1;k<=8;k++)
				{
					in=i+d2[k];
					jn=j+d1[k];
					//  in, jn is the row and column of a neighbor
					//  Does the neighbor point to me
                    if(!pData->isNodata(jn,in)){
						short pdir=pData->getData(jn,in,pdir);
						if(pdir-k==4 || pdir-k==-4)
						{
							//  Label the neighbor and proceed up
							ldarea(in,jn,lab,pData);
						}
					}
				}
			}
		}
	}