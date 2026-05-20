-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Video" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "title" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'pending',
    "style" TEXT NOT NULL DEFAULT 'slideshow',
    "duration" REAL NOT NULL DEFAULT 3.0,
    "transition" TEXT NOT NULL DEFAULT 'fade',
    "colorEffect" TEXT,
    "motionEffect" TEXT,
    "frameEffect" TEXT,
    "textPosition" TEXT NOT NULL DEFAULT 'bottom',
    "captions" TEXT,
    "music" TEXT,
    "outputPath" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);
INSERT INTO "new_Video" ("createdAt", "duration", "id", "music", "outputPath", "status", "style", "title", "transition", "updatedAt") SELECT "createdAt", "duration", "id", "music", "outputPath", "status", "style", "title", "transition", "updatedAt" FROM "Video";
DROP TABLE "Video";
ALTER TABLE "new_Video" RENAME TO "Video";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
