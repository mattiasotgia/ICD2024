#include <fstream>
#include <cmath>
#include <TCanvas.h>
#include <TGraphErrors.h>
#include <TApplication.h>
#include <TH1F.h>
#include <TStyle.h>
#include <iostream>
using namespace std;


Double_t
poissonf(Double_t*x,Double_t*par)                                         
{                                                                              
  return par[0]*TMath::Poisson(x[0],par[1]);
}                                                                              
                                 



//TApplication app("gui",0,NULL);


void h() {
 

  // int Nbin=0;
  int nmin=0;
  int nmax=0;
 
  cout<<"Vuoi disegnare (scrivi plot) o fare il fit (scrivi fit)?"<<endl;
  string cosa;
  cin>>cosa;
  cout<<"Dimmi valore minimo e massimo"<<endl;

  cin>>nmin>>nmax;

  int Nbin=nmax-nmin+1;
  TH1F *isto=new TH1F("isto","isto",Nbin,nmin-0.5,nmax+0.5);
  TH1F *iston=new TH1F("iston","iston",Nbin,nmin-0.5,nmax+0.5);
  int n=0;
  int area=0;


  if(cosa=="plot"){

    for(int i=0; i<Nbin; i++){
      cout<<"Dimmi il numero di volte che è hai misurato: "<<nmin+i<<endl;
      cin>>n;
      isto->Fill(nmin+i,n);
      area=area+n;
    }
  }
  if(cosa=="fit"){
    area=0;
    cout<<"Dimmi l'area "<<endl;
    cin>>area;
    for(int i=0; i<Nbin; i++){
      cout<<"Dimmi il numero di volte che è hai misurato: "<<nmin+i<<endl;
      cin>>n;
      double nn=(double)n/(double)area;
      isto->Fill(nmin+i,nn);
      //cout<<"n "<<n<<endl;
      cout<<nn<<endl;
      //    iston->Fill(i,nn);
    }
  }
 
  TCanvas* c=new TCanvas("isto","isto",400,400); 
  
  TF1* pois=new TF1("pois",poissonf,nmin,nmax,2); 
  pois->SetParameter(1,16);                       

  //  TF1 *fun=new TF1("fun","x[0]^x*e^(-x[0])/e.6e-19/(2*8.85e-12)*1e-3*1e-3*log(0.02/x)",Rp,Rcil);
  // fun->Draw();
  //  TF1 *fun2=new TF1("fun2","-1e14*1.6e-19/(4*8.85e-12)*(1e-3*1e-3-x*x+2*1e-3*1e-3*log(0.02/1e-3))",0,Rp);
  if(cosa=="plot"){
    isto->Draw();
  }

  if(cosa=="fit"){
    isto->Draw();
    isto->Fit("pois");     
    pois->Draw("same");   
    cout<<"Valor medio "<<pois->GetParameter(1)<<endl;
    //cout<<"Sigma "<<pois->GetParameter(0)<<endl;
  }
  //  app.Run(true);
  
  // c.Close();
   
}


