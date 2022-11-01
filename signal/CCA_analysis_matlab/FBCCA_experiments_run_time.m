% 48.875 seconds 
all_channels=[48 54 55 56 57 58 61 62 63];

%{
The four dimensions indicate: 
0:      ‘Electrode index’
1:      ‘Time points’
3:      ‘Target index’(in this case 40 different charactors in each block)
4:      ‘Block index’ (in this case 6 blocks)
%}
load('S2.mat', 'data')
warning('off')

% S2 result
[mean, std]=crossValidateFBCCA(data,all_channels,5,2,1)


% 48.16 seconds (98% of the total time)
function [meanScores, stdScores]=crossValidateFBCCA(data, channels, numHarmonics, dataLength, includesLatency)
[~, ~, numTargets, numBlocks]=size(data);
scores=zeros(numBlocks, 1);
results=zeros(1,40);
matrix=zeros(40);
% 0.158 seconds ()
[beta, alpha] = cheby1(2,1,[7/125 90/125],'bandpass');
for b=1:numBlocks
    blocks=1:numBlocks;
    blocks(b)=[];
    for j=1:numTargets
    %test = filter(bpFilt, data([45 46 48 50 51 61 62 63],125+35:160+125,j,1)');
    test = data(channels,125+35*includesLatency:125+35*includesLatency+250*dataLength,j,b)';
    unfilt = mean(data(channels,125+35*includesLatency:125+35*includesLatency+250*dataLength,j,blocks), 4)';
    %unfilt = data(channels,125+35:end-125,j,6)';
    template = filter(beta, alpha, unfilt);
        for k=1:5
            for i=1:8
            % 47.836 seconds (97.87% of the total time)with 9600 calls
            % fuindamental afrequencies 
            rho=FBCCA_IT(test,8+1*(i-1)+0.2*(k-1),8,88,numHarmonics,template,1,0,4,250,4);
            results(i+(k-1)*8)=rho;
            end
        end
    matrix(j,:)=results;
    end
    counter=0;
    for i=1:numTargets
        [~, arg]=max(matrix(i,:));
        if arg==i
            counter=counter+1;
        end
    end
    scores(b,1)=counter*100/numTargets;
end
meanScores=mean(scores);
stdScores=std(scores);
end