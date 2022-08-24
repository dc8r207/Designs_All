% Toffolon and Savenije (JGR, 2011)
% Revisiting linearized one-dimensional tidal propagation
%------------------------------------------------------------
% Contact: Marco Toffolon, University of Trento, Italy
% marco.toffolon@ing.unitn.it
%------------------------------------------------------------
% MAIN PROGRAM - PARAMETERS AT THE MOUTH
% uses external functions:
% - f_param_setal (Savenije et al. (2008) solution);
% - f_param_lin0 ('lin0' model);
% - f_param_linR ('linR' model);
% - f_param_linN ('linN' model).
%------------------------------------------------------------
% Dimensionless parameters at the mouth as a function of gamma/chi:
% - single reach and multiple reaches;
% - iterative refinement of friction;
% - solver of linear system: intrinsic Matlab routine.
% Storage ratio sigma = 1 (unnecessary).
% Comparison with Savenije et al. (JGR, 2008) solution.
%------------------------------------------------------------
% Insert the input data in the section PROBLEM PARAMETERS below
%------------------------------------------------------------
clear; clc;

%-------- PROBLEM PARAMETERS (start) ----------
varvar=1;       %=1 variable gamma; =2 variable chi
gamma_max=3.6;  %fixed or max value of gamma (total convergence)
chi_max=3.56;   %fixed or max value of chi (friction parameter)
%-------- PROBLEM PARAMETERS (end) ----------

%setting of the variable parameter for plots
if(varvar==1)
    gamma=0:gamma_max/100:gamma_max;
    chi=gamma*0+chi_max;
    xlab='\gamma';
    var=gamma;
elseif(varvar==2)
    chi=0:chi_max/100:chi_max;
    gamma=chi*0+gamma_max;
    xlab='\chi';
    var=chi;
end

%-------- analytical solutions ----------

%--- Savenije et al. (JGR, 2008)
[muS,deltaS,lambdaS,phiS]=f_param_setal(chi,gamma);

%--- lin0 model (single reach, without friction refinement)
[mu0,delta0,lambda0,phi0]=f_param_lin0(chi,gamma);

%--- linR model (single reach, with friction refinement)
[muR,deltaR,lambdaR,phiR,n_iterR]=f_param_linR(chi,gamma);

%--- linN model (multiple reaches, with friction refinement)
nv=length(var);     %elements of the vector of the independent variable
%model parameters (infinite length case)
NN=20;              %number of reaches
LeN=1;              %dimensionless length of the channel [-]
%pre-allocate vectors (for speed)
muN=zeros(1,nv); 
deltaN=zeros(1,nv); 
lambdaN=zeros(1,nv); 
phiN=zeros(1,nv);
%cycle (for the 
for i=1:nv
    [muN(i),deltaN(i),lambdaN(i),phiN(i),n_iterN] ...
    =f_param_linN(chi(i),gamma(i),LeN,NN);
    %note that this function could also provide separate
    %deltaA, deltaV, lambdaA, lambdaV, phiA, phiV
end

%-------- set up plots ----------
fig1=figure;
%create line types and legend
lt={'-r','--k','-k','-.g'}; %line type
lw=[1,1,1.5,1.5];           %line width
subplot(4,1,4); hold on;
pp=-100:-100;               %invisible points (just for legend)
for i=1:4
    plot(pp,pp,lt{i},'linewidth',lw(i));
end
xlabel(xlab);               %label of variable parameter
legend('Sav.', 'lin0', 'linR', 'linN'); %create legend
xmin=-0.05;
xmax=max(var)*1.01;

%-------- plots ----------

%dimensionless velocity parameter
subplot(4,1,1); hold on;
plot(var,muS,lt{1},'linewidth',lw(1));
plot(var,mu0,lt{2},'linewidth',lw(2));
plot(var,muR,lt{3},'linewidth',lw(3));
plot(var,muN,lt{4},'linewidth',lw(4));
ylabel('\mu');
pp=[muS mu0 muR muN];
axis([xmin xmax min(pp)-0.05 max(pp)+0.05]);

%dimensionless damping parameter
subplot(4,1,2); hold on;
plot(var,deltaS,lt{1},'linewidth',lw(1));
plot(var,delta0,lt{2},'linewidth',lw(2));
plot(var,deltaR,lt{3},'linewidth',lw(3));
plot(var,deltaN,lt{4},'linewidth',lw(4));
ylabel('\delta');
pp=[deltaS delta0 deltaR deltaN];
axis([xmin xmax min(pp)-0.05 max(pp)+0.05]);

%dimensionless wavenumber
subplot(4,1,3); hold on;
plot(var,lambdaS,lt{1},'linewidth',lw(1));
plot(var,lambda0,lt{2},'linewidth',lw(2));
plot(var,lambdaR,lt{3},'linewidth',lw(3));
plot(var,lambdaN,lt{4},'linewidth',lw(4));
ylabel('\lambda');
pp=[lambdaS lambda0 lambdaR lambdaN];
axis([xmin xmax min(pp)-0.05 max(pp)+0.05]);

%phase lag
subplot(4,1,4); hold on;
plot(var,phiS,lt{1},'linewidth',lw(1));
plot(var,phi0,lt{2},'linewidth',lw(2));
plot(var,phiR,lt{3},'linewidth',lw(3));
plot(var,phiN,lt{4},'linewidth',lw(4));
ylabel('\phi');
pp=[phiS phi0 phiR phiN];
axis([xmin xmax min(pp)-0.05 max(pp)+0.05]);
