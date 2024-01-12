clc;
clear;
%% Numerical Solution
U_inf = 10; %Free stream velocity
L=1;
Re=10000;
nu = 1/Re;
delta = 5/sqrt(Re); %Boundary layer thickness at x=1m
Y =  2*delta; %Size of domain in Y-direction
Nx = 3000; %Number of points along x axis
Ny = 90; %Number of points along y axis
dx = L/Nx; %Grid size along x axis
dy = Y/Ny; %Grid size along y axis

stability_criterion = 0.5*Re*(dy^2);
if dx <= stability_criterion 
    disp("Stability criterion met! Please wait for results.")
    u = zeros(Nx,Ny); %Matrix to store u values
    v = zeros(Nx,Ny); %Matrix to store v values
    x = linspace(0,L,Nx);
    y = linspace(0,Y,Ny);
    %%
    u(:,1) = 0; %No slip condition over flat flate
    u(1,:) = 1; %Free stream velocity condition at inlet since we are solving for non-dimensional u
    u(:,Ny) = 1; %Free stream velocity condition at domain top since we are solving for non-dimensional u
    u(1,1)=0;
    
    v(1:Nx) = 0; %No slip condition over flat plate
    v(1,:) = 0; %No vertical velocity component at inlet free stream
    v(:,Ny) = 0; %No vertical velocity component at domain top free stream
   
    %%
    for t = 1:Nx

        for j = 2:Ny-1
            for i = 1:Nx-1
                       
                u(i+1,j) = u(i,j) + (nu*(u(i,j+1)-2*u(i,j)+u(i,j-1))*(dx))/((u(i,j)*dy^2))-((u(i,j+1)-u(i,j-1))*v(i,j)*dx)/(2*u(i,j)*dy);
                v(i+1,j) = v(i+1,j-1) - ((0.5*dy*(u(i+1,j)-u(i,j)+u(i+1,j-1)-u(i,j-1)))/dx);
            end
        end
    end
    figure(1)
    colorbar
    hold on
    contourf(x,y,u',25)
    title("Contour plot of horizontal component of velocity - u")
    xlabel("Distance along the plate")
    ylabel("Vertical distance above the plate")
    legend('u contour')
    hold off
    figure(2)
    colorbar
    hold on
    contourf(x,y,v',25)
    title("Contour plot of vertical component of velocity - v")
    xlabel("Distance along the plate")
    ylabel("Vertical distance above the plate")
    legend('v contour')
    hold off
else
    disp("Stability criterion not met! Recheck your gridpoint values")
end
%%




