// Generated code to display 3 graphs of Battleship simulation results

// Y coordinates
sample_sizes = [0              25             ];

// X coordinates
guesses      = [60             55             ;
                65             54             ];
steps        = [1000           2000           ;
                1100           2100           ];
durations    = [6              10.5           ;
                5.1            11             ];

// Graph number of rounds vs. sample sizes
subplot(1, 3, 1);
title ("Algorithm Accuracy");
plot(sample_sizes, guesses, 'o', sample_sizes, mean(guesses, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [-5;30];
xlabel ("Monte Carlo Sample Size");
ylabel ("Number of Guesses Required");

// Graph algorithm steps vs. sample sizes
subplot(1, 3, 2);
title ("Algorithm Efficiency (Steps)");
plot(sample_sizes, steps, 'o', sample_sizes, mean(steps, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [-5;30];
xlabel ("Monte Carlo Sample Size");
ylabel ("Number Steps Per Game");

// Graph game duration vs. sample sizes
subplot(1, 3, 3);
title ("Algorithm Efficiency (Duration)");
plot(sample_sizes, durations, 'o', sample_sizes, mean(durations, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [-5;30];
xlabel ("Monte Carlo Sample Size");
ylabel ("Simulation Duration (Seconds)");

// Close the window after a mouse click
xclick();
xdel(winsid());