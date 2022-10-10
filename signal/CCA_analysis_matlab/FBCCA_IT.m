function r = FBCCA_IT(Signal, fundFrequency, lowerFrequency, ...
    upperFrequency, numHarmonics, Template, a, b, numFB, sampleRate, FiltOrder)
sum=0;
for i=1:numFB
    [beta, alpha] = cheby1(FiltOrder, 1, [(lowerFrequency*2)/sampleRate (upperFrequency*2)/sampleRate], 'bandpass');
    FB = filtfilt(beta, alpha, Signal);
    rho = standardCCA_ITCCA(FB(1:end-4,:), fundFrequency, numHarmonics, Template(1:end-4,:));
    % remove last 4 time points
    sum=sum+(power(i,-a)+b)*(rho^2);
end
r=sum;
end
