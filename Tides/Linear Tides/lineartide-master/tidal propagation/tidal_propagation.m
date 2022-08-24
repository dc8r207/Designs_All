% Toffolon and Savenije (JGR, 2011)
% Revisiting linearized one-dimensional tidal propagation
%------------------------------------------------------------
% Contact: Marco Toffolon, University of Trento, Italy
% marco.toffolon@ing.unitn.it
%------------------------------------------------------------
% MAIN PROGRAM - TIDAL PROPAGATION ALONG THE ESTUARY
% uses subroutines:
% - subroutine_setup_plots (prepare plots);
% - subroutine_results_plots (calculate waves and plot them).
%------------------------------------------------------------
% Characteristic of the solution:
% - single reach and multiple reaches;
% - iterative refinement of friction;
% - solver of linear system: intrinsic Matlab routine.
% Storage ratio sigma = 1 (unnecessary)
%------------------------------------------------------------
% Insert the input data in the section PROBLEM PARAMETERS below
%------------------------------------------------------------
clear; clc;

%-------- model set up ----------
%model parameters
kappa=8/(3*pi); %Lorentz's linearization constant
kmax=100;       %maximum number of iterations
tol=1e-6;       %numerical tolerance
N=20;           %number of reaches
%constant dimensional parameters
km=1000; 
g=9.81; 
omega=2*pi/(12.41*3600);	%M2 tide

%-------- PROBLEM PARAMETERS (start) ----------
inf=2;          %landward boundary condition
                %(=1 infinite length; =2 closed channel)
dimless=1;      %plot type
                %(=1 dimensionless plots; <>1 dimensional plot)
epsilon=0.2;    %dimensionless tidal amplitude [-]
%dimensional parameters
Le=90*km;   %estuary length [m]
ks=45;      %friction [m^(1/3)/s]
            %Gauckler-Strickler coefficient (inverse of Manning)
D0=10;      %depth at the mouth [m]
Lz=0*km;   %depth convergence length [m] (select Lz=0 for constant depth, where Lz=infinite)
if(Lz==0), Lz=9e9; end;     %infinite value of Lz for constant depth
B0=1000;    %width at the mouth [m]
Lb=60*km;   %width convergence length [m] (select Lb=0 for constant width)
if(Lb==0), Lb=9e9; end;     %infinite value of Lb for constant width
%-------- PROBLEM PARAMETERS (end) ----------

%dependent parameters
C0=sqrt(g*D0);  %frictionless wave celerity [m/s]
L0=C0/omega;    %reference length scale [m]
U0=epsilon*C0;  %reference velocity [m/s]
a0=epsilon*D0;  %dimensional tidal amplitude [m]

%-------- single reach solution ('lin0', 'linR') ----------
Ds=D0; Cs=C0; Ls=L0;            %reference values at the seaward end of the channel
Ch=ks/sqrt(g)*Ds.^(1/6);        %dimensionless Chezy parameter [-]
L=Le/Ls;                        %dimensionless channel length [-]
%independent dimensionless parameters (Table 1)
chi=epsilon*Cs/(Ch^2*omega*Ds); %friction [-]
gammaB=Ls/Lb;                   %width convergence [-]
gammaZ=Ls/Lz;                   %depth convergence [-]
gamma=gammaB+gammaZ;            %total convergence [-]
Gamma=1-(gamma/2)^2;            %distance from critical conditions (eq. 18) [-]

%first guess of dimensionless velocity
mu=1/kappa;         %'lin0' model (chi_hat=chi)
x=0:L/(N*100):L;    %dimensionless x-vector [-]
xd=x*Ls;            %dimensional x-vector [m]

%create figure
fig1=figure;
subroutine_setup_plots; %call subroutine to set up plots

