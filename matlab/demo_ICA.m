t=0:.01:12;
XT1=sin(t);
XT2=mod(t,1);
plot(t,XT1,'c-',t,XT2,'c-.')
m1=mean(XT1);
m2=mean(XT2);
XT=[XT1-m1
    XT2-m2];
mix=[.9  .1
     .2  .8];
X=mix*XT;
[icasig,A,W] = fastica (X);
% , 'approach', 'defl'
% , 'g', 'tanh'
% , 'g', 'skew'
% , 'g', 'gauss'
[icasig] = fastica (X, 'initGuess', A, 'approach', 'defl');
minica=zeros(2,1);
minica=min(icasig,[],2);
ICA1=icasig(1,:)+minica(1);
ICA2=icasig(2,:)+minica(2);
figure;
subplot(2,3,1), plot(t,X(1,:));
subplot(2,3,4), plot(t,X(2,:));
subplot(2,3,2), plot(t,icasig(1,:));
subplot(2,3,5), plot(t,icasig(2,:));
subplot(2,3,3), plot(t,XT1);
subplot(2,3,6), plot(t,XT2);
