load Af_distance.txt
load Af_elevation.txt
A = Af_distance;
B = Af_elevation;
[m,n] = size(A);
offset_norm_elev = nan(m,n);
median_norm_offset = nan(n,1);
iqr_norm_offset = nan(n,1);
for i = 1:n
    X = A(:,i);
    E = B(:,i);
    R = max(B(:,i))-min(B(:,i));
    x1 = A(1,i);
    x2 = max(A(:,i));
    y1 = B(1,i);
    y2 = max(B(:,i));%where x1,y1 x2,y2 are the long profile endpoints
    x = [x1 x2];
    y = [y1 y2];
    [r m b] = regression(x,y,'one');
    Y = m*X+b; %Y values on the line
    offset_elev = (E-Y)/R;
    offset_norm_elev(:,i) = offset_elev;
    mean_norm_offset(i) = nanmean(offset_elev);
    median_norm_offset(i) = nanmedian(offset_elev);
    iqr_norm_offset(i) = iqr(offset_elev);
end
boxplot(offset_norm_elev,'Notch','on')
set(gca,'YMinorTick','on')
xlabel('River');
ylabel('Normalised concavity index')
axis([0.5,7.5,-1,0.5])
mean(median_norm_offset)
std(median_norm_offset)
stderror=std(median_norm_offset)/sqrt(length(median_norm_offset))