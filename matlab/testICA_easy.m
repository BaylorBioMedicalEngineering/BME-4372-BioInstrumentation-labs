t=1:pi/200:8*pi;
s=sin(t);
r=rand(size(t));
mix=[.75 .25
     .4  .6];
 X=[s;r];
 meas=mix*X;

[icasig,A,W] = fastica (X);
figure;
subplot(2,3,1), plot(t,meas(1,:));
subplot(2,3,4), plot(t,meas(2,:));
subplot(2,3,2), plot(t,icasig(1,:));
subplot(2,3,5), plot(t,icasig(2,:));
subplot(2,3,3), plot(t,s);
subplot(2,3,6), plot(t,r);