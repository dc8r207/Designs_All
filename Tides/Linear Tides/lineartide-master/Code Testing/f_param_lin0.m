%lin0 model (single reach, without friction refinement)
%------------------------------------------------------------
% dimensionless parameters at the mouth for infinite channel
%------------------------------------------------------------
function [mu,delta,lambda,phi]=f_param_lin0(chi,gamma)

Gamma=1-gamma.^2/4;
Omega=sqrt(Gamma.^2+chi.^2);
K=sqrt((Omega-Gamma)/2);
mu=1./sqrt(1+gamma.*K+2*K.^2);
delta=gamma/2-K;
phi=atan((gamma.*K+2*K.^2)./chi);
lambda=sqrt(K.^2+Gamma);

return
