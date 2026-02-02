const fs = require('fs');
const filePath = 'C:/Users/Acer/Desktop/web sayfası/data.js';

try {
    let content = fs.readFileSync(filePath, 'utf8');

    // Try to find the object literal
    const start = content.indexOf('{');
    const end = content.lastIndexOf('}');

    if (start === -1 || end === -1) {
        console.log("Error: Brace not found.");
    } else {
        const jsonPart = content.substring(start, end + 1);
        try {
            // Using eval to handle relaxed JSON (keys without quotes if any, or trailing commas)
            const data = eval('(' + jsonPart + ')');

            console.log("--- ANALYSIS REPORT ---");
            const keys = Object.keys(data);
            console.log(`Total Categories: ${keys.length}`);

            let totalPrompts = 0;
            keys.forEach(key => {
                const count = Array.isArray(data[key]) ? data[key].length : 'Not an array';
                console.log(`- Category: [${key}] -> ${count} items`);
                if (typeof count === 'number') totalPrompts += count;
            });
            console.log(`\nGrand Total Prompts: ${totalPrompts}`);

        } catch (parseError) {
            console.error("Parsing Error:", parseError.message);
            console.log("Snippet causing error:", jsonPart.substring(0, 200) + "...");
        }
    }
} catch (e) {
    console.error("File Error:", e.message);
}
