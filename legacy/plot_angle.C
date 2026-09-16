#include <fstream>
#include <cmath>
#include <TCanvas.h>
#include <TGraph.h>
#include <TApplication.h>
#include <TH1F.h>
#include <TStyle.h>
#include <iostream>
using namespace std;


Double_t ffunction(Double_t* x,Double_t* par)                                         
{                                                                              
  return par[0]*cos(2*3.14/360*x[0])*cos(2*3.14/360*x[0]);
}                                                                              
                                 



//TApplication app("gui",0,NULL);


void plot_angolo() {
 

  int N=0;
  int nmin=0;
  int nmax=0;
  int Nmis=0;
 
  cout<<"Dimmi quanti punti (valori dell'angolo) hai preso "<<endl;
  cin>>N;

  cout<<"Dimmi quante misure hai preso per ogni angolo "<<endl;
  cin>>Nmis;
  double *x=new double[N];
  double *y=new double[N];
  double *ex=new double[N];
  double *ey=new double[N];

  double errx;
  cout<<"Dimmi il valore dell'errore sugli angoli "<<endl;
  cin>>errx;
  for(int i=0; i<N; i++){
    cout<<"Dimmi i valori X"<<endl;
    cin>>x[i];
    ex[i]=errx;
  }

  for(int i=0; i<N; i++){
    cout<<"Dimmi i valori Y"<<endl;
    cin>>y[i];
    ey[i]=sqrt(y[i])/sqrt(Nmis);
  }

  TGraphErrors *plot=new TGraphErrors(N, x, y,ex,ey);
 
 
  TCanvas *c=new TCanvas("plot2","plot2",400,600);; 
 
  TF1* fun = new TF1("fun",ffunction,nmin,nmax,1); 
 
  plot->Draw("AP");
  plot->Fit("fun");
 
  cout<<"Valor medio del flusso "<<fun->GetParameter(0)<<endl;
  // app.Run(true);
 
  // c.Close();
   
}


