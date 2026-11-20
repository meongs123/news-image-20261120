// news-image-20261120 — make.fun entry program.
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
mkdirSync(outputDir, { recursive: true });
writeFileSync(targetPath, imageBytes);

// Round-trip check: the copy must be exactly the input bytes.
const writtenBytes = readFileSync(targetPath);
if (!writtenBytes.equals(imageBytes)) {
  console.error(`copy mismatch: wrote ${writtenBytes.length} bytes, expected ${imageBytes.length}`);
  process.exit(1);
}
console.log(`copied ${imageBytes.length} bytes: ${sourcePath} -> ${targetPath}`);
