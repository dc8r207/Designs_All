% linN model (multiple reaches, with friction refinement)
%------------------------------------------------------------
% Note that this function could also provide separate
% deltaA, deltaV, lambdaA, lambdaV, phiA, phiV.
% - n_iter: number of iterations
% Assumptions for comparison with other solutions:
% - inf=1 infinite channel;
% - gammaZ=0 horizontal bed.
% Le: dimensionless length
% N: number of reaches
%------------------------------------------------------------
function [mu,delta,lambda,phi,n_iter] ...
    =f_param_linN(chi0,gamma0,Le,N)

%model parameters
kappa=8/(3*pi); %Lorentz's constant
kmax=100;       %max number of iterations
tol=1e-6;       %tolerance to satisfy
%for the comparison with the other models:
inf=1;          %=1 infinite channel
gammaZ=0;       %=0 horizontal bed [-]

%-------- multiple reaches solution ----------
xi=[0:N-1]*Le/N;        %x-coordinates [-]
%parameters for reaches (assumed constant along estuary)
chi=xi*0+chi0;          %friction [-]
gamma=xi*0+gamma0;      %total convergence [-]
Ds=exp(-gammaZ*xi);     %dimensionless depth [-]
alpha=Ds(2:N)./Ds(1:N-1);
L=diff([xi Le]);        %lengths of reaches [-]
Gamma=1-(gamma/2).^2;

%-------- start iterations ----------
mu=xi*0+1;              %first guess
for kk=1:kmax
    chi_hat=kappa*mu.*chi;  %linearized friction parameter [-]
    Delta=sqrt(-Gamma+1i*chi_hat);  %[-], complex number
    w1=gamma/2+Delta;       %[-], complex number
    w2=gamma/2-Delta;       %[-], complex number
    ew1=exp(w1.*L);         %coefficients [-]
    ew2=exp(w2.*L);         %coefficients [-]
    
    M=zeros(2*N,2*N);       %allocation of matrix coefficients
    P=zeros(2*N,1);         %allocation of vector coefficients
    for j=1:N-1             %reaches 1 to N-1
        je=2*j-1;   %equation for water level (H)
        M(je,2*j-1)=ew1(j);
        M(je,2*j)  =ew2(j);
        M(je,2*j+1)=alpha(j);
        M(je,2*j+2)=alpha(j);
        je=2*j;     %equation for velocity (U)
        M(je,2*j-1)=ew1(j)/w2(j);
        M(je,2*j)  =ew2(j)/w1(j);
        pp=alpha(j)^(1/2);
        M(je,2*j+1)=pp/w2(j+1);
        M(je,2*j+2)=pp/w1(j+1);
    end
    %landward boundary condition
    j=N;                    %last reach N
    je=2*j-1;               %equation for water level (H)
    M(je,1)=1;
    M(je,2)=1;
    P(je)=1;
    je=2*j;                 %equation for velocity (U)
    M(je,2*N-1)=ew1(j)/w2(j);
    if(inf==1)              %infinite channel
        M(je,2*N)=0;
    else                    %finite channel
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
        n_iter=kk; %number of iteration to satisfy tolerance
        break
    end
end

%parameters at estuary mouth
j=1; 
w1=w1(j); w2=w2(j);
a1=a1(j); a2=a2(j);
v1=v1(j); v2=v2(j);
A=a1+a2;        %water level amplitude [-], complex number
V=v1+v2;        %velocity amplitude [-], complex number
mu=abs(V);      %dimensionless velocity parameter
phiA=atan2(imag(A),real(A));    %phase of water level [rad]
phiV=atan2(imag(V),real(V));    %phase of velocity [rad]
phi=phiV-phiA;                  %phase lag [rad]
phi(phi<0)=phi(phi<0)+2*pi;

%water level
pp=(a1*w1+a2*w2)/A;
deltaA=real(pp);                %damping [-]
lambdaA=-imag(pp);              %wave number [-]

%velocity
pp=(v1*w1+v2*w2)/V;
deltaV=real(pp);                %damping [-]
lambdaV=-imag(pp);              %wave number [-]

delta=(deltaA+deltaV)/2;        %damping [-]
lambda=(lambdaA+lambdaV)/2;     %wave number [-]

return
