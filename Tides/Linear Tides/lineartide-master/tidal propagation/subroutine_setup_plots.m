%subroutine: set up plots

%------ legend ------
%create legend with fictitous lines to have the correct order
subplot(3,1,2);hold on
plot([-1 -1],[-1 -1],'-.k');
plot([-1 -1],[-1 -1],'--k');
plot([-1 -1],[-1 -1],'+-k');
plot([-1 -1],[-1 -1],'-k');
legend('lin0','linR','linN','num');

%------ scales ------
%coordinates and scales for plots
if(dimless==1)      %for dimensionless plots
    xp=L0;          %length scale [m]
    ap=epsilon*D0;  %water level scale [m]
    up=epsilon*C0;  %velocity scale [m/s]
else                %for dimensional plots
    xp=km;          %x-coordinate [m/km]
    ap=1;           %water level scale [-]
    up=1;           %velocity scale [-]
end

%------ labels ------
%set labels for dimensionless/dimensional plots
if(dimless==1)      %dimensionless plots
    subplot(3,1,1); hold on;
    ylabel('|A^*|');
    subplot(3,1,2); hold on;
    ylabel('|V^*|');
    subplot(3,1,3); hold on;
    xlabel('x^*');
    ylabel('\phi [rad]');
else                %dimensional plots
    subplot(3,1,1); hold on;
    ylabel('A [m]');
    subplot(3,1,2); hold on;
    ylabel('V [m/s]');
    subplot(3,1,3); hold on;
    xlabel('x [km]');
    ylabel('\phi [rad]');
end
