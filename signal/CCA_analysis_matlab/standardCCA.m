function [r, Wx, Wy, reference] = standardCCA(Signal, fundFrequency, numHarmonics)
[tpts, ~] = size(Signal);
ReferenceSignal = zeros(tpts, 2*numHarmonics);
T = (1:(tpts))*(1/250);
for i=1:(numHarmonics)
    ReferenceSignal(:, 2*i-1) = (sin(2*pi*fundFrequency*i*T))';
    ReferenceSignal(:, 2*i) = (cos(2*pi*fundFrequency*i*T))';
end
[Wx, Wy, r] = canoncorr(Signal, ReferenceSignal);
reference = ReferenceSignal;
end