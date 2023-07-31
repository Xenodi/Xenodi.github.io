const XMLWriter = require("xml-writer");
const XMLParser = require("xml-parser");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const archiver = require("archiver");

function zipDirectory(sourceDir, outPath, destpath) {
    const archive = archiver("zip", { zlib: { level: 9 }, });
    const stream = fs.createWriteStream(outPath);

    return new Promise((resolve, reject) => {
        archive
            .directory(sourceDir, destpath)
            .on("error", err => reject(err))
            .pipe(stream)
        ;

        stream.on("close", () => resolve());
        archive.finalize();
    });
  }

const xw = new XMLWriter();

xw.startDocument("1.0", "UTF-8").startElement("addons");

if (!fs.existsSync(path.join(".", "zips"))) fs.mkdirSync(path.join(".", "zips"));

fs.readdirSync(path.join(".", "addons")).forEach((addonName) => {
    const addonXml = fs.readFileSync(path.join(".", "addons", addonName, "addon.xml"), "utf-8");

    xw.writeRaw(addonXml.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", ""));

    const version = XMLParser(addonXml).root.attributes.version;

    if (fs.existsSync(path.join(".", "zips", addonName))) {
        fs.rmSync(path.join(".", "zips", addonName), { recursive: true });
    }

    fs.mkdirSync(path.join(".", "zips", addonName));
    fs.copyFileSync(path.join(".", "addons", addonName, "addon.xml"), path.join(".", "zips", addonName, "addon.xml"));
    fs.copyFileSync(path.join(".", "addons", addonName, "icon.png"), path.join(".", "zips", addonName, "icon.png"));

    zipDirectory(path.join(".", "addons", addonName), path.join(".", "zips", addonName, `${addonName}-${version}.zip`), addonName).then(() => {
        if (addonName === "repository.xenodi") fs.copyFileSync(path.join(".", "zips", addonName, `${addonName}-${version}.zip`), path.join(".", `${addonName}-${version}.zip`))
    });
});

xw.endElement();

fs.writeFileSync(path.join(".", "zips", "addons.xml"), xw.toString());
fs.writeFileSync(path.join(".", "zips", "addons.xml.md5"), crypto.createHash("md5").update(xw.toString()).digest("hex"));