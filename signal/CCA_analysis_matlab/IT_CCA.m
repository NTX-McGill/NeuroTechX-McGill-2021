function [r, Wx, Wxx] = IT_CCA(Signal,  Template)
[Wx, Wxx, r] = canoncorr(Signal, Template);
end