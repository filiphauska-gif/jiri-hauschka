const { artworks } = require('../lib/artworks');
const fs = require('fs');

let js = 'export const artworks = [\n';
for (const a of artworks) {
  js += `  {\n`;
  js += `    slug: '${a.slug}',\n`;
  js += `    title: '${a.title.replace(/'/g, "\\'")}',\n`;
  js += `    year: '${a.year}',\n`;
  js += `    medium: '${a.medium.replace(/'/g, "\\'")}',\n`;
  js += `    size: '${(a.size || '').replace(/'/g, "\\'")}',\n`;
  js += `    image: '${a.image}',\n`;
  js += `    ar: true,\n`;
  js += `    glb: '${a.glb || '/assets/' + a.slug + '.usdz'}',\n`;
  js += `    usdz: '${a.usdz || '/assets/' + a.slug + '.usdz'}',\n`;
  js += `    poster: '${a.poster || ''}',\n`;
  js += `  },\n`;
}
js += '];\n\n';
js += 'export function artworkBySlug(slug) {\n';
js += '  return artworks.find(a => a.slug === slug);\n';
js += '}\n';

fs.writeFileSync(process.argv[2], js);
console.log('Written ' + artworks.length + ' artworks to ' + process.argv[2]);
