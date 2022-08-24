%subroutine: calculate results and produce plots

%------ results: variables and parameters ------
A=a1*exp(w1*x)+a2*exp(w2*x);    %dimensionless water level [-], complex number
V=v1*exp(w1*x)+v2*exp(w2*x);    %dimensionless velocity [-], complex number
H=epsilon*Ds*abs(A);            %dimensional water level [m]
U=epsilon*Cs*abs(V);            %dimensional velocity [m/s]
phiA=atan2(imag(A),real(A));    %phase of water level
phiV=atan2(imag(V),real(V));    %phase of velocity
phi=phiV-phiA;                  %phase lag
phi(end)=nan;                   %last section is not defined for closed channels

%------ plots ------
subplot(3,1,1);
plot(xd/xp,H/ap,[lnstl,'b']);      %water level
subplot(3,1,2);
plot(xd/xp,U/up,[lnstl,'r']);      %velocity
subplot(3,1,3);
plot(xd/xp,phi,[lnstl,'g']);       %phase lag
