
var starData1k = require('./1k_stars_sorted_by_dist.json');
var fs = require('fs');

if(!fs.existsSync('new')) fs.mkdirSync('new');
for(var i in starData1k) {
    let star = starData1k[i];
    let src = `./old_images/hip${i}.png`;
    let dst = `./images/hip${star.hip}.png`;
    if(fs.existsSync(src)) {
        console.log('id', i, 'hip', star.hip, '--', src, '=>', dst);
        fs.copyFileSync(src,dst);
    } else {
        console.log('id', i, 'hip', star.hip, '--', src, '<>', 'NOT_FOUND');
    }
}