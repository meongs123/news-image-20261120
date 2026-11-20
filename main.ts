// news-image-20261120 v3 — make.fun entry program.
// Delivers the repository's entry.png to the harness output path as an
// exact byte-for-byte copy. Node 22, standard library only, no network.
// The copy is deterministic: the bytes written are the bytes read, so two
// runs always produce identical output.
import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const inputFile = path.join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputFile = path.join(outDir, "entry.png");

const haveImage = fs.existsSync(inputFile);
if (!haveImage) {
  console.error(`no entry image yet: ${inputFile}`);
  process.exit(1);
}
// Read the entry only once the file is known to exist.
const bytes = fs.readFileSync(inputFile);

// The intake only grades a real PNG, so refuse anything else here
// instead of handing the harness a stray file.
const magic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < magic.length || !bytes.subarray(0, 8).equals(magic)) {
  console.error(`not a PNG: ${inputFile} (${bytes.length} bytes)`);
  process.exit(1);
}
if (bytes.length > 1024 * 1024) {
  console.error(`over the 1 MiB limit: ${bytes.length} bytes`);
  process.exit(1);
}
// Width and height sit in the IHDR chunk as big-endian uint32s at bytes
// 16-23; an oversize image would be rejected at intake, so refuse it now.
const picWidth = bytes.readUInt32BE(16);
const picHeight = bytes.readUInt32BE(20);
if (picWidth > 1024 || picHeight > 1024) {
  console.error(`over the 1024x1024 limit: ${picWidth}x${picHeight}`);
  process.exit(1);
}
// Guards passed — the bytes below are a valid PNG under 1 MiB, 1024x1024.
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outputFile, bytes);

// Round-trip check: what landed on disk must equal what was read.
const delivered = fs.readFileSync(outputFile);
if (!delivered.equals(bytes)) {
  console.error(
    `copy mismatch: wrote ${delivered.length} bytes, expected ${bytes.length}`,
  );
  process.exit(1);
}
// Copy verified — the delivered bytes equal the source bytes.
console.log(`copied ${bytes.length} bytes: ${inputFile} -> ${outputFile}`);
