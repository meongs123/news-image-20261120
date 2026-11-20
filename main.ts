// news-image-20261120 v2 — make.fun entry program.
// Copies the repository's entry.png byte-identical to the output path.
// Node 22, standard library only, no network, deterministic: two runs
// produce identical bytes because the input bytes are never modified.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(repoRoot, "entry.png");

// The harness runs with a writable /output; a local run can point
// elsewhere with MAKEFUN_OUTPUT_DIR (e.g. MAKEFUN_OUTPUT_DIR=out).
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const targetPath = join(outputDir, "entry.png");

if (!existsSync(sourcePath)) {
  console.error(`missing input image: ${sourcePath} (not built yet)`);
  process.exit(1);
}

const imageBytes = readFileSync(sourcePath);

// The entry must be a real PNG the harness can grade, not a stray file.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (imageBytes.length < PNG_SIGNATURE.length || !imageBytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  console.error(`input is not a PNG: ${sourcePath} (${imageBytes.length} bytes)`);
  process.exit(1);
}
if (imageBytes.length > 1024 * 1024) {
  console.error(`input exceeds the 1 MiB limit: ${imageBytes.length} bytes`);
  process.exit(1);
}
// The competition caps the image at 1024x1024. Width and height live in
// the IHDR chunk as big-endian uint32 at bytes 16-23; refuse an oversize
// input instead of shipping an entry the intake would reject.
const width = imageBytes.readUInt32BE(16);
const height = imageBytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  console.error(`input exceeds the 1024x1024 limit: ${width}x${height}`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(targetPath, imageBytes);

// Round-trip check: the copy must be exactly the input bytes.
const writtenBytes = readFileSync(targetPath);
if (!writtenBytes.equals(imageBytes)) {
  console.error(`copy mismatch: wrote ${writtenBytes.length} bytes, expected ${imageBytes.length}`);
  process.exit(1);
}
console.log(`copied ${imageBytes.length} bytes: ${sourcePath} -> ${targetPath}`);
