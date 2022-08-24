%Savenije et al. (JGR, 2008) solution
%------------------------------------------------------------
% dimensionless parameters at the mouth for infinite channel
%------------------------------------------------------------
function [mu,delta,lambda,phi]=f_param_setal(chi,gamma)

%subcritical case (mixed wave)
pp=27*chi.^2+2*(9-gamma.^2).*gamma.*chi+8-gamma.^2;
m1=(27*chi+(9-gamma.^2).*gamma+3*sqrt(3)*sqrt(pp)).^(1/3);
mu1=sqrt((m1-gamma+(gamma.^2-6)./m1)./(3*chi));
mu1(mu1>1)=nan;
delta1=(gamma-chi.*mu1.^2)/2;
pp=(gamma-delta1).*mu1;
phi1=asin(pp);
lambda1=sqrt(1+(chi.^2.*mu1.^4-gamma.^2)/4);

%supercritical case
Gamma=1-gamma.^2/4;
delta2=gamma/2-sqrt(-Gamma);
mu2=delta2;
phi2=gamma*0+pi/2;
lambda2=gamma*0;

%critical threshold
m1=(chi.^2-2).^2.*(27*chi.^2-4);
m1=36*chi.^2.*(3*chi.^2+8)-8+12*chi.*sqrt(3*m1);
m1=m1.^(1/3);

%critical gamma and sub/supercritical curves merging
gammac=(m1/2-1+2*(12*chi.^2+1)./m1)./(3*chi);
pp=(gamma>gammac);
mu=mu1;mu(pp)=mu2(pp);
delta=delta1;delta(pp)=delta2(pp);
lambda=lambda1;lambda(pp)=lambda2(pp);
phi=phi1;phi(pp)=phi2(pp);

%check possibile infinite values for chi-->0
pp=~isfinite(mu);
mu(pp)=nan;
delta(pp)=nan;
lambda(pp)=nan;
phi(pp)=nan;

return