%-------- start iterations for 'linR' model (single reach) ----------
%iterations for 'linR' model
%note: the first iteration gives 'lin0' model
for kk=1:kmax
    chi_hat=kappa*mu*chi;           %linearized friction parameter [-]
    Delta=sqrt(-Gamma+1i*chi_hat);  %[-], complex number
    w1=gamma/2+Delta;               %[-], complex number
    w2=gamma/2-Delta;               %[-], complex number
    %free surface coefficients a1, a2 [-], complex numbers
    if(inf==1)
        a1=0;                       %from b.c. for infinite channel
    else
        R1=(Delta+gamma/2)/(Delta-gamma/2);
        a1=1/(1+exp(2*Delta*L)*R1); %from b.c. for finite channel
    end
    a2=1-a1;
    %velocity coefficients v1, v2 [-], complex numbers
    v1=1i*a1/w2;
    v2=1i*a2/w1;
    mup=mu;
    mu=abs(v1+v2);                 %dimensionless velocity parameter [-] at the mouth
    deviation=abs(1-mu/mup);       %deviation
    if(deviation<tol)
        kk_tol=kk;  %number of iterations to satisfy tolerance
        break;      %exit cycle
    end
    if(kk==1)
        %results for 'lin0' model (first iteration)
        lnstl='-.'; %line style for 'lin0' plots
        %call subroutine to plot H,U,phi
        subroutine_results_plots;
        %set limits for plots
        HM=max(H); Hm=min(H);       %water level [m]
        UM=max(U); Um=min(U);       %velocity [m/s]
        fM=max(phi); fm=min(phi);   %phase lag [rad]
    end
end
%results for 'linR' model (first iteration)
lnstl='--'; %line style for 'linR' plots
%call subroutine to plot H,U,phi
subroutine_results_plots;
%set limits for plots
HM=max(HM,max(H)); Hm=min(Hm,min(H));       %water level [m]
UM=max(UM,max(U)); Um=min(Um,min(U));       %velocity [m/s]
fM=max(fM,max(phi)); fm=min(fm,min(phi));   %phase lag [rad]
%-------- end 'linR' model (single reach) ----------

%-------- multiple reaches solution ('linN') ----------
%definitions at the seaward ends of multiple reaches:
%- dimensional quantities
xi=[0:N-1]*Le/N;            %x-coordinates [m]
Ds=D0*exp(-xi/Lz);          %depths [m]
Bs=B0*exp(-xi/Lb);          %widths [m]
Cs=sqrt(g*Ds);              %celerities [m/s]
Ls=Cs/omega;                %length scales [m]
Ch=ks/sqrt(g)*Ds.^(1/6);    %Chézy friction parameters [-]
%- dimensionless quantities
alpha=Ds(2:N)./Ds(1:N-1);               %ratios among reaches [-]
L=diff([xi Le])./Ls;                    %lengths of reaches [-]
chi=epsilon.*Cs./(Ch.^2.*omega.*Ds);    %friction [-]
gammaB=Ls./Lb;                          %width convergence [-]
gammaZ=Ls./Lz;                          %depth convergence [-]
gamma=gammaB+gammaZ;                    %total convergence [-]
Gamma=1-(gamma/2).^2;                   %distance from critical conditions (eq. 18) [-]

