function r = standardCCA_ITCCA(Signal, fundFrequency, numHarmonics, Template)
[r1, Wxy, ~, ~] = standardCCA(Signal, fundFrequency, numHarmonics);
[r5, Wx, ~] = IT_CCA(Signal, Template);
r2 = corrcoef([Signal*(Wx(:,1)) Template*(Wx(:,1))]);
r3 = corrcoef([Signal*(Wxy(:,1)) Template*(Wxy(:,1))]);
[~, Wxxy, ~, ~] = standardCCA(Template, fundFrequency, numHarmonics);
r4 = corrcoef([Signal*(Wxxy(:,1)) Template*(Wxxy(:,1))]);
rho_array = zeros(1,5);
rho_array(1)=r1(1);
rho_array(2)=r2(1,2);
rho_array(3)=r3(1,2);
rho_array(4)=r4(1,2);
rho_array(5)=r5(1);
r=sum(sign(rho_array).*power(rho_array,2));
end