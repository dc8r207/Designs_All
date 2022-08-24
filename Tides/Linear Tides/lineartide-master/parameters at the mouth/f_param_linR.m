%linR model (single reach, with friction refinement)
%------------------------------------------------------------
% dimensionless parameters at the mouth for infinite channel
% n_iter: number of iterations
%------------------------------------------------------------
function [mu,delta,lambda,phi,n_iter]=f_param_linR(chi,gamma)

%model parameters
kappa=8/(3*pi); %Lorentz's constant
kmax=100;       %max number of iterations
tol=1e-6;       %tolerance to satisfy

%-------- single reach solution (Table 3) ----------
Gamma=1-gamma.^2/4;             %distance from critical conditions [-]
Omega=sqrt(Gamma.^2+chi.^2);    %first guess with chi instead of chi_hat
K=sqrt((Omega-Gamma)/2);
mu=1./sqrt(1+gamma.*K+2*K.^2);  %dimensionless velocity parameter [-]
for kk=1:kmax
    chi_hat=kappa*chi.*mu;
    Omega=sqrt(Gamma.^2+chi_hat.^2);
    K=sqrt((Omega-Gamma)/2);
    mup=mu;
    mu=1./sqrt(1+gamma.*K+2*K.^2);  %dimensionless velocity parameter [-]
    if(abs(1-mu/mup)<tol)
        n_iter=kk;  %number of iterations to satisfy tolerance
        break;      %exit cycle
    end
end
delta=gamma/2-K;                        %dimensionless damping [-]
phi=atan((gamma.*K+2*K.^2)./chi_hat);   %phase lag [rad]
lambda=sqrt(K.^2+Gamma);                %dimensionless wavenumber [-]

return
