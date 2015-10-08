t=1:pi/200:8*pi;
s1=sin(t);
s2=sawtooth(t*(2/3));
r=rand(size(t));
mix=[.5  .25 .25
     .25 .5  .25
     .25 .25 .5];
 X=[s1;s2;r];
 meas=mix*X;

[icasig,A,W] = fastica (X);
figure;
subplot(3,3,1), plot(t,meas(1,:));
subplot(3,3,4), plot(t,meas(2,:));
subplot(3,3,7), plot(t,meas(3,:));
subplot(3,3,2), plot(t,icasig(1,:));
subplot(3,3,5), plot(t,icasig(2,:));
subplot(3,3,8), plot(t,icasig(3,:));
subplot(3,3,3), plot(t,s1);
subplot(3,3,6), plot(t,s2);
subplot(3,3,9), plot(t,r);