%-------- start iterations for 'linN' model (multiple reaches) ----------
mu=chi*0+1;     %first guess (mu=1, chi_hat=chi)
for kk=1:kmax
    chi_hat=kappa*mu.*chi;          %linearized friction parameter [-]
    Delta=sqrt(-Gamma+1i*chi_hat);  %[-], complex number
    w1=gamma/2+Delta;               %[-], complex number
    w2=gamma/2-Delta;               %[-], complex number
    ew1=exp(w1.*L);                 %coefficients [-]
    ew2=exp(w2.*L);                 %coefficients [-]
    %--- linear system ---
    M=zeros(2*N,2*N);               %allocation of matrix coefficients
    P=zeros(2*N,1);                 %allocation of vector coefficients
    for j=1:N-1                     %reaches 1 to N-1
        je=2*j-1;       %equation for water level (H)
        M(je,2*j-1)=ew1(j);
        M(je,2*j)  =ew2(j);
        M(je,2*j+1)=alpha(j);
        M(je,2*j+2)=alpha(j);
        je=2*j;         %equation for velocity (U)
        M(je,2*j-1)=ew1(j)/w2(j);
        M(je,2*j)  =ew2(j)/w1(j);
        pp=alpha(j)^(1/2);
        M(je,2*j+1)=pp/w2(j+1);
        M(je,2*j+2)=pp/w1(j+1);
    end
    %landward boundary condition
    j=N;                %last reach N
    je=2*j-1;           %equation for water level (H)
    M(je,1)=1;
    M(je,2)=1;
    P(je)=1;
    je=2*j;             %equation for velocity (U)
    M(je,2*N-1)=ew1(j)/w2(j);
    if(inf==1)          %infinite channel
        M(je,2*N)=0;
    else                %finite channel
        M(je,2*N)=ew2(j)/w1(j);
    end
    %solution of linear system
    aa=linsolve(M,P);
    a1=aa(1:2:2*N);
    a2=aa(2:2:2*N);
    a1=a1.';            %important: a1'=transpose+conjugate,
    a2=a2.';            %           a1.'=only transpose
    v1=1i*a1./w2;       %important: a1'=transpose+conjugate,
    v2=1i*a2./w1;       %           a1.'=only transpose
    %dimensionless velocity parameter
    mup=mu;
    mu=abs(v1+v2);      %dimensionless velocity parameter [-] at the mouth
    %check the convergence of the iterative refinement of friction
    deviation=1-mu./mup;
    if(length(deviation)>1)         %multiple reaches
        deviation=std(deviation);
    else                            %single reach
        deviation=abs(deviation);
    end
    if(deviation<tol)
        kk_tol=kk;         %number of iteration to satisfy tolerance
        break;          %exit cycle
    end
end

%once that the friction term has been iteratively defined,
%the solution can be determined completely
for j=1:N               %reaches
    x=0:L(j)/10:L(j);   %dimensionless coordinate of reach j [-]
    xd=xi(j)+x*Ls(j);   %total dimensional physical coordinate [m]
    
    %------ results: variables and parameters ------
    A=a1(j)*exp(w1(j)*x)+a2(j)*exp(w2(j)*x);    %dimensionless water level [-], complex number
    H=epsilon*Ds(j)*abs(A);                     %dimensional water level [m]
    V=v1(j)*exp(w1(j)*x)+v2(j)*exp(w2(j)*x);    %dimensionless velocity [-], complex number
    U=epsilon*Cs(j)*abs(V);                     %dimensional velocity [m/s]
    phiA=atan2(imag(A),real(A));                %phase of water level [rad]
    phiV=atan2(imag(V),real(V));                %phase of velocity [rad]
    phi=phiV-phiA;                              %phase lag [rad]
    phi(phi<0)=phi(phi<0)+2*pi;
    if(j==N)
        phi(end)=nan;                           %last section is not defined for closed channels
    end
    
    %------ plots ------
    subplot(3,1,1);             %water level
    plot(xd/xp,H/ap,'b');
    plot(xd(1)/xp,H(1)/ap,'+b');
    subplot(3,1,2);             %velocity
    plot(xd/xp,U/up,'r');
    plot(xd(1)/xp,U(1)/up,'+r');
    subplot(3,1,3);             %phase lag
    plot(xd/xp,phi,'-g');
    plot(xd(1)/xp,phi(1),'+g');

    %set limits for plots
    HM=max(HM,max(H)); Hm=min(Hm,min(H));       %water level [m]
    UM=max(UM,max(U)); Um=min(Um,min(U));       %velocity [m/s]
    fM=max(fM,max(phi)); fm=min(fm,min(phi));   %phase lag [rad]
end
%-------- end 'linN' model (multiple reaches) ----------

%------ plot limits ------
%set limits for dimensionless/dimensional plots
xM=max(xd)/xp;
subplot(3,1,1);
axis([0 xM max(0,Hm/ap-0.1) HM/ap+0.1]);
subplot(3,1,2);
axis([0 xM max(0,Um/up-0.1) UM/up+0.1]);
subplot(3,1,3);
axis([0 xM max(0,fm-0.1) fM+0.1]);
