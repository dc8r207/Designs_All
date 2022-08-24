Auxiliary material for Paper 2010JC006616
Revisiting linearized one-dimensional tidal propagation
Marco Toffolon - Dipartimento di Ingegneria Civile e Ambientale, University of Trento, Italy.
Hubert H. G. Savenije - Department of Water Management, Delft University of Technology, Delft, Netherlands. UNESCO-IHE Institute for Water Education, Delft, Netherlands.
JOURNAL OF GEOPHYSICAL RESEARCH, VOL. 116, C07007, DOI:10.1029/2010JC006616

---------------------------------------------------
Contact:
Marco Toffolon, Department of Civil and Environmental Engineering, University of Trento, Via Mesiano, 77, I-38123 Trento, Italy. (marco.toffolon@ing.unitn.it)
---------------------------------------------------


Two examples of Matlab codes are provided:


1. TIDAL PROPAGATION
Calculate tidal propagation along the estuary (water level and velocity).

Files:
"tidal_progagation.m" - main program
"subroutine_setup_plots.m" - subroutine, prepare plots
"subroutine_results_plots.m" - subroutine, calculate wave characteristics and plot them

Default setting produces plots as in Figure 2 (without comparison with numerical results):
inf=2;          %landward boundary condition (=2 closed channel)
dimless=1;      %plot type (=1 dimensionless plots)
epsilon=0.2;    %dimensionless tidal amplitude [-]
Le=90*km;   %estuary length [m]
ks=45;      %friction [m^(1/3)/s]
D0=10;      %depth at the mouth [m]
Lz=0*km;   %depth convergence length [m] (=0 constant depth)
B0=1000;    %width at the mouth [m]
Lb=60*km;   %width convergence length [m] (=0 constant width)



2. PARAMETERS AT THE MOUTH
Calculate dimensionless parameters at the mouth as a function of gamma/chi.

Files:
"parameters_at_the_mouth.m" - main program
"f_param_setal.m" - function, Savenije et al. (2008) solution (single reach)
"f_param_lin0.m" - function, 'lin0' model (single reach, friction without iterative refinement)
"f_param_linR.m" - function, 'linR' model (single reach, friction with iterative refinement)
"f_param_linN.m" - function, 'linN' model (multiple reaches, friction with iterative refinement)

Default setting produces plots as in Figure 6 (without comparison with numerical results):
varvar=1;       %=1 variable gamma
gamma_max=3.6;  %max value of gamma (total convergence)
chi_max=3.56;   %fixed value of chi (friction parameter)
