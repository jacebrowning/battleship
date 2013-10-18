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
hist3d(round_1, alpha=12.5, theta=27.5, flag=[1,1,0], ebox=[0,10,0,10,-1,10]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end
hist3d(round_2, alpha=12.5, theta=27.5, flag=[1,1,0], ebox=[0,10,0,10,-1,10]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end
hist3d(round_3, alpha=12.5, theta=27.5, flag=[1,1,0], ebox=[0,10,0,10,-1,10]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end


// Close the window
xdel(winsid());