// Generated code to display the Monte Carlo experiments for each round of a game
round_1 = [0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   1   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   ];
round_2 = [0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   -1  0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   ];
round_3 = [0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   
           0   0   0   0   0   0   0   0   0   0   ];


// Automatically clear the graph after each plot
da=gda();
da.auto_clear = 'on';

// Draw each round and wait for a mouse click
subplot(1, 2, 1);
title ("Round 1: Algorithm Frequency Results");
hist3d(round_1, alpha=50, theta=25, flag=[1,1,0], ebox=[0,10,0,10,0,10]);
subplot(1, 2, 2);
title ("Previous Round Hits and Misses");
hist3d(round_1 * -1/4, alpha=34.5, theta=45, flag=[1,1,0], ebox=[0,10,0,10,0,1]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end
subplot(1, 2, 1);
title ("Round 2: Algorithm Frequency Results");
hist3d(round_2, alpha=50, theta=25, flag=[1,1,0], ebox=[0,10,0,10,0,10]);
subplot(1, 2, 2);
title ("Previous Round Hits and Misses");
hist3d(round_2 * -1/4, alpha=34.5, theta=45, flag=[1,1,0], ebox=[0,10,0,10,0,1]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end
subplot(1, 2, 1);
title ("Round 3: Algorithm Frequency Results");
hist3d(round_3, alpha=50, theta=25, flag=[1,1,0], ebox=[0,10,0,10,0,10]);
subplot(1, 2, 2);
title ("Previous Round Hits and Misses");
hist3d(round_3 * -1/4, alpha=34.5, theta=45, flag=[1,1,0], ebox=[0,10,0,10,0,1]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end


// Close the window
messagebox("Simulation completed.");
xclick();
xdel(winsid());